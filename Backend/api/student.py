from api.models import *
from api.serializer import *
from django.db.models import Q

# Django Restframework
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist

from api.utils import get_student_transcript
from collections import defaultdict


# STUDENT
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_student_data(request):
    student = Student.objects.select_related('current_level', 'st_class__head_teacher__user').prefetch_related('academic_years', 'st_class__subjects', 'st_class__students__user').get(user=request.user)
    current_level = student.current_level
    term = int(request.GET.get('term'))
    current_academic_year = AcademicYear.objects.get(id=int(request.GET.get('year')))
    students = []
    head_teacher = None
    class_name = ''
    class_subjects = []
    if student.st_class:
        student_class = student.st_class
        students = student_class.students.all()
        head_teacher = student_class.head_teacher
        class_subjects = student_class.subjects.all()
        class_name = student_class.name
    else:
        student_class = GraduatedClasse.objects.prefetch_related('students__user').get(level=current_level, students=student)
        students = student_class.students.all()
        class_name = student_class.name
    
    attendance_year_term_mapping = defaultdict(lambda: defaultdict(list))
    attendance_objs = StudentAttendance.objects.select_related('academic_year').prefetch_related('students_absent').filter(Q(students_present=student) | Q(students_absent=student), level=current_level).order_by('-date')
    for _attedance_ in attendance_objs:
        year_name = _attedance_.academic_year.name
        term_name = f"{_attedance_.academic_year.period_division} {_attedance_.academic_term}"
        attendance_year_term_mapping[year_name][term_name].append(_attedance_)
    
    assessments_year_term_mapping = defaultdict(lambda: defaultdict(list))
    assessment_objs = Assessment.objects.select_related('academic_year').prefetch_related('subjects').filter(level=current_level, student=student)
    for _assessment_ in assessment_objs:
        year_name = _assessment_.academic_year.name
        term_name = f"{_assessment_.academic_year.period_division} {_assessment_.academic_term}"
        assessments_year_term_mapping[year_name][term_name].append(_assessment_)
    
    exams_year_term_mapping = defaultdict(lambda: defaultdict(list))
    exams_objs = Exam.objects.select_related('academic_year').prefetch_related('subjects').filter(level=current_level, student=student)
    for _exam_ in exams_objs:
        year_name = _exam_.academic_year.name
        term_name = f"{_exam_.academic_year.period_division} {_exam_.academic_term}"
        exams_year_term_mapping[year_name][term_name].append(_exam_)
        
    released_results_year_term_mapping = defaultdict(dict)
    released_results_objs = ReleasedResult.objects.select_related('academic_year').filter(level=current_level, students=student)
    for _released_results_ in released_results_objs:
        year_name = _released_results_.academic_year.name
        term_name = f"{_released_results_.academic_year.period_division} {_released_results_.academic_term}"
        released_results_year_term_mapping[year_name][term_name] = _released_results_
    
    results_year_term_mapping = defaultdict(lambda: defaultdict(list))
    results_objs = StudentResult.objects.select_related('academic_year').prefetch_related('subjects').filter(level=current_level, student=student)
    for _results_ in results_objs:
        year_name = _results_.academic_year.name
        term_name = f"{_results_.academic_year.period_division} {_results_.academic_term}"
        results_year_term_mapping[year_name][term_name].append(_results_)
                
    year_data = defaultdict(dict)
    student_academic_years = student.academic_years.all().order_by('-start_date')
    for year in student_academic_years:
        year_name = year.name
        no_divisions = year.no_divisions
        period_division = year.period_division
        attendance_term_data = {}
        assessments_term_data = {}
        results_term_data = {}
        exams_term_data = {}
        for __term__ in range(no_divisions+1):
            _term = __term__+1
            term_name = f"{period_division} {_term}"
            
            # Attendance
            student_attendance_data = []
            attendance_data_objs = attendance_year_term_mapping[year_name][term_name]
            for __attendance in attendance_data_objs:
                absent_students = __attendance.students_absent.all()
                if student in absent_students:
                    student_attendance_data.append({'date': __attendance.date, 'status': 'ABSENT'})
                else:
                    student_attendance_data.append({'date': __attendance.date, 'status': 'PRESENT'})
            attendance_term_data[term_name] = student_attendance_data
        
            # Assessments
            assessments = AssessmentSerializerOne(assessments_year_term_mapping[year_name][term_name], many=True).data
            assessments_term_data[term_name] = assessments

            # Exams
            exams = ExamSerializerOne(exams_year_term_mapping[year_name][term_name], many=True).data
            exams_term_data[term_name] = exams
            
            # Results
            if released_results_year_term_mapping.get(year_name, {}).get(term_name):
                results_term_data[term_name] = ResultSerializerOne(results_year_term_mapping[year_name][term_name], many=True).data
            else:
                results_term_data[term_name] = []
                
        year_data[year_name]['attendance'] = attendance_term_data
        year_data[year_name]['assessment'] = assessments_term_data
        year_data[year_name]['exam'] = exams_term_data
        year_data[year_name]['result'] = results_term_data
    
    student_subjects = []
    if student.st_class:
        subject_assignment_objs = SubjectAssignment.objects.select_related('teacher__user').prefetch_related('subjects').filter(level=current_level, students_class=student.st_class, academic_year=current_academic_year, academic_term=term)
        for subject in class_subjects:
            subject_data = {'name': subject.name}
            for _assign in subject_assignment_objs:
                if subject in _assign.subjects.all():
                    subject_assignment_teacher_data = StaffSerializerFour(_assign.teacher).data
                    subject_data['teacher'] = subject_assignment_teacher_data['user']
                    subject_data['teacher_img'] = subject_assignment_teacher_data['img']
                    subject_data['teacher_contact'] = subject_assignment_teacher_data['contact']
                    subject_data['teacher_email'] = subject_assignment_teacher_data['email']
                    subject_data['teacher_gender'] = subject_assignment_teacher_data['gender']
                else:    
                    subject_data['teacher'] = ''
                    subject_data['teacher_img'] = ''
                    subject_data['teacher_contact'] = ''
                    subject_data['teacher_email'] = ''
                    subject_data['teacher_gender'] = ''

            student_subjects.append(subject_data)
    
    return Response({
        'subjects': student_subjects,
        'year_data': year_data,
        'class_name': class_name,
        'students': StudentSerializerFour(students, many=True).data, 
        'head_teacher': StaffSerializerFour(head_teacher).data if head_teacher else ''
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def student_transcript(request):
    file_path = get_student_transcript(request.user.student, request=request)
    return Response(file_path)

