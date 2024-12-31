# Django
from django.db import IntegrityError, transaction
from django.core.files.storage import default_storage

# Document Manipulation
import pandas as pd
from openpyxl.styles import Font, Alignment, Protection
from openpyxl import Workbook, load_workbook

# Django Restframework
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from api.models import *
from api.serializer import *
from api.utils import *
import json
from collections import defaultdict
from datetime import datetime
import hashlib
import math
from decimal import Decimal
import time

# TEACHER
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_teacher_data(request):
    start = time.time()
    teacher = request.user.staff
    school = teacher.school
    current_level = teacher.current_level
    end = time.time()
    print(f"time taken: {end - start}")
    current_term = int(request.GET.get('term'))
    current_academic_year = AcademicYear.objects.get(school=school, level=current_level, name=request.GET.get('year'))
    department_data = None
    staff = StaffSerializerTwo(Staff.objects.filter(school=school, is_active=True), many=True).data
    subject_assignments = SubjectAssignment.objects.prefetch_related('subjects', 'students_class__students').filter(school=school, level=current_level, teacher=teacher, academic_year=current_academic_year, academic_term=current_term)
    subject_assignments_data = SubjectAssignmentSerializerTwo(subject_assignments, many=True).data
    all_assignments = {}
    for _assignment in subject_assignments_data:
        all_assignments[_assignment['students_class']['name']] = _assignment
        
    department = Department.objects.filter(school=school, level=current_level, teachers=teacher).first()
    if department:
        department_data = DepartmentNameSubjectsSerializer(department).data
    
    head_classes = Classe.objects.prefetch_related('students').filter(school=school, level=current_level, head_teacher=teacher).order_by('name')
    atttendance_data = defaultdict(dict)
    if head_classes.exists():
        for _class in head_classes:
            students_class_name = _class.name
            students = StudentUserIdSerializer(_class.students.all())
            attendance_instances = StudentAttendance.objects.filter(school=school, level=current_level, students_class=_class, academic_year=current_academic_year, academic_term=current_term).order_by('-date')
            attendances = StudentsAttendanceSerializer(attendance_instances, many=True).data
            atttendance_data[students_class_name]['students'] = students
            atttendance_data[students_class_name]['attendances'] = attendances
            
    return Response({
        'subject_assignments': all_assignments,
        'department_data': department_data,
        'staff': staff,
        'students_attendance': atttendance_data
    })
    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def teacher_students_attendance(request):
    teacher = request.user.staff.select_related('school', 'current_level')
    school = teacher.school
    current_level = teacher.current_level
    
    if request.method == 'POST':
        data = request.data
        students_class = Classe.objects.prefetch_related('students').get(school=school, level=current_level, name=data['className'])
        current_academic_year = AcademicYear.objects.get(school=school, level=current_level, name=data['year'])
        current_term = int(data['term'])
        if data['type'] == 'create':
            students = data['absentStudents'].split(',')
            try:
                existing_attendance = StudentAttendance.objects.get(
                    school=school,
                    level=teacher.level,
                    date=data['date'],
                    teacher=teacher,
                    students_class=students_class,
                    academic_year=current_academic_year,
                    academic_term=current_term,
                )
                return Response({
                    'message': f"You have already uploaded attendance for this date [ {data['date']} ]",
                }, status=400)

            except StudentAttendance.DoesNotExist:
                with transaction.atomic():
                    attendance = StudentAttendance.objects.create(
                        school=school,
                        level=teacher.level,
                        teacher=teacher,
                        date=data['date'],
                        students_class=students_class,
                        academic_year=current_academic_year,
                        academic_term=int(data['term']),
                    )
                        
                    for st in students_class.students.all():
                        if st.st_id not in students:
                            attendance.students_present.add(st)
                        else:
                            attendance.students_absent.add(st)

                    attendance.save()

                new_attendance = StudentsAttendanceSerializer(StudentAttendance.objects.get(
                    school=school,
                    level=teacher.level,
                    academic_year=current_academic_year,
                    academic_term=current_term,
                    date=data['date'],
                    students_class=students_class,
                    teacher=teacher
                )).data

                return Response(new_attendance)

        elif data['type'] == 'delete':
            try:
                students_class = Classe.objects.get(school=school, level=teacher.level, name=data['className'])
                with transaction.atomic():
                    student_attendance = StudentAttendance.objects.get(
                        school=school,
                        level=current_level,
                        academic_year=current_academic_year,
                        academic_term=current_term,
                        students_class=students_class,
                        teacher=teacher,
                        date=data['date'],
                    )
                    student_attendance.delete()

                return Response()

            except StudentAttendance.DoesNotExist:
                return Response(status=400)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def teacher_assessments(request):
    teacher = request.user.staff.select_related('school', 'current_level')
    school = teacher.school
    current_level = teacher.current_level
    
    if request.method == 'GET':
        current_term = int(request.GET.get('term'))
        current_academic_year = AcademicYear.objects.get(school=school, level=current_level, name=request.GET.get('year'))
        all_assessments_data = {}
            
        subject_assignments = list(SubjectAssignment.objects.select_related('teacher', 'students_class').prefetch_related('subjects').filter(school=school, level=current_level, teacher=teacher, academic_year=current_academic_year, academic_term=current_term))
        for assign in subject_assignments:
            all_students = assign.students_class.students.all()
            students_class_name = assign.students_class.name
            assessment_class_data = {}
            for _subject in assign.subjects.all():
                assessment_subject_name = _subject.name
                assessment_subject_data = {}
                all_assessments = list(Assessment.objects.select_related('student').filter(school=school, level=current_level, teacher=teacher, subject=_subject, student_class=assign.students_class, academic_year=current_academic_year, academic_term=current_term))
                assessment_titles = list(set([x.title for x in all_assessments]))
                for _title in assessment_titles:
                    assessment_with_title = Assessment.objects.select_related('student').filter(school=school, level=current_level, teacher=teacher, subject=_subject, title=_title, student_class=assign.students_class, academic_year=current_academic_year, academic_term=current_term).order_by('-score')
                    first_assessment = assessment_with_title[0]
                    assessment_title_data = {'title': _title, 'total_score': first_assessment.total_score, 'description': first_assessment.description, 'percentage': first_assessment.percentage, 'assessment_date': first_assessment.assessment_date, 'students_with_assessment': {}, 'students_without_assessment': {}}
                    students_with_assessments = set()
                    for _assessment in assessment_with_title:
                        if _assessment.student:
                            st_id = _assessment.student.st_id
                            students_with_assessments.add(_assessment.student)
                            st_data = {
                                'name': f"{_assessment.student.user.first_name} {_assessment.student.user.last_name}",
                                'st_id': st_id,
                                'score': _assessment.score,
                                'comment': _assessment.comment,
                            }
                            assessment_title_data['students_with_assessment'][st_id] = st_data
                    for _student in all_students:
                        st_id = _student.st_id
                        if _student.st_id not in students_with_assessments:
                            st_data = {
                                'name': f"{_student.user.first_name} {_student.user.last_name}",
                                'st_id': st_id,
                            }
                            assessment_title_data['students_without_assessment'][st_id] = st_data
                    assessment_subject_data[_title] = assessment_title_data
                assessment_class_data[assessment_subject_name] = assessment_subject_data
            all_assessments_data[students_class_name] = assessment_class_data
            
        return Response({
            'assessments': all_assessments_data
        })
    
    elif request.method == 'POST':
        year = request.data['year']
        term = int(request.data['term'])
        subject_name = request.data['subject']
        st_class_name = request.data['studentsClassName']
        current_academic_year = AcademicYear.objects.select_related('period_division').get(school=school, level=current_level, name=year)
        assessment_title = request.data['title']
        if request.data['type'] == 'getFile':
            students = json.loads(request.data['selectedStudents'])
            total_score = request.data['totalScore']
            if current_level.students_id:
                data = [
                    ['STUDENT NAME', 'STUDENT ID', 'SCORE', 'COMMENT']
                ]
            else:
                data = [
                    ['STUDENT NAME', 'STUDENT USERNAME', 'SCORE', 'COMMENT']
                ]

            if len(students) == 0:
                return Response({
                    'message': f"You have already uploaded all the {subject_name}[{assessment_title}] Assessment scores for all students in this class",
                }, status=400)
                
            subject_obj = Subject.objects.get(name=subject_name)
            for _st in students:
                row = [_st['name'], _st['st_id'], '']
                data.append(row)

            wb = Workbook()
            ws = wb.active
            ws.title = subject_name

            ws.merge_cells('A1:I3')
            ws['A1'].value = f"SUBJECT: [{subject_name}]  ACADEMIC YEAR: [{year}]  CLASS: [{st_class_name}]  {current_academic_year.period_division.name}: [{term}]  ASSESSMENT: [{assessment_title}]"
            ws['A1'].font = Font(size=14, bold=True)
            ws['A1'].alignment = Alignment(horizontal='center', vertical='center')

            count = 0
            container = ws['B5:E200']
            while count < len(data):
                for row_ws, row_data in zip(container, data):
                    for cell, item in zip(row_ws, row_data):
                        cell.value = item

                count += 1

            ws.column_dimensions['A'].width = 20
            ws.column_dimensions['B'].width = 50
            ws.column_dimensions['C'].width = 25
            ws.column_dimensions['D'].width = 15
            ws.column_dimensions['E'].width = 50

            for row in ws['A3:F200']:
                for cell in row:
                    cell.font = Font(size=14)
                    cell.alignment = Alignment(horizontal='center', vertical='center')

            for row in ws['B3:B200']:
                for cell in row:
                    cell.alignment = Alignment(horizontal='left', vertical='center')

            for cells in ws['A5:F200'][0]:
                cells.font = Font(bold=True, size=14)

            ws.protection.sheet = True
            for cell in ws.iter_rows(min_row=6, max_row=ws.max_row, min_col=4, max_col=4):
                cell[0].protection = Protection(locked=False)
            for cell in ws.iter_rows(min_row=6, max_row=ws.max_row, min_col=5, max_col=5):
                cell[0].protection = Protection(locked=False)

            ws.protection.password = 'teamjn'

            filename = f"{subject_name.replace(' ', '-')}-{st_class_name}-{assessment_title}.xlsx"
            byte_file = io.BytesIO()
            wb.save(byte_file)
            file_path = f"{get_school_folder(school)}/staff/{teacher.user.username}/{filename}"
            if default_storage.exists(file_path):
                default_storage.delete(file_path)

            saved_file = default_storage.save(file_path, byte_file)
            if settings.DEBUG:
                return Response({
                    'filename': filename,
                    'message': 'File generated successfully',
                    'file_path': f"http://localhost:8000{default_storage.url(saved_file)}",
                })
            else:
                return Response({
                    'filename': filename,
                    'message': 'File generated successfully',
                    'file_path': default_storage.url(saved_file),
                })

        elif request.data['type'] == 'createAssessment':
            students_class = Classe.objects.get(school=school, level=current_level, name=st_class_name)
            subject_obj = Subject.objects.get(name=subject_name)
            description = request.data['description']
            total_score = float(request.data['totalScore'])
            assessment_date = request.data['date']
            assessment_date_object = datetime.strptime(assessment_date, '%Y-%m-%d').date()
            existing_results = StudentResult.objects.filter(school=school, level=current_level, teacher=teacher, subject=subject_obj, student_class=students_class, academic_year=current_academic_year, academic_term=term).exists()
            if existing_results:
                return Response({'message': f"Results for {subject_name} in this class have already been generated. Please delete the existing results data and try again."}, status=400)
            if total_score <= 0:
                return Response({'message': f"The total score of the assessment cannot be negative or zero(0)"}, status=400)
            if (assessment_date_object > current_academic_year.end_date) or (assessment_date_object < current_academic_year.start_date):
                return Response({'message': f"The assessment date must be between the academic year start and end dates. That's {current_academic_year.start_date} and {current_academic_year.end_date}"}, status=400)
            if Assessment.objects.filter(school=school, level=current_level, teacher=teacher, subject=subject_obj, student_class=students_class, title=assessment_title, academic_year=current_academic_year, academic_term=term).exists():
                return Response({'message': f"An assessment with the title '{assessment_title}' already exists. Please use a different title."}, status=400)
            
            with transaction.atomic():
                assessment_obj = Assessment.objects.create(
                    school=school, 
                    level=current_level, 
                    teacher=teacher, 
                    subject=subject_obj, 
                    student_class=students_class,
                    title=assessment_title,
                    description=description,
                    total_score=float(total_score),
                    assessment_date=assessment_date,
                    academic_year=current_academic_year, 
                    academic_term=term
                )
                try:
                    assessment_obj.save()
                except Exception:
                    return Response(status=400) 
            
            return Response({'message': "Operation successful"})
            
        elif request.data['type'] == 'uploadWithFile':
            file = request.data['file']
            subject_obj = Subject.objects.get(name=subject_name)
            old_assessment = Assessment.objects.filter(school=school, level=current_level, teacher=teacher, subject=subject_obj, title=assessment_title, academic_year=current_academic_year, academic_term=term).first()
            description = old_assessment.description
            total_score = old_assessment.total_score
            percentage = old_assessment.percentage
            assessment_date = old_assessment.assessment_date
                
            try:
                wb = load_workbook(file)
            except Exception:
                return Response({'message': "Invalid file. Ensure you upload the excel file that you generated"}, status=400)
            
            ws = wb.active
            ws.protection = False
            if ws['A1'].value != f"SUBJECT: [{subject_name}]  ACADEMIC YEAR: [{year}]  CLASS: [{st_class_name}]  {current_academic_year.period_division.name}: [{term}]  ASSESSMENT: [{assessment_title}]":
                return Response({'message': "Invalid file. Ensure you upload the same excel file that you got"}, status=400)
            
            cleaned_data = []
            for row in ws.iter_rows(min_row=6, max_row=ws.max_row, min_col=2, max_col=5):
                data = []
                for cell in row:
                    data.append(cell.value)
                cleaned_data.append(data)
            
            if len(cleaned_data) == 0:
                return Response({'message': f"There are no students data in the uploaded file"}, status=400)

            valid_rows = [x for x in cleaned_data if x[0] and x[1]]
            for row in valid_rows:
                score = row[2]
                try:
                    float(score)
                except Exception:
                    return Response({'message': f"The scores must be a number. Recheck the score for {row[0]}[{row[1]}] in the file"}, status=400)
                
                if score > total_score:
                    print(total_score)
                    return Response({'message': f"Scores cannot exceed the total score for the assessment. Recheck the score for {row[0]}[{row[1]}] in the file"}, status=400)
                elif score < 0:
                    return Response({'message': f"Scores cannot be negative. Recheck the score for {row[0]}[{row[1]}] in the file"}, status=400)

            students_class = Classe.objects.prefetch_related('students').get(school=school, level=current_level, name=st_class_name)
            assessment_students = []
            with transaction.atomic():
                assessments_to_create = []
                for _student in valid_rows:
                    if students_class.students.filter(school=school, level=current_level, st_id=_student[1]).exists():
                        student = Student.objects.get(school=school, level=current_level, st_id=_student[1])
                        assessment_students.append(student)
                        st_assessment = Assessment(
                            school=school,
                            student=student,
                            subject=subject_obj,
                            teacher=teacher,
                            student_class=students_class,
                            score=float(_student[2]),
                            academic_year=current_academic_year,
                            title=assessment_title,
                            description=description,
                            percentage=percentage,
                            total_score=total_score,
                            comment=_student[3] if _student[3] else '',
                            academic_term=term,
                            level=current_level,
                            assessment_date=assessment_date,
                        )
                        assessments_to_create.append(st_assessment)
                    else:
                        transaction.set_rollback(True)
                        return Response({'message': f"Invalid student {_student[0]}[{_student[1]}]. Make sure you don't change anything in the excel file except the scores and comments"}, status=400)
                try:
                    Assessment.objects.bulk_create(assessments_to_create)
                    assessment_to_delete = Assessment.objects.get(school=school, level=current_level, teacher=teacher, student=None, student_class=students_class, subject=subject_obj, title=assessment_title, academic_year=current_academic_year, academic_term=term)
                    assessment_to_delete.delete()
                except Assessment.DoesNotExist:
                    transaction.set_rollback(False)
                except IntegrityError:
                    transaction.set_rollback(True)
                    return Response({'message': f"You have already uploaded Assessment for some of the students in the file. Click on get file to get a new updated file"}, status=400)
                except Exception:
                    transaction.set_rollback(True)
                    return Response({'message': f"An unexpected error occurred! Ensure you don't delete or change anything in the excel file except the scores and comments"}, status=400)
            
            assessments = Assessment.objects.select_related('student__user').filter(school=school, level=current_level, teacher=teacher, subject=subject_obj, title=assessment_title, student__in=assessment_students, academic_year=current_academic_year, academic_term=term)
            students_data = [{
                'name': f"{_assessment.student.user.first_name} {_assessment.student.user.last_name}", 
                'st_id': _assessment.student.st_id,
                'score': _assessment.score,
                'comment': _assessment.comment,
            } for _assessment in assessments]
            return Response({'message': "Operation successful!", 'data': students_data})

        elif request.data['type'] == 'uploadWithoutFile':
            students_class = Classe.objects.get(school=school, level=current_level, name=st_class_name)
            subject_obj = Subject.objects.get(name=subject_name)
            assessment_students = []
            student_ids = json.loads(request.data['selectedStudents'])
            comment = request.data['comment']
            old_assessment = Assessment.objects.filter(school=school, level=current_level, teacher=teacher, student_class=students_class, subject=subject_obj, title=assessment_title, academic_year=current_academic_year, academic_term=term).first()
            description = old_assessment.description
            total_score = old_assessment.total_score
            percentage = old_assessment.percentage
            assessment_date = old_assessment.assessment_date
            
            score = float(request.data['score'])
            if score > total_score:
                return Response({'message': f"The student(s) score cannot exceed the total score for the assessment!"}, status=400)
            
            with transaction.atomic():
                assessments_to_create = []
                for _st_id in student_ids:
                    student = Student.objects.get(school=school, level=current_level, st_id=_st_id)
                    assessment_students.append(student)
                    st_assessment = Assessment(
                        school=school,
                        student=student,
                        subject=subject_obj,
                        teacher=teacher,
                        student_class=students_class,
                        score=score,
                        academic_year=current_academic_year,
                        title=assessment_title,
                        description=description,
                        percentage=percentage,
                        total_score=total_score,
                        comment=comment,
                        academic_term=term,
                        level=current_level,
                        assessment_date=assessment_date,
                    )
                    assessments_to_create.append(st_assessment)
                
                try:
                    Assessment.objects.bulk_create(assessments_to_create)
                    assessment_to_delete = Assessment.objects.get(school=school, level=current_level, teacher=teacher, student=None, student_class=students_class, subject=subject_obj, title=assessment_title, academic_year=current_academic_year, academic_term=term)
                    assessment_to_delete.delete()
                except Assessment.DoesNotExist:
                    transaction.set_rollback(False)
                except Exception:
                    transaction.set_rollback(True)
                    return Response(status=400)
            
            assessments = Assessment.objects.select_related('student__user').filter(school=school, level=current_level, teacher=teacher, subject=subject_obj, title=assessment_title, student__in=assessment_students, academic_year=current_academic_year, academic_term=term)
            students_data = [{
                'name': f"{_assessment.student.user.first_name} {_assessment.student.user.last_name}", 
                'st_id': _assessment.student.st_id,
                'score': _assessment.score,
                'comment': _assessment.comment,
            } for _assessment in assessments]
            return Response({'message': "Operation successful!", 'data': students_data})

        elif request.data['type'] == 'editAssessment':
            students_class = Classe.objects.get(school=school, level=current_level, name=st_class_name)
            subject_obj = Subject.objects.get(name=subject_name)
            if (request.data['editType'] == 'title'):
                with transaction.atomic():
                    assessments_to_update = []
                    old_title = assessment_title
                    new_title = request.data['newTitle']
                    if Assessment.objects.filter(school=school, level=current_level, teacher=teacher, subject=subject_obj, student_class=students_class, title=new_title, academic_year=current_academic_year, academic_term=term).exists():
                        return Response({'message': f"Assessment with title [ {new_title} ] already exists! Use a different title"}, status=400)
                    assessments = list(Assessment.objects.filter(school=school, level=current_level, teacher=teacher, subject=subject_obj, student_class=students_class, title=old_title, academic_year=current_academic_year, academic_term=term))
                    for _assessment in assessments:
                        _assessment.title = new_title
                        assessments_to_update.append(_assessment)
                    try:
                        Assessment.objects.bulk_update(assessments_to_update, ['title'])
                    except Exception:
                        return Response(status=400) 
                
            elif (request.data['editType'] == 'description'):
                with transaction.atomic():
                    assessments_to_update = []
                    new_description = request.data['newDescription']
                    assessments = list(Assessment.objects.filter(school=school, level=current_level, teacher=teacher, subject=subject_obj, student_class=students_class, title=assessment_title, academic_year=current_academic_year, academic_term=term))
                    for _assessment in assessments:
                        _assessment.description = new_description
                        assessments_to_update.append(_assessment)
                    try:
                        Assessment.objects.bulk_update(assessments_to_update, ['description'])
                    except Exception:
                        return Response(status=400) 
                    
            elif (request.data['editType'] == 'totalScore'):
                assessments_to_update = []
                results_to_update = []
                new_total_score = Decimal(request.data['newTotalScore'])
                if new_total_score <= 0:
                    return Response({'message': "The total score of the assessment cannot be negative or zero(0)"}, status=400)
                assessments = Assessment.objects.select_related('student').filter(school=school, level=current_level, teacher=teacher, subject=subject_obj, student_class=students_class, title=assessment_title, academic_year=current_academic_year, academic_term=term)
                grading_system = GradingSystem.objects.filter(school=school, levels=current_level).order_by('lower_limit')
                for _assessment in assessments:
                    old_total_score = _assessment.total_score
                    if _assessment.score and new_total_score < float(_assessment.score):
                        return Response({'message': "The total score of the assessment cannot be less than the a student's score"}, status=400)
                    _assessment.total_score = new_total_score
                    assessments_to_update.append(_assessment)
                    st_result = StudentResult.objects.filter(school=school, level=current_level, teacher=teacher, student=_assessment.student, subject=subject_obj, student_class=students_class, academic_year=current_academic_year, academic_term=term).first()
                    if st_result:
                        old_assessment_score = (_assessment.score/old_total_score)*_assessment.percentage
                        new_assessment_score = (_assessment.score/new_total_score)*_assessment.percentage
                        new_total_assessment_score = (st_result.total_assessment_score + new_assessment_score) - old_assessment_score
                        new_total_assessment_score = math.ceil(new_total_assessment_score) if new_total_assessment_score - math.floor(new_total_assessment_score) >= 0.5 else math.floor(new_total_assessment_score)
                        new_result = st_result.exam_score + new_total_assessment_score
                        student_grade = next((item for item in grading_system if item.upper_limit >= new_result >= item.lower_limit), None)
                        st_result.total_assessment_score = new_total_assessment_score
                        st_result.result = new_result
                        st_result.grade = student_grade.label
                        st_result.remark = student_grade.remark
                        results_to_update.append(st_result)
                with transaction.atomic():
                    try:
                        Assessment.objects.bulk_update(assessments_to_update, ['total_score'])
                        StudentResult.objects.bulk_update(results_to_update, ['total_assessment_score', 'result', 'grade', 'remark'])
                    except Exception:
                        return Response(status=400) 
                all_results =  StudentResult.objects.filter(school=school, level=current_level, teacher=teacher, subject=subject_obj, student_class=students_class, academic_year=current_academic_year, academic_term=term).order_by('-result')
                all_results_data = TeacherGetStudentResultSerializer(all_results, many=True).data
                return Response(all_results_data)
            
            elif (request.data['editType'] == 'date'):
                assessments_to_update = []
                new_date = request.data['newDate']
                new_date_object = datetime.strptime(new_date, '%Y-%m-%d').date()
                if (new_date_object > current_academic_year.end_date) or (new_date_object < current_academic_year.start_date):
                    return Response({'message': f"The assessment date must be between the academic year start and end dates. That's {current_academic_year.start_date} and {current_academic_year.end_date}"}, status=400)
                assessments = list(Assessment.objects.filter(school=school, level=current_level, teacher=teacher, subject=subject_obj, student_class=students_class, title=assessment_title, academic_year=current_academic_year, academic_term=term))
                for _assessment in assessments:
                    _assessment.assessment_date = new_date
                    assessments_to_update.append(_assessment)
                with transaction.atomic():
                    try:
                        Assessment.objects.bulk_update(assessments_to_update, ['assessment_date'])
                    except Exception:
                        return Response({'message': 'An unexpected error occurred! try again later'}, status=400)
                
            elif (request.data['editType'] == 'comment'):
                new_comment = request.data['newComment']
                student = Student.objects.get(school=school, level=current_level, st_id=request.data['studentId'])
                with transaction.atomic():
                    try:
                        assessment = Assessment.objects.get(school=school, level=current_level, teacher=teacher, subject=subject_obj, student=student, student_class=students_class, title=assessment_title, academic_year=current_academic_year, academic_term=term)
                        assessment.comment = new_comment
                        assessment.save()
                    except Exception:
                        return Response(status=400)     
                
            elif (request.data['editType'] == 'score'):
                new_score = Decimal(request.data['newScore'])
                if new_score < 0:
                    return Response({'message': "The student's score cannot be negative"}, status=400)
                student = Student.objects.get(school=school, level=current_level, st_id=request.data['studentId'])
                with transaction.atomic():
                    try:
                        assessment = Assessment.objects.get(school=school, level=current_level, teacher=teacher, subject=subject_obj, student=student, student_class=students_class, title=assessment_title, academic_year=current_academic_year, academic_term=term)
                        if new_score > float(assessment.total_score):
                            return Response({"message": "The student's score cannot exceed the total assessment score"}, status=400)
                        old_assessment_score = (assessment.score/assessment.total_score)*assessment.percentage
                        assessment.score = new_score
                        assessment.save()
                        st_result = StudentResult.objects.get(school=school, level=current_level, teacher=teacher, subject=subject_obj, student=student, student_class=students_class, academic_year=current_academic_year, academic_term=term)
                        new_assessment_score = (new_score/assessment.total_score)*assessment.percentage
                        new_total_assessment_score = (st_result.total_assessment_score + new_assessment_score) - old_assessment_score
                        new_total_assessment_score = math.ceil(new_total_assessment_score) if new_total_assessment_score - math.floor(new_total_assessment_score) >= 0.5 else math.floor(new_total_assessment_score)
                        grading_system = GradingSystem.objects.filter(schools=school, level=current_level).order_by('lower_limit')
                        new_result = new_total_assessment_score + st_result.exam_score
                        student_grade = next((item for item in grading_system if item.upper_limit >= new_result >= item.lower_limit), None)
                        st_result.total_assessment_score = new_total_assessment_score
                        st_result.result = new_result
                        st_result.grade = student_grade.label
                        st_result.remark = student_grade.remark
                        st_result.save()
                        return Response({
                            'new_total_assessment_score': new_total_assessment_score, 
                            'new_result': new_result,
                            'new_grade': student_grade.label,
                            'new_remark': student_grade.remark,
                        })
                    except StudentResult.DoesNotExist:
                        transaction.set_rollback(False)
                    except Exception:
                        return Response(status=400)                
                
            return Response()
        
        elif request.data['type'] == 'deleteAssessment':
            students_class = Classe.objects.get(school=school, level=current_level, name=st_class_name)
            subject_obj = Subject.objects.get(name=subject_name)
            with transaction.atomic():
                try:
                    existing_results = StudentResult.objects.filter(school=school, level=current_level, subject=subject_obj, student_class=students_class, teacher=teacher, academic_year=current_academic_year, academic_term=term).exists()
                    if existing_results:
                        return Response({'message': f"Results for {subject_name} in this class have already been generated. Please delete the existing results data and try again."}, status=400)
                    assessments = Assessment.objects.filter(school=school, level=current_level, teacher=teacher, student_class=students_class, subject=subject_obj, title=assessment_title, academic_year=current_academic_year, academic_term=term)
                    assessments.delete()
                except Exception:
                    transaction.set_rollback(True)
                    return Response(status=400)
            
            return Response()
    

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def teacher_exams(request):
    teacher = request.user.staff.select_related('school', 'current_level')
    school = teacher.school
    current_level = teacher.current_level
    
    if request.method == 'GET':
        current_term = int(request.GET.get('term'))
        current_academic_year = AcademicYear.objects.get(school=school, level=current_level, name=request.GET.get('year'))
        student_exams_data = {}
        subject_assignments = SubjectAssignment.objects.select_related('teacher', 'students_class').prefetch_related('subjects').filter(school=school, level=current_level, teacher=teacher, academic_year=current_academic_year, academic_term=current_term)
        for assign in subject_assignments:
            students_class_name = assign.students_class.name
            all_students = assign.students_class.students.all()
            exams_data = {}
            for _subject in assign.subjects.all():
                subject_name = _subject.name
                subject_data = {'students_with_exams': {}, 'students_without_exams': {}}
                all_exams = Exam.objects.select_related('student__user').filter(school=school, level=current_level, teacher=teacher, subject=_subject, student_class=assign.students_class, academic_year=current_academic_year, academic_term=current_term).order_by('-score')
                students_with_exams = set()
                if all_exams.exists():
                    all_exams_first = all_exams.first()
                    subject_data['percentage'] = all_exams_first.percentage
                    subject_data['total_score'] = all_exams_first.total_score
                    for _exams in all_exams:
                        if _exams.student:
                            st_id = _exams.student.st_id
                            st_data = {
                                'name': f"{_exams.student.user.first_name} {_exams.student.user.last_name}",
                                'st_id': st_id,
                                'score': _exams.score,
                            }
                            subject_data['students_with_exams'][st_id] = st_data
                            students_with_exams.add(_exams.student)
                for _student in all_students:
                    if _student not in students_with_exams:
                        st_id = _student.st_id
                        st_data = {
                            'name': f"{_student.user.first_name} {_student.user.last_name}",
                            'st_id': st_id,
                        }
                        subject_data['students_without_exams'][st_id] = st_data
                exams_data[subject_name] = subject_data
            student_exams_data[students_class_name] = exams_data
            
        return Response({
            'exams_data': student_exams_data
        })
    
    elif request.method == 'POST':
        year = request.data['year']
        term = int(request.data['term'])
        subject_name = request.data['subject']
        st_class_name = request.data['studentsClassName']
        current_academic_year = AcademicYear.objects.select_related('period_division').get(school=school, level=current_level, name=year)
        if request.data['type'] == 'getFile':
            students = json.loads(request.data['selectedStudents'])
            if current_level.students_id:
                data = [
                    ['STUDENT NAME', 'STUDENT ID', 'SCORE']
                ]
            else:
                data = [
                    ['STUDENT NAME', 'STUDENT USERNAME', 'SCORE']
                ]

            if len(students) == 0:
                return Response({
                    'message': f"You have already uploaded all the {subject_name} Exams scores for all students in this class",
                }, status=400)
                
            for _st in students:
                row = [_st['name'], _st['st_id'], '']
                data.append(row)

            wb = Workbook()
            ws = wb.active
            ws.title = subject_name

            ws.merge_cells('A1:I3')
            ws['A1'].value = f"SUBJECT: [{subject_name}]  ACADEMIC YEAR: [{year}]  CLASS: [{st_class_name}]  {current_academic_year.period_division.name} {term} EXAMS"
            ws['A1'].font = Font(size=14, bold=True)
            ws['A1'].alignment = Alignment(horizontal='center', vertical='center')

            count = 0
            container = ws['B5:D200']
            while count < len(data):
                for row_ws, row_data in zip(container, data):
                    for cell, item in zip(row_ws, row_data):
                        cell.value = item

                count += 1

            ws.column_dimensions['A'].width = 40
            ws.column_dimensions['B'].width = 50
            ws.column_dimensions['C'].width = 25
            ws.column_dimensions['D'].width = 15

            for row in ws['A3:F200']:
                for cell in row:
                    cell.font = Font(size=14)
                    cell.alignment = Alignment(horizontal='center', vertical='center')

            for row in ws['B3:B200']:
                for cell in row:
                    cell.alignment = Alignment(horizontal='left', vertical='center')

            for cells in ws['A5:F200'][0]:
                cells.font = Font(bold=True, size=14)

            ws.protection.sheet = True
            for cell in ws.iter_rows(min_row=6, max_row=ws.max_row, min_col=4, max_col=4):
                cell[0].protection = Protection(locked=False)

            ws.protection.password = 'teamjn'

            filename = f"{subject_name.replace(' ', '-')}-{st_class_name}-Exams.xlsx"
            byte_file = io.BytesIO()
            wb.save(byte_file)
            file_path = f"{get_school_folder(school)}/staff/{teacher.user.username}/{filename}"
            if default_storage.exists(file_path):
                default_storage.delete(file_path)

            saved_file = default_storage.save(file_path, byte_file)
            if settings.DEBUG:
                return Response({
                    'filename': filename,
                    'message': 'File generated successfully',
                    'file_path': f"http://localhost:8000{default_storage.url(saved_file)}",
                })
            else:
                return Response({
                    'filename': filename,
                    'message': 'File generated successfully',
                    'file_path': default_storage.url(saved_file),
                })
        
        elif request.data['type'] == 'createExams':
            subject_obj = Subject.objects.get(name=subject_name)
            students_class = Classe.objects.get(school=school, level=current_level, name=st_class_name)
            existing_exams = Exam.objects.filter(school=school, level=current_level, teacher=teacher, subject=subject_obj, student_class=students_class, academic_year=current_academic_year, academic_term=term).exists()
            if existing_exams:
                return Response({'message': f"You have already created {subject_name} exams for this class"}, status=400)
            existing_results = StudentResult.objects.filter(school=school, level=current_level, teacher=teacher, subject=subject_obj, student_class=students_class, academic_year=current_academic_year, academic_term=term).exists()
            if existing_results:
                return Response({'message': f"Results for {subject_name} in this class have already been generated. Please delete the existing results data and try again."}, status=400)
            exams_total_score = request.data['totalScore']
            exams_obj = Exam.objects.create(
                school=school,
                level=current_level,
                teacher=teacher,
                student_class=students_class,
                subject=subject_obj,
                percentage=0,
                score=0,
                total_score=exams_total_score,
                academic_year=current_academic_year,
                academic_term=term
            )
            with transaction.atomic():
                try:
                    exams_obj.save()
                except Exception:
                    return Response(status=400)
                
            return Response({'message': "Operation Successful"})
            
        elif request.data['type'] == 'uploadWithFile':
            file = request.data['file']
            try:
                wb = load_workbook(file)
            except Exception:
                return Response({'message': "Invalid file. Ensure you upload the excel file that you generated"}, status=400)
            
            ws = wb.active
            ws.protection = False
            if ws['A1'].value != f"SUBJECT: [{subject_name}]  ACADEMIC YEAR: [{year}]  CLASS: [{st_class_name}]  {current_academic_year.period_division.name} {term} EXAMS":
                return Response({'message': "Invalid file. Ensure you upload the excel file that you generated"}, status=400)
            
            cleaned_data = []
            for row in ws.iter_rows(min_row=6, max_row=ws.max_row, min_col=2, max_col=4):
                data = []
                for _cell in row:
                    data.append(_cell.value)
                cleaned_data.append(data)
            
            valid_rows = [x for x in cleaned_data if x[0]]
            if len(valid_rows) == 0:
                return Response({'message': f"There are no students data in the uploaded file"}, status=400)
            for row in valid_rows:
                score = row[2]
                try:
                    float(score)
                except Exception:
                    return Response({'message': f"The scores must be a number. Recheck the score for {row[0]}[{row[1]}] in the file"}, status=400)
                if score > 100:
                    return Response({'message': f"Scores cannot be more than 100. Recheck the score for {row[0]}[{row[1]}] in the file"}, status=400)
                elif score < 0:
                    return Response({'message': f"Scores cannot be negative. Recheck the score for {row[0]}[{row[1]}] in the file"}, status=400)

            students_class = Classe.objects.prefetch_related('students').get(school=school, level=level, name=st_class_name)
            exams_students = []
            subject_obj = Subject.objects.get(name=subject_name)
            exams_to_create = []
            for _student in valid_rows:
                if students_class.students.filter(level=current_level, st_id=_student[1]).exists():
                    st = Student.objects.get(school=school, level=current_level, st_id=_student[1])
                    exams_students.append(st)
                    st_exam = Exam(
                        school=school,
                        student=st,
                        subject=subject_obj,
                        teacher=teacher,
                        percentage=0,
                        student_class=students_class,
                        score=float(_student[2]),
                        academic_year=current_academic_year,
                        academic_term=term,
                        level=current_level,
                    )
                    exams_to_create.append(st_exam)
                else:
                    return Response({'message': f"Invalid student {_student[0]}[{_student[1]}]. Make sure you don't change anything in the excel file except the scores"}, status=400)
            with transaction.atomic():
                try:
                    Exam.objects.bulk_create(exams_to_create)
                    exam_create_obj = Exam.objects.get(school=school, level=current_level, teacher=teacher, student=None, subject=subject_obj, student_class=students_class, academic_year=current_academic_year, academic_term=term)
                    exam_create_obj.delete()
                except Exam.DoesNotExist:
                    transaction.set_rollback(False)
                except IntegrityError:
                    transaction.set_rollback(True)
                    return Response({'message': f"You have already uploaded exams score for some of the students in the file. Click on get file to get an updated file"}, status=400)
                except Exception:
                    transaction.set_rollback(True)
                    return Response({'message': f"Invalid data! Ensure you don't delete or change anything in the excel file"}, status=400)
        
            all_exams = Exam.objects.select_related('student__user').filter(school=school, level=current_level, teacher=teacher, subject=subject_obj, student_class=students_class, student__in=exams_students, academic_year=current_academic_year, academic_term=term)
            all_exams_data = [{
                'name': f"{x.student.user.first_name} {x.student.user.last_name}",
                'st_id': x.student.st_id,
                'score': x.score,
            } for x in all_exams]
            
            return Response({'message': "Operation successful", 'data': all_exams_data})

        elif request.data['type'] == 'uploadWithoutFile':
            students_class = Classe.objects.get(school=school, level=current_level, name=st_class_name)
            subject_obj = Subject.objects.get(name=subject_name)
            score = float(request.data['score'])
            exams_to_create = []
            for _st_id in json.loads(request.data['selectedStudents']):
                student = Student.objects.get(school=school, level=current_level, st_id=_st_id)
                st_exam = Exam(
                    school=school,
                    student=student,
                    subject=subject_obj,
                    teacher=teacher,
                    student_class=students_class,
                    score=score,
                    percentage=0,
                    academic_year=current_academic_year,
                    academic_term=term,
                    level=current_level,
                )
                exams_to_create.append(st_exam)
            with transaction.atomic():
                try:
                    Exam.objects.bulk_create(exams_to_create)
                    exam_create_obj = Exam.objects.get(school=school, level=current_level, teacher=teacher, student=None, subject=subject_obj, student_class=students_class, academic_year=current_academic_year, academic_term=term)
                    exam_create_obj.delete()
                except Exam.DoesNotExist:
                    transaction.set_rollback(False)
                except Exception:
                    transaction.set_rollback(True)
                    return Response(status=400)
            
            return Response({'message': "Operation successful"})

        elif request.data['type'] == 'editTotalScore':
            new_total_score = Decimal(request.data['totalScore'])
            students_class = Classe.objects.get(school=school, level=current_level, name=st_class_name)
            subject_obj = Subject.objects.get(name=subject_name)
            exams_to_update = []
            results_to_update = []
            grading_system = GradingSystem.objects.filter(schools=school, level=current_level).order_by('lower_limit')
            exams = Exam.objects.filter(school=school, level=current_level, subject=subject_obj, student_class=students_class, teacher=teacher, academic_year=current_academic_year, academic_term=term)
            for _exam in exams:
                _exam.total_score = new_total_score
                exams_to_update.append(_exam)
                try:
                    st_result = StudentResult.objects.get(school=school, level=current_level, student=_exam.student, subject=subject_obj, student_class=students_class, teacher=teacher, academic_year=current_academic_year, academic_term=term)
                    new_exam_score = (_exam.score/new_total_score)*st_result.exam_percentage
                    new_exam_score = math.ceil(new_exam_score) if new_exam_score - math.floor(new_exam_score) >= 0.5 else math.floor(new_exam_score)
                    new_result = new_exam_score + st_result.total_assessment_score
                    student_grade = next((item for item in grading_system if item.upper_limit >= new_result >= item.lower_limit), None)
                    st_result.exam_score = new_exam_score
                    st_result.result = new_result
                    st_result.grade = student_grade.label
                    st_result.remark = student_grade.remark
                    results_to_update.append(st_result)
                except StudentResult.DoesNotExist:
                    continue
            with transaction.atomic():
                try:
                    Exam.objects.bulk_update(exams_to_update, ['total_score'])
                    if results_to_update:
                        StudentResult.objects.bulk_update(results_to_update, ['exam_score', 'result', 'grade', 'remark'])
                        all_results =  StudentResult.objects.filter(school=school, level=current_level, teacher=teacher, subject=subject_obj, student_class=students_class, academic_year=current_academic_year, academic_term=term).order_by('-result')
                        all_results_data = TeacherGetStudentResultSerializer(all_results, many=True).data
                        return Response(all_results_data)
                except Exception:
                    transaction.set_rollback(True)
                    return Response(status=400)
            return Response()
            
        
        elif request.data['type'] == 'editExamScore':
            new_score = Decimal(request.data['score'])
            with transaction.atomic():
                try:
                    students_class = Classe.objects.get(school=school, level=current_level, name=st_class_name)
                    subject_obj = Subject.objects.get(name=subject_name)
                    student = Student.objects.get(school=school, level=current_level, st_id=request.data['studentId'])
                    st_exam = Exam.objects.get(school=school, level=current_level, student=student, subject=subject_obj, student_class=students_class, teacher=teacher, academic_year=current_academic_year, academic_term=term)
                    st_exam.score = new_score
                    st_exam.save()
                    st_result = StudentResult.objects.get(school=school, level=current_level, student=student, subject=subject_obj, student_class=students_class, teacher=teacher, academic_year=current_academic_year, academic_term=term)
                    new_exam_score = (new_score/st_exam.total_score)*st_result.exam_percentage
                    new_exam_score = math.ceil(new_exam_score) if new_exam_score - math.floor(new_exam_score) >= 0.5 else math.floor(new_exam_score)
                    grading_system = GradingSystem.objects.filter(schools=school, level=current_level).order_by('lower_limit')
                    new_result = new_exam_score + st_result.total_assessment_score
                    student_grade = next((item for item in grading_system if item.upper_limit >= new_result >= item.lower_limit), None)
                    st_result.exam_score = new_exam_score
                    st_result.result = new_result
                    st_result.grade = student_grade.label
                    st_result.remark = student_grade.remark
                    st_result.save()
                    return Response({
                        'new_exam_score': new_exam_score, 
                        'new_result': new_result,
                        'new_grade': student_grade.label,
                        'new_remark': student_grade.remark,
                        })
                except StudentResult.DoesNotExist:
                    transaction.set_rollback(False)
                except Exception:
                    transaction.set_rollback(True)
                    return Response(status=400)
            
            return Response()
        
        elif request.data['type'] == 'deleteExam':
            with transaction.atomic():
                try:
                    students_class = Classe.objects.get(school=school, level=current_level, name=st_class_name)
                    subject_obj = Subject.objects.get(name=subject_name)
                    existing_results = StudentResult.objects.filter(school=school, level=current_level, subject=subject_obj, student_class=students_class, teacher=teacher, academic_year=current_academic_year, academic_term=term).exists()
                    if existing_results:
                        return Response({'message': f"Results for {subject_name} in this class have already been generated. Please delete the existing results data and try again."}, status=400)
                    exams = Exam.objects.filter(school=school, level=current_level, subject=subject_obj, student_class=students_class, teacher=teacher, academic_year=current_academic_year, academic_term=term)
                    exams.delete()
                    
                except Exception:
                    transaction.set_rollback(True)
                    return Response(status=400)
            
            return Response()


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def teacher_students_results(request):
    teacher = request.user.staff.select_related('school', 'current_level')
    school = teacher.school
    current_level = teacher.current_level
    
    if request.method == 'GET':
        current_academic_year = AcademicYear.objects.get(school=school, level=current_level, name=request.GET.get('year'))
        current_term = request.GET.get('term')
        student_results_data = {}
        subject_assignments = SubjectAssignment.objects.select_related('teacher', 'students_class').prefetch_related('subjects').filter(school=school, level=current_level, teacher=teacher, academic_year=current_academic_year, academic_term=current_term)
        for assign in subject_assignments:
            students_class_name = assign.students_class.name
            results_data = {}
            assignment_subjects = assign.subjects.all()
            for _subject in assignment_subjects:
                subject_name = _subject.name
                subject_data = {}
                student_results = StudentResult.objects.select_related('student__user').filter(school=school, level=current_level, teacher=teacher, subject=_subject, student_class=assign.students_class, academic_year=current_academic_year, academic_term=current_term).order_by('-result')
                if student_results.exists():
                    first_result_data = student_results.first()
                    subject_data['total_assessment_percentage'] = first_result_data.total_assessment_percentage
                    subject_data['exam_percentage'] = first_result_data.exam_percentage
                    all_results = {}
                    for _result in student_results:
                        st_id = _result.student.st_id
                        st_data = {
                            'result': _result.result,
                            'total_assessment_score': _result.total_assessment_score,
                            'exam_score': _result.exam_score,
                            'student': {'name': f"{_result.student.user.first_name} {_result.student.user.last_name}", 'st_id': st_id},
                            'remark': _result.remark,
                            'grade': _result.grade
                        }
                        all_results[st_id] = st_data
                    subject_data['student_results'] = all_results
                else:
                    subject_data['total_assessment_percentage'] = 0
                    subject_data['exam_percentage'] = 0
                    subject_data['student_results'] = {}
                results_data[subject_name] = subject_data
            student_results_data[students_class_name] = results_data
            
        return Response(student_results_data)

    elif request.method == 'POST':
        current_academic_year = AcademicYear.objects.get(school=school, level=current_level, name=request.data['year'])
        current_term = int(request.data['term'])
        subject_obj = Subject.objects.get(name=request.data['subject'])
        students_class = Classe.objects.get(school=school, level=current_level, name=request.data['studentsClassName'])
        if request.data['type'] == 'createResults':
            existing_results = StudentResult.objects.filter(school=school, level=current_level, teacher=teacher, subject=subject_obj, student_class=students_class, academic_year=current_academic_year, academic_term=current_term)
            if existing_results.exists():
                return Response({'message': f"{subject_obj.name} results for this class already exists"}, status=400)
            result_data = json.loads(request.data['resultsData'])
            grading_system = GradingSystem.objects.filter(schools=school, level=current_level).order_by('lower_limit')
            assessments_to_update = []
            exams_to_update = []
            results_to_create = []
            for _student in students_class.students.all():
                student_total_assessment_score = 0
                for _title in result_data['assessments']:
                    student_assessment = Assessment.objects.get(school=school, level=current_level, teacher=teacher, subject=subject_obj, student_class=students_class, student=_student, title=_title['title'], academic_year=current_academic_year, academic_term=current_term)
                    student_total_assessment_score += ((student_assessment.score/_title['totalScore'])*_title['percentage'])
                    student_assessment.percentage = _title['percentage']
                    assessments_to_update.append(student_assessment)
                student_total_assessment_score = math.ceil(student_total_assessment_score) if student_total_assessment_score - math.floor(student_total_assessment_score) >= 0.5 else math.floor(student_total_assessment_score)
                student_exam = Exam.objects.get(school=school, level=current_level, teacher=teacher, subject=subject_obj, student_class=students_class, student=_student, academic_year=current_academic_year, academic_term=current_term)
                student_exam_score = (student_exam.score/student_exam.total_score)*result_data['examsPercentage']
                student_exam_score = math.ceil(student_exam_score) if student_exam_score - math.floor(student_exam_score) >= 0.5 else math.floor(student_exam_score)
                result = student_total_assessment_score + student_exam_score
                student_exam.percentage = result_data['examsPercentage']
                exams_to_update.append(student_exam)
                student_grade = next((item for item in grading_system if item.upper_limit >= result >= item.lower_limit), None)
                student_result = StudentResult.objects.create(
                    school=school,
                    level=current_level,
                    teacher=teacher,
                    student=_student,
                    subject=subject_obj,
                    student_class=students_class,
                    exam_percentage=result_data['examsPercentage'],
                    exam_score=student_exam_score,
                    total_assessment_percentage=result_data['totalAssessmentPercentage'],
                    total_assessment_score=student_total_assessment_score,
                    result=result,
                    remark=student_grade.remark,
                    grade=student_grade.label,
                    academic_year = current_academic_year,
                    academic_term=current_term,
                )
                results_to_create.append(student_result)
            with transaction.atomic():
                try:
                    Assessment.objects.bulk_update(assessments_to_update, ['percentage'])
                    Exam.objects.bulk_update(exams_to_update, ['percentage'])
                    StudentResult.objects.bulk_create(results_to_create)
                except IntegrityError:
                    transaction.set_rollback(False)
                except Exception:
                    transaction.set_rollback(True)
                    return Response(status=400)
                
            subject_data = {}
            student_subject_results = StudentResult.objects.select_related('student__user').filter(school=school, level=current_level, teacher=teacher, subject=subject_obj, student_class=students_class, academic_year=current_academic_year, academic_term=current_term).order_by('-result')
            first_result_data = student_subject_results.first()
            subject_data['total_assessment_percentage'] = first_result_data.total_assessment_percentage
            subject_data['exam_percentage'] = first_result_data.exam_percentage
            all_results = {}
            for _result in student_results:
                st_id = _result.student.st_id
                st_data = {
                    'result': _result.result,
                    'total_assessment_score': _result.total_assessment_score,
                    'exam_score': _result.exam_score,
                    'student': {'name': f"{_result.student.user.first_name} {_result.student.user.last_name}", 'st_id': st_id},
                    'remark': _result.remark,
                    'grade': _result.grade
                }
                all_results[st_id] = st_data
            subject_data['student_results'] = all_results
            
            return Response(subject_data)
        
        elif request.data['type'] == 'deleteResults':
            with transaction.atomic():
                results = StudentResult.objects.filter(school=school, level=current_level, teacher=teacher, subject=subject_obj, student_class=students_class, academic_year=current_academic_year, academic_term=current_term)
                results.delete()
            
            return Response()

