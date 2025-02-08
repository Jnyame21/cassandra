# Django
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.core.validators import EmailValidator
from django.utils import timezone
from django.http import FileResponse
from django.forms import DateField
from django.db.models import Q

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
    subject_assignments = SubjectAssignment.objects.prefetch_related('subjects').select_related('teacher__user', 'students_class').filter(school=school, level=current_level, academic_year=current_academic_year, academic_term=current_term)
    subject_assignments_data = SubjectAssignmentSerializerOne(subject_assignments, many=True).data
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

    released_results_objs = ReleasedResult.objects.select_related('academic_year', 'released_by__user').filter(school=school, level=current_level).order_by('-date')
    released_results_data = ReleasedResultsSerializer(released_results_objs, many=True).data
    
    return Response({
        'classes': student_classes_data,
        'departments': departments_data,
        'subjects': subjects,
        'staff': staff_data,
        'programs': programs,
        'academic_years': academic_years,
        'subject_assignments': subject_assignments_data,
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

    
    
    