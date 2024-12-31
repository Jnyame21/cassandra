# # Django
# from django.db import IntegrityError, transaction


# # Django Restframework
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from api.models import *
# from api.serializer import *
# from api.utils import *
# import json


# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
# def hod_data(request):
#     staff = request.user.staff
#     school = staff.school
    
#     if request.method == 'GET':
#         current_academic_year = AcademicYear.objects.get(school=school, name=request.GET.get('year'))
#         current_term = int(request.GET.get('term'))
#         department = Department.objects.prefetch_related('subjects').get(school=school, teachers=staff)
#         studentClasses = Classe.objects.filter(school=school, subjects__in=department.subjects.all()).distinct()
#         student_classes_data = [x.name for x in studentClasses]
        
#         subject_assignments = SubjectAssignment.objects.select_related('teacher', 'students_class').prefetch_related('subjects').filter(school=school, assigned_by=staff, academic_year=current_academic_year, academic_term=current_term)
#         subject_assignments_data = SubjectAssignmentSerializerOne(subject_assignments, many=True).data
        
#         return Response({
#             'student_classes': student_classes_data,
#             'subject_assignments': subject_assignments_data,
#         })
    


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def hod_subject_assignment(request):
#     staff = request.user.staff
#     school = staff.school
 
#     if request.method == 'POST':
#         current_academic_year = AcademicYear.objects.get(school=school, name=request.data['year'])
#         current_term = int(request.data['term'])
#         students_class = Classe.objects.prefetch_related('subjects').get(school=school, name=request.data['studentsClassName'])
#         teacher = Staff.objects.prefetch_related('subjects').select_related('user').get(school=school, staff_id=request.data['teacher'])
#         if request.data['type'] == 'upload':
#             subjects = json.loads(request.data['subjects'])
#             subjects_obj = Subject.objects.filter(name__in=subjects).distinct()
#             students_class_subjects = students_class.subjects.all()
#             teacher_subjects = teacher.subjects.all()
#             existing_subject_assignments = SubjectAssignment.objects.select_related('teacher__user').prefetch_related('subjects').filter(school=school, students_class=students_class, academic_year=current_academic_year, academic_term=current_term)
#             for _subject in subjects_obj:
#                 if _subject not in teacher_subjects:
#                     return Response({'message': f"{teacher.title} {teacher.user.get_full_name()} doesn't teach {_subject.name}"}, status=400)
#                 elif _subject not in students_class_subjects:
#                     return Response({'message': f"{students_class.name} doesn't study {_subject.name}"}, status=400)
#                 for _assign in existing_subject_assignments:
#                     existing_subject_assignments_subjects = _assign.subjects.all()
#                     if _subject in existing_subject_assignments_subjects:
#                         return Response({'message': f"{_assign.teacher.title} {_assign.teacher.user.get_full_name()} is already teaching the {students_class.name} {_subject.name}"}, status=400)
                    
#             with transaction.atomic():
#                 try:
#                     assignment_obj = SubjectAssignment.objects.create(
#                         school=school,
#                         assigned_by=staff,
#                         students_class=students_class,
#                         teacher=teacher,
#                         academic_year=current_academic_year,
#                         academic_term=current_term,
#                     )
#                     assignment_obj.subjects.set(subjects_obj)
#                     assignment_obj.save()
#                 except IntegrityError:
#                     transaction.set_rollback(True)
#                     return Response({'message': f"{teacher.title} {teacher.user.first_name} {teacher.user.last_name} is already teaching the {students_class.name} class {[_sub.name for _sub in teacher_subjects]}"}, status=400)
#                 except Exception:
#                     transaction.set_rollback(True)
#                     return Response(status=400)
            
#             subject_assignment = SubjectAssignment.objects.get(school=school, assigned_by=staff, students_class=students_class, teacher=teacher, academic_year=current_academic_year, academic_term=current_term)
#             subject_assignments_data = SubjectAssignmentSerializerOne(subject_assignment).data
#             return Response(subject_assignments_data)
        
#         elif request.data['type'] == 'delete':
#             with transaction.atomic():  
#                 try:
#                     existing_exams = Exam.objects.filter(school=school, student_class=students_class, academic_year=current_academic_year, academic_term=current_term).first()
#                     if existing_exams:
#                         return Response({'message': f"{existing_exams.teacher.user.get_full_name()} has already uploaded exams data for students in the selected class [{students_class.name}]. If you still want to delete this subject assignment, please ask him/her to delete the exams data and try again."}, status=400)
#                     existing_assessments = Assessment.objects.select_related('teacher__user').filter(school=school, student_class=students_class, academic_year=current_academic_year, academic_term=current_term).first()
#                     if existing_assessments:
#                         return Response({'message': f"{existing_assessments.teacher.user.get_full_name()} has already uploaded assessment data for students in the selected class [{students_class.name}]. If you still want to delete this subject assignment, please ask him/her to delete them and try again."}, status=400)
                    
#                     assignment_obj = SubjectAssignment.objects.get(
#                         school=school,
#                         assigned_by=staff,
#                         students_class=students_class,
#                         teacher=teacher,
#                         academic_year=current_academic_year,
#                         academic_term=current_term,
#                     )
#                     assignment_obj.delete()
#                 except Exception:
#                     transaction.set_rollback(True)
#                     return Response(status=400)
            
#             return Response()
        
        
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def hod_students_performance(request):
#     staff = request.user.staff
#     department = DepartmentSerializer(Department.objects.get(school=staff.school, teachers=staff)).data
#     academic_year = AcademicYear.objects.get(school=staff.school, name=request.GET.get('year'))

#     data = []
#     if department:
#         for subject in department['subjects']:
#             first_year = {'term_one': [], 'term_two': [], 'term_three': []}
#             second_year = {'term_one': [], 'term_two': [], 'term_three': []}
#             third_year = {'term_one': [], 'term_two': [], 'term_three': []}

#             subject_obj = Subject.objects.get(schools=staff.school, name=subject['name'])

#             # Year One Student Exams
#             result_one_one = ExamsSerializer(
#                 Exam.objects.filter(
#                     school=staff.school,
#                     academic_year=academic_year,
#                     subject=subject_obj,
#                     academic_term=1,
#                     student_year=1,
#                 ),
#                 many=True).data
#             if result_one_one:
#                 for result in result_one_one:
#                     first_year['term_one'].append({
#                         'name': f"{result['student']['user']['first_name']} {result['student']['user']['last_name']}",
#                         'st_id': result['student']['st_id'],
#                         'score': float(result['score']),
#                     })

#                 first_year['term_one'] = sorted(first_year['term_one'], key=lambda x: x['score'], reverse=True)

#             result_one_two = ExamsSerializer(
#                 Exam.objects.filter(
#                     school=staff.school,
#                     academic_year=academic_year,
#                     subject=subject_obj,
#                     academic_term=2,
#                     student_year=1,
#                 ),
#                 many=True).data
#             if result_one_two:
#                 for result in result_one_two:
#                     first_year['term_two'].append({
#                         'name': f"{result['student']['user']['first_name']} {result['student']['user']['last_name']}",
#                         'st_id': result['student']['st_id'],
#                         'score': float(result['score']),
#                     })

#                 first_year['term_two'] = sorted(first_year['term_two'], key=lambda x: x['score'], reverse=True)

#             result_one_three = ExamsSerializer(
#                 Exam.objects.filter(
#                     school=staff.school,
#                     academic_year=academic_year,
#                     subject=subject_obj,
#                     academic_term=3,
#                     student_year=1,
#                 ),
#                 many=True).data
#             if result_one_three:
#                 for result in result_one_three:
#                     first_year['term_three'].append({
#                         'name': f"{result['student']['user']['first_name']} {result['student']['user']['last_name']}",
#                         'st_id': result['student']['st_id'],
#                         'score': float(result['score']),
#                     })

#                 first_year['term_three'] = sorted(first_year['term_three'], key=lambda x: x['score'], reverse=True)

#             # Year Two Students Exams
#             result_two_one = ExamsSerializer(
#                 Exam.objects.filter(
#                     school=staff.school,
#                     academic_year=academic_year,
#                     subject=subject_obj,
#                     academic_term=1,
#                     student_year=2,
#                 ),
#                 many=True).data
#             if result_two_one:
#                 for result in result_two_one:
#                     second_year['term_one'].append({
#                         'name': f"{result['student']['user']['first_name']} {result['student']['user']['last_name']}",
#                         'st_id': result['student']['st_id'],
#                         'score': float(result['score']),
#                     })

#                 second_year['term_one'] = sorted(second_year['term_one'], key=lambda x: x['score'], reverse=True)

#             result_two_two = ExamsSerializer(
#                 Exam.objects.filter(
#                     school=staff.school,
#                     academic_year=academic_year,
#                     subject=subject_obj,
#                     academic_term=2,
#                     student_year=2,
#                 ),
#                 many=True).data
#             if result_two_two:
#                 for result in result_two_two:
#                     second_year['term_two'].append({
#                         'name': f"{result['student']['user']['first_name']} {result['student']['user']['last_name']}",
#                         'st_id': result['student']['st_id'],
#                         'score': float(result['score']),
#                     })

#                 second_year['term_two'] = sorted(second_year['term_two'], key=lambda x: x['score'], reverse=True)

#             result_two_three = ExamsSerializer(
#                 Exam.objects.filter(
#                     school=staff.school,
#                     academic_year=academic_year,
#                     subject=subject_obj,
#                     academic_term=3,
#                     student_year=2,
#                 ),
#                 many=True).data
#             if result_two_three:
#                 for result in result_two_three:
#                     second_year['term_three'].append({
#                         'name': f"{result['student']['user']['first_name']} {result['student']['user']['last_name']}",
#                         'st_id': result['student']['st_id'],
#                         'score': float(result['score']),
#                     })

#                 second_year['term_three'] = sorted(second_year['term_three'], key=lambda x: x['score'], reverse=True)

#             # Year Three Students Exams
#             result_three_one = ExamsSerializer(
#                 Exam.objects.filter(
#                     school=staff.school,
#                     academic_year=academic_year,
#                     subject=subject_obj,
#                     academic_term=1,
#                     student_year=3,
#                 ),
#                 many=True).data
#             if result_three_one:
#                 for result in result_three_one:
#                     third_year['term_one'].append({
#                         'name': f"{result['student']['user']['first_name']} {result['student']['user']['last_name']}",
#                         'st_id': result['student']['st_id'],
#                         'score': float(result['score']),
#                     })

#                 third_year['term_one'] = sorted(third_year['term_one'], key=lambda x: x['score'],
#                                                 reverse=True)

#             result_three_two = ExamsSerializer(
#                 Exam.objects.filter(
#                     school=staff.school,
#                     academic_year=academic_year,
#                     subject=subject_obj,
#                     academic_term=2,
#                     student_year=3,
#                 ),
#                 many=True).data
#             if result_three_two:
#                 for result in result_three_two:
#                     third_year['term_two'].append({
#                         'name': f"{result['student']['user']['first_name']} {result['student']['user']['last_name']}",
#                         'st_id': result['student']['st_id'],
#                         'score': float(result['score']),
#                     })

#                 third_year['term_two'] = sorted(third_year['term_two'], key=lambda x: x['score'],
#                                                 reverse=True)

#             result_three_three = ExamsSerializer(
#                 Exam.objects.filter(
#                     school=staff.school,
#                     academic_year=academic_year,
#                     subject=subject_obj,
#                     academic_term=3,
#                     student_year=3,
#                 ),
#                 many=True).data
#             if result_three_three:
#                 for result in result_three_three:
#                     third_year['term_three'].append({
#                         'name': f"{result['student']['user']['first_name']} {result['student']['user']['last_name']}",
#                         'st_id': result['student']['st_id'],
#                         'score': float(result['score']),
#                     })

#                 third_year['term_three'] = sorted(third_year['term_three'], key=lambda x: x['score'],
#                                                   reverse=True)

#             data.append({
#                 'subject': subject['name'],
#                 'year_one': first_year,
#                 'year_two': second_year,
#                 'year_three': third_year,
#             })

#         return Response(data)

#     else:
#         return Response(status=401)