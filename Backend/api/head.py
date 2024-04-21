
# Django Restframework
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Other
from api.models import *
from api.serializer import *
from api.utils import *
from functools import partial
from timeit import timeit


# HEAD
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_head_data(request):
    head = request.user.head
    data = []
    academic_year = AcademicYear.objects.get(school=head.school, name=request.GET.get('year'))
    departments = DepartmentSerializer(Department.objects.filter(school=head.school), many=True).data
    all_subject_assignments = SubjectAssignmentWithoutStudentsSerializer(SubjectAssignment.objects.filter(school=head.school, academic_year=academic_year), many=True).data

    for department in departments:
        subject_assignments = {}
        for term in range(1, 4):
            term_name = 'one' if term==1 else ('two' if term==2 else 'three')
            subject_assignments[f'term_{term_name}'] = [x for x in all_subject_assignments if x['academic_term'] == term]

        data.append({
            'department': department,
            'subject_assignments': subject_assignments,
        })

    programs = []

    sch_programs = ProgramSerializer(Program.objects.filter(schools=head.school), many=True).data
    classes = ClasseSerializer(Classe.objects.filter(school=head.school, is_active=True).order_by('students_year'), many=True).data
    for program in sch_programs:
        program_data = {'name': program['name'],
            'classes': [x for x in classes if program['name'] == x['program']['name']]
        }
        programs.append(program_data)
        
    response_data = {
        'departments': data,
        'programs': programs,
    }

    return Response(response_data)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def head_students_performance(request):
    head = request.user.head
    departments = SpecificDepartmentSerializer(Department.objects.filter(school=head.school).prefetch_related("subjects"), many=True).data
    if not departments:
        return Response(status=401)
    
    academic_year = AcademicYear.objects.get(school=head.school, name=request.GET.get('year'))
    all_results = ResultsSerializerWithoutStudentTeacher(Result.objects.filter(school=head.school, academic_year=academic_year).order_by('-score'), many=True).data
    
    data = []
    for department in departments:
        subjects = []
        
        for subject in department['subjects']:
            
            year_1 = {}
            year_2 = {}
            year_3 = {}
            
            for year in range(1, 4):
                for term in range(1, 4):
                    term_name = 'one' if term==1 else('two' if term==2 else 'three')
                    if year == 1:
                        year_1[f"term_{term_name}"] = [x['score'] for x in all_results if x['subject']['name'] == subject['name'] and x['student_year'] == year and x['academic_term'] == term]
                    elif year == 2:
                        year_2[f"term_{term_name}"] = [x['score'] for x in all_results if x['subject']['name'] == subject['name'] and x['student_year'] == year and x['academic_term'] == term]
                    elif year == 3:
                        year_3[f"term_{term_name}"] = [x['score'] for x in all_results if x['subject']['name'] == subject['name'] and x['student_year'] == year and x['academic_term'] == term]
                
            subjects.append({'name': subject['name'], 'year_one': year_1, 'year_two': year_2, 'year_three': year_3})

        data.append({
            'department': department['name'],
            'subjects': subjects,
        })

    return Response(data)

    
    
    