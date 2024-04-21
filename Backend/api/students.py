from api.models import *
from api.serializer import *

# Django Restframework
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api.utils import get_student_transcript


# STUDENT
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_student_data(request):
    school = request.user.student.school
    if request.method == 'GET':
        academic_year = AcademicYear.objects.get(school=school, name=request.GET.get('year'))
        term = request.GET.get('term')
        student = request.user.student
        if AcademicYearSerializer(academic_year).data not in AcademicYearSerializer(student.st_class.academic_years.all(), many=True).data:
            years = AcademicYearSerializer(student.st_class.academic_years, many=True).data
            if len(years) == 1:
                academic_year = AcademicYear.objects.get(school=school, name=years[0]['name'])
            elif len(years) > 1:
                years = sorted(years, key=lambda x: x['start_date'])
                academic_year = AcademicYear.objects.get(school=school, name=years[-1]['name'])

        student_class = Classe.objects.get(students=student)

        results_term_one = StudentResultsSerializer(
            Result.objects.filter(academic_year=academic_year, student=student, academic_term=1), many=True).data
        results_term_two = StudentResultsSerializer(
            Result.objects.filter(academic_year=academic_year, student=student, academic_term=2), many=True).data
        results_term_three = StudentResultsSerializer(
            Result.objects.filter(academic_year=academic_year, student=student, academic_term=3), many=True).data

        student_results = {'term_one': results_term_one, 'term_two': results_term_two, 'term_three': results_term_three}

        class_data = ClasseWithSubjectsSerializer(student_class).data
        student_subjects = []
        for subject in class_data['subjects']:
            subject_data = {'name': subject['name']}
            st_subject = Subject.objects.get(name=subject['name'])
            subject_assignment = SubjectAssignment.objects.filter(academic_year=academic_year, academic_term=term,
                                                                students_class=student_class, subject=st_subject).first()
            if subject_assignment:
                subject_assignment_data = SubjectAssignmentSerializer(subject_assignment).data
                subject_data['teacher'] = f"{ subject_assignment_data['teacher']['user']['first_name']} {subject_assignment_data['teacher']['user']['last_name']}"
                subject_data['teacher_img'] = f"{subject_assignment_data['teacher']['img']}"
                subject_data['teacher_contact'] = f"{subject_assignment_data['teacher']['contact']}"
                subject_data['teacher_email'] = f"{subject_assignment_data['teacher']['user']['email']}"
                subject_data['teacher_gender'] = f"{subject_assignment_data['teacher']['gender']}"
                subject_data['teacher_department'] = f"{subject_assignment_data['teacher']['department']['name']}"

            else:
                subject_data['teacher'] = 'null'
                subject_data['teacher_img'] = 'null'
                subject_data['teacher_contact'] = 'null'
                subject_data['teacher_email'] = 'null'
                subject_data['teacher_gender'] = 'null'
                subject_data['teacher_department'] = 'null'

            student_subjects.append(subject_data)
        if len(class_data['academic_years']) > 1:
            return Response({'subjects': student_subjects, 'results': student_results,
                             'academic_years': sorted(class_data['academic_years'], key=lambda x: x['start_date'], reverse=True),
                             'class_data': class_data['students']
                             })
        else:
            return Response({'subjects': student_subjects, 'results': student_results, 'class_data': class_data['students']})

    else:
        academic_year = AcademicYear.objects.get(school=school, name=request.data['year'])
        student = request.user.student

        results_term_one = StudentResultsSerializer(
            Result.objects.filter(academic_year=academic_year, student=student, academic_term=1), many=True).data
        results_term_two = StudentResultsSerializer(
            Result.objects.filter(academic_year=academic_year, student=student, academic_term=2), many=True).data
        results_term_three = StudentResultsSerializer(
            Result.objects.filter(academic_year=academic_year, student=student, academic_term=3), many=True).data

        return Response({'term_one': results_term_one, 'term_two': results_term_two, 'term_three': results_term_three})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def student_transcript(request):
    file_path = get_student_transcript(request.user.student, request=request)
    return Response(file_path)