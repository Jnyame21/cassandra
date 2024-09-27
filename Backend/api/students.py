from api.models import *
from api.serializer import *

# Django Restframework
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist

from api.utils import get_student_transcript


# STUDENT
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_student_data(request):
    student = request.user.student
    school = student.school
    if request.method == 'GET':
        term = request.GET.get('term')
        current_academic_year = AcademicYear.objects.get(school=school, name=request.GET.get('year'))
        student_class = Classe.objects.get(school=school, students=student)
        class_data = ClasseWithSubjectsSerializer(student_class).data
        grading_system = GradingSystemSerializer(GradingSystem.objects.filter(school=school), many=True).data
        student_subjects = []
        academic_years_data = []
        
        for year in student_class.academic_years.all().order_by('-start_date'):
            year_serializer = AcademicYearSerializer(year).data
            term_one_results = []; term_one_attendance = []; term_one_assessments = []
            term_two_results = []; term_two_attendance = []; term_two_assessments = []
            term_three_results = []; term_three_attendance = []; term_three_assessments = []

            """
                Attendance
            """
            # term one
            term_one_attendance_all = StudentAttendance.objects.prefetch_related('students_absent').filter(school=school, students_class=student_class, academic_year=year, academic_term=1).order_by('-date')
            if term_one_attendance_all.count() != 0:
                term_one_attendance_data = StudentsAttendanceSerializer(term_one_attendance_all, many=True).data
                for __attendance in term_one_attendance_data:
                    attendance_st = StudentAttendanceStudentSerializer(student).data
                    if attendance_st in __attendance['students_absent']:
                        term_one_attendance.append({'date': __attendance['date'], 'status': 'ABSENT'})
                    else:
                        term_one_attendance.append({'date': __attendance['date'], 'status': 'PRESENT'})
            
            # term two
            term_two_attendance_all = StudentAttendance.objects.prefetch_related('students_absent').filter(school=school, students_class=student_class, academic_year=year, academic_term=2).order_by('-date')
            if term_two_attendance_all.count() != 0:
                term_two_attendance_data = StudentsAttendanceSerializer(term_two_attendance_all, many=True).data
                for __attendance in term_two_attendance_data:
                    attendance_st = StudentAttendanceStudentSerializer(student).data
                    if attendance_st in __attendance['students_absent']:
                        term_two_attendance.append({'date': __attendance['date'], 'status': 'ABSENT'})
                    else:
                        term_two_attendance.append({'date': __attendance['date'], 'status': 'PRESENT'})
            
            # term three
            if year_serializer['period_division']['name'] != 'SEMESTER':
                term_three_attendance_all = StudentAttendance.objects.prefetch_related('students_absent').filter(school=school, students_class=student_class, academic_year=year, academic_term=2).order_by('-date')
                if term_three_attendance_all.count() != 0:
                    term_three_attendance_data = StudentsAttendanceSerializer(term_three_attendance_all, many=True).data
                    for __attendance in term_three_attendance_data:
                        attendance_st = StudentAttendanceStudentSerializer(student).data
                        if attendance_st in __attendance['students_absent']:
                            term_three_attendance.append({'date': __attendance['date'], 'status': 'ABSENT'})
                        else:
                            term_three_attendance.append({'date': __attendance['date'], 'status': 'PRESENT'})
            
            """
                Results and Assessments
            """
            for subject in class_data['subjects']:
                st_subject = Subject.objects.get(name=subject['name'])
          
                # term one
                total_assessment_score_term_one = 0
                total_assessment_percentage_term_one = 0
                all_term_one_subject_assessments_data = StudentAssessmentSerializer(Assessment.objects.filter(school=school, student=student, subject=st_subject, academic_year=year, academic_term=1), many=True).data
                if len(all_term_one_subject_assessments_data) != 0:
                    for __assessment in all_term_one_subject_assessments_data:
                        total_assessment_score_term_one += float(__assessment['score'])*(float(__assessment['percentage'])/100)
                        total_assessment_percentage_term_one += float(__assessment['percentage'])
                        term_one_assessments.append({'subject': subject['name'], 'score': __assessment['score'], 'title': __assessment['title']})
                        
                all_term_one_subject_results = Exam.objects.filter(school=school, subject=st_subject, student_class=student_class, academic_year=year, academic_term=1).order_by('-score')
                try:
                    st_term_one_subject_result = Exam.objects.get(school=school, subject=st_subject, student=student, academic_year=year, academic_term=1)
                    st_term_one_subject_result_data = StudentExamsSerializer(st_term_one_subject_result).data
                    grading = None
                    st_exams_score = float(st_term_one_subject_result_data['score'])
                    st_total_subject_score = total_assessment_score_term_one + (st_exams_score*((100-total_assessment_percentage_term_one)/100))
                    for grade in  grading_system:
                        upper_limit = max([float(x) for x in grade['range'].split('-')])
                        lower_limit = max([float(x) for x in grade['range'].split('-')])
                        if upper_limit >= st_total_subject_score <= lower_limit:
                            grading = {'label': grade['label'], 'remark': grade['remark']}
                        
                    term_one_subject_position = str(list(all_term_one_subject_results).index(st_term_one_subject_result) + 1)
                    if str(term_one_subject_position)[-1] == '1':
                        term_one_subject_position += 'st'
                    elif str(term_one_subject_position)[-1] == '2':
                        term_one_subject_position += 'nd'
                    elif str(term_one_subject_position)[-1] == '3':
                        term_one_subject_position += 'rd'
                    else:
                        term_one_subject_position += 'th'
                        
                    term_one_results.append({
                        'subject': subject['name'], 'score': st_term_one_subject_result_data['score'], 'grade': grading, 'position': term_one_subject_position,
                        'assessment_percentage': total_assessment_percentage_term_one, 'assessment_score': total_assessment_score_term_one
                        })
                except ObjectDoesNotExist:
                    pass
                    
                # term two
                total_assessment_score_term_two = 0
                total_assessment_percentage_term_two = 0
                all_term_two_subject_assessments_data = StudentAssessmentSerializer(Assessment.objects.filter(school=school, student=student, subject=st_subject, academic_year=year, academic_term=2), many=True).data
                if len(all_term_two_subject_assessments_data) != 0:
                    for __assessment in all_term_two_subject_assessments_data:
                        total_assessment_score_term_two += float(__assessment['score'])*(float(__assessment['percentage'])/100)
                        total_assessment_percentage_term_two += float(__assessment['percentage'])
                        term_two_assessments.append({'subject': subject['name'], 'score': __assessment['score'], 'title': __assessment['title']})
                        
                all_term_two_subject_results = Exam.objects.filter(school=school, subject=st_subject, student_class=student_class, academic_year=year, academic_term=2).order_by('-score')
                try:
                    st_term_two_subject_result = Exam.objects.get(school=school, subject=st_subject, student=student, academic_year=year, academic_term=2)
                    st_term_two_subject_result_data = StudentExamsSerializer(st_term_two_subject_result).data
                    grading = None
                    st_exams_score = float(st_term_two_subject_result_data['score'])
                    st_total_subject_score = total_assessment_score_term_two + (st_exams_score*((100-total_assessment_percentage_term_two)/100))
                    for grade in  grading_system:
                        upper_limit = max([float(x) for x in grade['range'].split('-')])
                        lower_limit = max([float(x) for x in grade['range'].split('-')])
                        if upper_limit >= st_total_subject_score <= lower_limit:
                            grading = {'label': grade['label'], 'remark': grade['remark']}
                        
                    term_two_subject_position = str(list(all_term_two_subject_results).index(st_term_two_subject_result) + 1)
                    if str(term_two_subject_position)[-1] == '1':
                        term_two_subject_position += 'st'
                    elif str(term_two_subject_position)[-1] == '2':
                        term_two_subject_position += 'nd'
                    elif str(term_two_subject_position)[-1] == '3':
                        term_two_subject_position += 'rd'
                    else:
                        term_two_subject_position += 'th'
                        
                    term_two_results.append({
                        'subject': subject['name'], 'score': st_term_two_subject_result_data['score'], 'grade': grading, 'position': term_two_subject_position,
                        'assessment_percentage': total_assessment_percentage_term_two, 'assessment_score': total_assessment_score_term_two
                        })
                except ObjectDoesNotExist:
                    pass
                
                # term three
                if year_serializer['period_division']['name'] != 'SEMESTER':
                    total_assessment_score_term_three = 0
                    total_assessment_percentage_term_three = 0
                    all_term_three_subject_assessments_data = StudentAssessmentSerializer(Assessment.objects.filter(school=school, student=student, subject=st_subject, academic_year=year, academic_term=1), many=True).data
                    if len(all_term_three_subject_assessments_data) != 0:
                        for __assessment in all_term_three_subject_assessments_data:
                            total_assessment_score_term_three += float(__assessment['score'])*(float(__assessment['percentage'])/100)
                            total_assessment_percentage_term_three += float(__assessment['percentage'])
                            term_three_assessments.append({'subject': subject['name'], 'score': __assessment['score'], 'title': __assessment['title']})
                            
                    all_term_three_subject_results = Exam.objects.filter(school=school, student_class=student_class, subject=st_subject, academic_year=year, academic_term=1).order_by('-score')
                    try:
                        st_term_three_subject_result = Exam.objects.get(school=school, subject=st_subject, student=student, academic_year=year, academic_term=1)
                        st_term_three_subject_result_data = StudentExamsSerializer(st_term_three_subject_result).data
                        grading = None
                        st_exams_score = float(st_term_three_subject_result_data['score'])
                        st_total_subject_score = total_assessment_score_term_three + (st_exams_score*((100-total_assessment_percentage_term_three)/100))
                        for grade in  grading_system:
                            upper_limit = max([float(x) for x in grade['range'].split('-')])
                            lower_limit = max([float(x) for x in grade['range'].split('-')])
                            if upper_limit >= st_total_subject_score <= lower_limit:
                                grading = {'label': grade['label'], 'remark': grade['remark']}
                            
                        term_three_subject_position = str(list(all_term_three_subject_results).index(st_term_three_subject_result) + 1)
                        if str(term_three_subject_position)[-1] == '1':
                            term_three_subject_position += 'st'
                        elif str(term_three_subject_position)[-1] == '2':
                            term_three_subject_position += 'nd'
                        elif str(term_three_subject_position)[-1] == '3':
                            term_three_subject_position += 'rd'
                        else:
                            term_three_subject_position += 'th'
                            
                        term_three_results.append({
                            'subject': subject['name'], 'score': st_term_three_subject_result_data['score'], 'grade': grading, 'position': term_three_subject_position,
                            'assessment_percentage': total_assessment_percentage_term_three, 'assessment_score': total_assessment_score_term_three
                            })
                    except ObjectDoesNotExist:
                        pass
            
            if year_serializer['period_division']['name'] == 'SEMESTER':
                year_data = {
                    'name': year_serializer['name'], 
                    'period_division': year_serializer['period_division']['name'], 
                    'attendance': {'term_one': term_one_attendance, 'term_two': term_two_attendance},
                    'assessments': {'term_one': term_one_assessments, 'term_two': term_two_assessments},
                    'results': {'term_one': term_one_results, 'term_two': term_two_results}
                }
            else:
                year_data = {
                    'name': year_serializer['name'], 
                    'period_division': year_serializer['period_division']['name'], 
                    'attendance': {'term_one': term_one_attendance, 'term_two': term_two_attendance, 'term_three': term_three_attendance},
                    'assessments': {'term_one': term_one_assessments, 'term_two': term_three_assessments, 'term_three': term_three_assessments},
                    'results': {'term_one': term_one_results, 'term_two': term_two_results, 'term_three': term_three_results}
                }
                
            academic_years_data.append(year_data)
            
        for subject in class_data['subjects']:
            subject_data = {'name': subject['name']}
            st_subject = Subject.objects.get(name=subject['name'])
            
            subject_assignment = SubjectAssignment.objects.filter(academic_year=current_academic_year, academic_term=term, students_class=student_class, subjects=st_subject).first()
            if subject_assignment:
                subject_assignment_data = SubjectAssignmentSerializer(subject_assignment).data
                subject_data['teacher'] = f"{ subject_assignment_data['teacher']['user']['first_name']} {subject_assignment_data['teacher']['user']['last_name']}"
                subject_data['teacher_img'] = f"{subject_assignment_data['teacher']['img']}"
                subject_data['teacher_contact'] = f"{subject_assignment_data['teacher']['contact']}"
                subject_data['teacher_email'] = f"{subject_assignment_data['teacher']['user']['email']}"
                subject_data['teacher_gender'] = f"{subject_assignment_data['teacher']['gender']}"
                if subject_assignment_data['teacher']['department']:
                    subject_data['teacher_department'] = f"{subject_assignment_data['teacher']['department']['name']}"
            else:
                subject_data['teacher'] = 'none'
                subject_data['teacher_img'] = 'none'
                subject_data['teacher_contact'] = 'none'
                subject_data['teacher_email'] = 'none'
                subject_data['teacher_gender'] = 'none'
                subject_data['teacher_department'] = 'none'

            student_subjects.append(subject_data)
        
        return Response({
            'subjects': student_subjects, 
            'academic_years_results': academic_years_data, 
            'class_data': {'students': class_data['students'], 'head_teacher': class_data['head_teacher'] if class_data['head_teacher'] else 'none'}
            })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def student_transcript(request):
    file_path = get_student_transcript(request.user.student, request=request)
    return Response(file_path)

