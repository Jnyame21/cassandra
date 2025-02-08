# Django
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.core.validators import EmailValidator
from django.utils import timezone
from django.http import FileResponse
from django.forms import DateField
from django.db.models import Q
from collections import defaultdict

# Document Manipulation
import pandas as pd

from api.models import *
from api.serializer import *
import random
from datetime import datetime
import json

# Django Restframework
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


# Admin
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_head_data(request):
    head = Staff.objects.select_related('school', 'current_role__level').get(user=request.user)
    school = head.school
    current_level = head.current_role.level
    current_academic_year = AcademicYear.objects.get(id=int(request.GET.get('year')))
    current_term = int(request.GET.get('term'))
    academic_years = AcademicYearSerializer(AcademicYear.objects.select_related('level').filter(school=school, level=current_level).order_by('-start_date'), many=True).data
    student_classes = Classe.objects.select_related('head_teacher__user', 'program').prefetch_related('subjects', 'students__user').filter(school=school, level=current_level).order_by('students_year')
    student_classes_data = ClassesSerializerOne(student_classes, many=True).data
    subject_assignments = SubjectAssignment.objects.prefetch_related('subjects', 'students_class__students__user').select_related('teacher__user').filter(school=school, level=current_level, academic_year=current_academic_year, academic_term=current_term)
    all_subject_assignments_data = SubjectAssignmentSerializerOne(subject_assignments, many=True).data
    departments_data = []
    programs = []
    if current_level.has_departments:
        department_objs = Department.objects.select_related('hod__user').prefetch_related('subjects', 'teachers__user').filter(school=school, level=current_level)
        departments_data = DepartmentNameHODSubjectsSerializer(department_objs, many=True).data
        
    if current_level.has_programs:
        programs = [x.identifier for x in Program.objects.filter(schools=school, level=current_level)]

    staff_objs = Staff.objects.select_related('user').prefetch_related('roles', 'departments', 'subjects').filter(school=school).order_by('-date_created')
    staff_data = StaffSerializerOne(staff_objs, many=True).data
    subjects = [x.identifier for x in Subject.objects.filter(schools=school, level=current_level)]

    subject_assignments_data = {}
    all_students_assessments_data = {}
    all_students_exams_data = {}
    all_students_results_data = {}
    all_students_assessments_objs = Assessment.objects.select_related('student__user', 'student_class', 'subject').filter(school=school, level=current_level, academic_year=current_academic_year, academic_term=current_term).order_by('-score')
    assessment_by_class_subject = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for _assessment in all_students_assessments_objs:
        assessment_by_class_subject[_assessment.student_class.name][_assessment.subject.name][_assessment.title].append(_assessment)
    
    all_students_exams_objs = Exam.objects.select_related('student__user', 'student_class', 'subject').filter(school=school, level=current_level, academic_year=current_academic_year, academic_term=current_term).order_by('-score')
    exams_by_class_subject = defaultdict(lambda: defaultdict(list))
    for _exam in all_students_exams_objs:
        exams_by_class_subject[_exam.student_class.name][_exam.subject.name].append(_exam)
    
    all_students_results_objs = StudentResult.objects.select_related('student__user', 'student_class', 'subject').filter(school=school, level=current_level, academic_year=current_academic_year, academic_term=current_term).order_by('-result')
    results_by_class_subject = defaultdict(lambda: defaultdict(list))
    for _result in all_students_results_objs:
        results_by_class_subject[_result.student_class.name][_result.subject.name].append(_result)
    
    for assign in subject_assignments:
        students_class = assign.students_class
        students_class_name = students_class.name
        class_students = students_class.students.all()
        subject_assignments_data[students_class_name] = SubjectAssignmentSerializerTwo(assign).data
        
        assessment_class_data = {}
        exams_class_data = {}
        results_class_data = {}
        assignment_subjects = assign.subjects.all()
        for _subject in assignment_subjects:
            
            ## Students Assessments
            assessment_subject_data = {}
            assessment_titles = set(assessment_by_class_subject[students_class_name][_subject.name].keys())
            for _title in assessment_titles:
                assessments_with_title = assessment_by_class_subject[students_class_name][_subject.name][_title]
                first_assessment = assessments_with_title[0]
                assessment_title_data = {
                    'title': _title, 
                    'total_score': first_assessment.total_score, 
                    'description': first_assessment.description, 
                    'percentage': first_assessment.percentage, 
                    'assessment_date': first_assessment.assessment_date, 
                    'students_with_assessment': {}, 
                    'students_without_assessment': {}
                }
                students_with_assessments = set()
                for _assessment in assessments_with_title:
                    assessment_student = _assessment.student
                    if assessment_student:
                        students_with_assessments.add(assessment_student.st_id)
                        student_data = {
                            'name': f"{assessment_student.user.first_name} {assessment_student.user.last_name}",
                            'st_id': assessment_student.st_id,
                            'score': _assessment.score,
                            'comment': _assessment.comment,
                        }
                        assessment_title_data['students_with_assessment'][assessment_student.st_id] = student_data
                        
                for _student in class_students:
                    st_id = _student.st_id
                    if st_id not in students_with_assessments:
                        st_data = {
                            'name': f"{_student.user.first_name} {_student.user.last_name}",
                            'st_id': st_id,
                        }
                        assessment_title_data['students_without_assessment'][st_id] = st_data
                assessment_subject_data[_title] = assessment_title_data
            assessment_class_data[_subject.name] = assessment_subject_data
            
            # Students Exams
            exams_subject_data = {'students_with_exams': {}, 'students_without_exams': {}}
            all_subject_exams_objs = exams_by_class_subject[students_class_name][_subject.name]
            students_with_exams = set()
            if len(all_subject_exams_objs) > 0:
                first_exams_objs = all_subject_exams_objs[0]
                exams_subject_data['percentage'] = first_exams_objs.percentage
                exams_subject_data['total_score'] = first_exams_objs.total_score
                for _exams in all_subject_exams_objs:
                    exams_student = _exams.student
                    if exams_student:
                        student_data = {
                            'name': f"{exams_student.user.first_name} {exams_student.user.last_name}",
                            'st_id': exams_student.st_id,
                            'score': _exams.score,
                        }
                        exams_subject_data['students_with_exams'][exams_student.st_id] = student_data
                        students_with_exams.add(exams_student.st_id)
            
                for _student in class_students:
                    st_id = _student.st_id
                    if st_id not in students_with_exams:
                        student_data = {
                            'name': f"{_student.user.first_name} {_student.user.last_name}",
                            'st_id': st_id,
                        }
                        exams_subject_data['students_without_exams'][st_id] = student_data
            else:
                exams_subject_data['percentage'] = 0
                exams_subject_data['total_score'] = 0
                
            exams_class_data[_subject.name] = exams_subject_data
            
            # Students Results
            results_subject_data = {}
            all_subject_results_objs = results_by_class_subject[students_class_name][_subject.name]
            if len(all_subject_results_objs) > 0:
                first_result_obj = all_subject_results_objs[0]
                results_subject_data['total_assessment_percentage'] = first_result_obj.total_assessment_percentage
                results_subject_data['exam_percentage'] = first_result_obj.exam_percentage
                all_results = {}
                for _result in all_subject_results_objs:
                    result_student = _result.student
                    student_data = {
                        'result': _result.result,
                        'total_assessment_score': _result.total_assessment_score,
                        'exam_score': _result.exam_score,
                        'student': {'name': f"{_result.student.user.first_name} {_result.student.user.last_name}", 'st_id': result_student.st_id},
                        'remark': _result.remark,
                        'grade': _result.grade,
                        'position': _result.position,
                    }
                    all_results[result_student.st_id] = student_data
                results_subject_data['student_results'] = all_results
            
            else:
                results_subject_data['total_assessment_percentage'] = 0
                results_subject_data['exam_percentage'] = 0
                results_subject_data['student_results'] = {}
                
            results_class_data[_subject.name] = results_subject_data
            
        # All(assessments, exams, results) data for the class
        all_students_assessments_data[students_class_name] = assessment_class_data
        all_students_exams_data[students_class_name] = exams_class_data
        all_students_results_data[students_class_name] = results_class_data
        
    released_results_objs = ReleasedResult.objects.select_related('academic_year', 'released_by__user').filter(school=school, level=current_level).order_by('-date')
    released_results_data = ReleasedResultsSerializer(released_results_objs, many=True).data
    
    attendance_mappings = defaultdict(list)
    attendance_objs = StudentAttendance.objects.select_related('students_class').prefetch_related('students_present__user', 'students_absent__user').filter(school=school, level=current_level, academic_year=current_academic_year, academic_term=current_term).order_by('-date')
    for _attendance_ in attendance_objs:
        attendance_mappings[_attendance_.students_class.id].append(_attendance_)
        
    atttendance_data = {}
    for _class in student_classes:
        students_class_name = _class.name
        attendances = StudentsAttendanceSerializer(attendance_mappings[_class.id], many=True).data
        atttendance_data[students_class_name] = attendances
        
    return Response({
        'classes': student_classes_data,
        'departments': departments_data,
        'subjects': subjects,
        'staff': staff_data,
        'programs': programs,
        'academic_years': academic_years,
        'students_attendance': atttendance_data,
        'students_assessments': all_students_assessments_data,
        'students_exams': all_students_exams_data,
        'students_results': all_students_results_data,
        'subject_assignments': all_subject_assignments_data,
        'released_results': released_results_data,
    }, status=200)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_head_data(request):
#     head = request.user.staff
#     school = head.school
#     current_academic_year = AcademicYear.objects.get(school=school, name=request.GET.get('year'))
#     current_term = int(request.GET.get('term'))
#     if request.method == 'GET':
#         academic_years = AcademicYearSerializer(AcademicYear.objects.filter(school=school).order_by('-start_date'), many=True).data
#         classes_data = defaultdict(dict)
#         departments = []
#         programs = []
#         if school.has_departments:
#             departments_data = DepartmentNameSerializer(Department.objects.filter(school=school), many=True).data
#             departments = [_department['name'] for _department in departments_data]
#         if school.has_programs:
#             programs_data = ProgramNameSerializer(Program.objects.filter(schools=school), many=True).data
#             programs = [_program['name'] for _program in programs_data]
#         student_classes = Classe.objects.select_related('head_teacher__user', 'program').prefetch_related('subjects', 'students__user').filter(school=school).order_by('students_year')

#         for _class in student_classes:
#             class_name = _class.name
#             class_subjects = _class.subjects.all()
#             classes_data[class_name]['students'] = StudentSerializerOne(_class.students.all(), many=True).data
#             classes_data[class_name]['students_year'] = _class.students_year
#             classes_data[class_name]['program'] = _class.program.name if _class.program else None
#             classes_data[class_name]['head_teacher'] = StaffUserIdImgSerializer(_class.head_teacher).data if _class.head_teacher else None
#             classes_data[class_name]['subjects'] = []
#             for _subject in class_subjects:
#                 subject_data = {'name': _subject.name}
#                 subject_assignment = SubjectAssignment.objects.select_related('teacher__user').filter(school=school, students_class=_class, subjects=_subject, academic_year=current_academic_year, academic_term=current_term).first()
#                 if subject_assignment:
#                     teacher_data = StaffUserIdImgSerializer(subject_assignment.teacher).data
#                     subject_data['teacher'] = teacher_data['user']
#                     subject_data['teacher_img'] = teacher_data['img']
#                 else:
#                     subject_data['teacher'] = ''
#                     subject_data['teacher_img'] = ''
#                 classes_data[class_name]['subjects'].append(subject_data)
                
#         staff = StaffSerializerOne(Staff.objects.filter(school=school, is_active=True).order_by('-date_created'), many=True).data
#         subjects = [_subject.name for _subject in Subject.objects.filter(schools=school)]
        
#         return Response({
#             'classes': classes_data,
#             'departments': departments,
#             'subjects': subjects,
#             'staff': staff,
#             'programs': programs,
#             'academic_years': academic_years,
#         }, status=200)


# # @api_view(['GET'])
# # @permission_classes([IsAuthenticated])
# # def head_students_performance(request):
# #     head = request.user.head
# #     departments = SpecificDepartmentSerializer(Department.objects.filter(school=head.school).Exam("subjects"), many=True).data
# #     if not departments:
# #         return Response(status=401)
# #
# #     academic_year = AcademicYear.objects.get(school=head.school, name=request.GET.get('year'))
# #     all_results = ExamsSerializerWithoutStudentTeacher(Exam.objects.filter(school=head.school, academic_year=academic_year).order_by('-score'), many=True).data
# #
# #     data = []
# #     for department in departments:
# #         subjects = []
# #
# #         for subject in department['subjects']:
# #
# #             year_1 = {}
# #             year_2 = {}
# #             year_3 = {}
# #
# #             for year in range(1, 4):
# #                 for term in range(1, 4):
# #                     term_name = 'one' if term==1 else('two' if term==2 else 'three')
# #                     if year == 1:
# #                         year_1[f"term_{term_name}"] = [x['score'] for x in all_results if x['subject']['name'] == subject['name'] and x['student_year'] == year and x['academic_term'] == term]
# #                     elif year == 2:
# #                         year_2[f"term_{term_name}"] = [x['score'] for x in all_results if x['subject']['name'] == subject['name'] and x['student_year'] == year and x['academic_term'] == term]
# #                     elif year == 3:
# #                         year_3[f"term_{term_name}"] = [x['score'] for x in all_results if x['subject']['name'] == subject['name'] and x['student_year'] == year and x['academic_term'] == term]
# #
# #             subjects.append({'name': subject['name'], 'year_one': year_1, 'year_two': year_2, 'year_three': year_3})
# #
# #         data.append({
# #             'department': department['name'],
# #             'subjects': subjects,
# #         })
# #
# #     return Response(data)

    
    
    