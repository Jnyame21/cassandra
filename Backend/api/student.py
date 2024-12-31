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
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_student_data(request):
    student = request.user.student
    level = student.level
    if request.method == 'GET':
        term = request.GET.get('term')
        current_academic_year = AcademicYear.objects.get(level=level, name=request.GET.get('year'))
        students = []
        student_subjects = []
        head_teacher = None
        class_subjects = []
        if student.has_completed:
            student_class = GraduatedClasse.objects.prefetch_related('students__user').get(level=level, students=student).student
            students = student_class.students.all()
        else:
            student_class = Classe.objects.select_related('head_teacher__user').prefetch_related('students__user', 'subjects').get(level=level, students=student)
            students = student_class.students.all()
            head_teacher = student_class.head_teacher
            class_subjects = student_class.subjects.all()
        
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
                attendances = StudentAttendance.objects.prefetch_related('students_absent').filter(level=level, academic_year=year, academic_term=_term).filter(Q(students_present=student) | Q(students_absent=student)).order_by('-date')
                for __attendance in attendances:
                    if student in __attendance.students_absent.all():
                        student_attendance_data.append({'date': __attendance.date, 'status': 'ABSENT'})
                    else:
                        student_attendance_data.append({'date': __attendance.date, 'status': 'PRESENT'})
                attendance_term_data[term_name] = student_attendance_data
            
                # Assessments
                assessments = AssessmentSerializerOne(Assessment.objects.filter(level=level, student=student, academic_year=year, academic_term=_term), many=True).data
                assessments_term_data[term_name] = assessments

                # Exams
                exams = ExamSerializerOne(Exam.objects.filter(level=level, student=student, academic_year=year, academic_term=_term), many=True).data
                exams_term_data[term_name] = exams
                
                # Results
                results = ResultSerializerOne(StudentResult.object.filter(level=level, student=student, academic_year=year, academic_term=_term), many=True).data
                if results and results[0]['released']:
                    results_term_data[term_name] = results
                else:
                    results_term_data[term_name] = []
                    
            year_data[year_name]['attendance'] = attendance_term_data
            year_data[year_name]['assessment'] = assessments_term_data
            year_data[year_name]['exam'] = exams_term_data
            year_data[year_name]['result'] = results_term_data
            
        for subject in class_subjects:
            subject_data = {'name': subject.name}
            try:
                subject_assignment = SubjectAssignment.objects.select_related('teacher__user', 'teacher__department').get(academic_year=current_academic_year, academic_term=term, students_class=student_class, subjects=subject)
                subject_assignment_teacher_data = StaffSerializerFour(subject_assignment.teacher).data
                subject_data['teacher'] = subject_assignment_teacher_data['user']
                subject_data['teacher_img'] = subject_assignment_teacher_data['img']
                subject_data['teacher_contact'] = subject_assignment_teacher_data['contact']
                subject_data['teacher_email'] = subject_assignment_teacher_data['email']
                subject_data['teacher_gender'] = subject_assignment_teacher_data['gender']
                if subject_assignment.teacher.department:
                    subject_data['teacher_department'] = subject_assignment.teacher.department.name
                else:
                   subject_data['teacher_department'] = ''
                    
            except SubjectAssignment.DoesNotExist:
                subject_data['teacher'] = ''
                subject_data['teacher_img'] = ''
                subject_data['teacher_contact'] = ''
                subject_data['teacher_email'] = ''
                subject_data['teacher_gender'] = ''
                subject_data['teacher_department'] = ''

            student_subjects.append(subject_data)
        
        return Response({
            'subjects': student_subjects,
            'year_data': year_data,
            'students': StudentSerializerFour(students, many=True).data, 
            'head_teacher': StaffSerializerFour(head_teacher).data if head_teacher else ''
        })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def student_transcript(request):
    file_path = get_student_transcript(request.user.student, request=request)
    return Response(file_path)

