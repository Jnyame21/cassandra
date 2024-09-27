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

# TEACHER
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def teacher_students_attendance(request):
    teacher = request.user.staff
    data = request.data
    academic_year = AcademicYear.objects.get(school=teacher.school, name=data['year'])
    students_class = Classe.objects.prefetch_related('students').get(school=teacher.school, name=data['className'])
    
    if data['type'] == 'create':
        students = data['absentStudents'].split(',')
        try:
            existing_attendance = StudentAttendance.objects.get(
                school=teacher.school,
                date=data['date'],
                teacher=teacher,
                students_class=students_class,
                academic_year=academic_year,
                academic_term=int(data['term']),
            )
            return Response({
                'ms': f"You have already uploaded attendance for the date {data['date']}",
            }, status=201)

        except StudentAttendance.DoesNotExist:
            with transaction.atomic():
                attendance = StudentAttendance.objects.create(
                    school=teacher.school,
                    teacher=teacher,
                    date=data['date'],
                    students_class=students_class,
                    academic_year=academic_year,
                    academic_term=int(data['term']),
                    students_year=students_class.students_year,
                )
                    
                for st in students_class.students.all():
                    if st.st_id not in students:
                        attendance.students_present.add(st)
                    else:
                        attendance.students_absent.add(st)

                attendance.save()

            new_attendance = StudentsAttendanceSerializer(StudentAttendance.objects.get(
                school=teacher.school,
                academic_year=academic_year,
                academic_term=int(data['term']),
                students_year=students_class.students_year,
                date=data['date'],
                students_class=students_class,
                teacher=teacher
            )).data

            return Response(new_attendance)

    elif data['type'] == 'delete':
        try:
            students_class = Classe.objects.get(school=teacher.school, name=data['className'])
            with transaction.atomic():
                student_attendance = StudentAttendance.objects.get(
                    school=teacher.school,
                    academic_year=academic_year,
                    academic_term=int(data['term']),
                    students_class=students_class,
                    teacher=teacher,
                    date=data['date'],
                )
                    
                student_attendance.delete()

            return Response(status=200)

        except StudentAttendance.DoesNotExist:
            return Response(status=401)

    # if request.method == 'GET':
    #     academic_year = AcademicYear.objects.get(school=teacher.school, name=request.GET.get('year'))
    #     term = int(request.GET.get('term'))
        # subject_assignments = SubjectAssignment.objects.prefetch_related('subject').filter(
        #     school=teacher.school,
        #     academic_year=academic_year,
        #     academic_term=term,
        #     teacher=teacher,
        # )
        # students_attendance = []
        
        # if subject_assignments.exists():
        #     for assign in subject_assignments:
        #         assign_data = SubjectAssignmentWithoutStudentsSerializer(assign).data
        #         attendance = StudentsAttendanceSerializer(StudentAttendance.objects.filter(
        #             school=teacher.school,
        #             academic_year=academic_year,
        #             academic_term=term,
        #             students_class=assign.students_class,
        #             subject=assign.subject
        #         ).order_by('-date'), many=True).data

        #         students_attendance.append({
        #             'subject': assign_data['subject']['name'],
        #             'class_name': assign_data['students_class']['name'],
        #             'students_year': assign_data['students_class']['students_year'],
        #             'attendance': attendance,
        #         })

        # return Response(attendance_data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_teacher_data(request):
    teacher = request.user.staff
    school = teacher.school
    current_term = int(request.GET.get('term'))
    current_academic_year = AcademicYear.objects.get(school=school, name=request.GET.get('year'))
    
    attendance = StudentAttendance.objects.filter(school=school, teacher=teacher, academic_year=current_academic_year, academic_term=current_term).order_by('-date')
    attendance_data = StudentsAttendanceSerializer(attendance, many=True).data
        
    subject_assignments = SubjectAssignment.objects.select_related('teacher', 'students_class').prefetch_related('subjects').filter(school=school, teacher=teacher, academic_year=current_academic_year, academic_term=current_term)
    subject_assignments_data = SubjectAssignmentSerializer(subject_assignments, many=True).data
        
    return Response({
        'subject_assignments': subject_assignments_data,
        'students_attendance': attendance_data,
    })


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def teacher_assessments(request):
    teacher = request.user.staff
    school = teacher.school
    
    if request.method == 'GET':
        current_term = int(request.GET.get('term'))
        current_academic_year = AcademicYear.objects.get(school=school, name=request.GET.get('year'))
        students_with_assessments_all = []
        students_without_assessments_all = []
            
        subject_assignments = list(SubjectAssignment.objects.select_related('teacher', 'students_class').prefetch_related('subjects').filter(school=school, teacher=teacher, academic_year=current_academic_year, academic_term=current_term))
        for assign in subject_assignments:
            all_students = assign.students_class.students.all()
            without_assessments_data = {'class_name': assign.students_class.name, 'assignments': []}
            with_assessments_data = {'class_name': assign.students_class.name, 'assignments': []}
            for _subject in assign.subjects.all():
                without_assessments = {'subject': _subject.name, 'assessments': []}
                with_assessments = {'subject': _subject.name, 'assessments': []}
                assessment = list(Assessment.objects.filter(school=school, teacher=teacher, subject=_subject, student_class=assign.students_class, academic_year=current_academic_year, academic_term=current_term))
                assessment_titles = list(set([x.title for x in assessment]))
                for _title in assessment_titles:
                    assessments_with_title = list(Assessment.objects.select_related('student__user').filter(school=school, teacher=teacher, title=_title, subject=_subject, student_class=assign.students_class, academic_year=current_academic_year, academic_term=current_term).order_by('-score'))
                    students_with_assessment = [x.student for x in assessments_with_title]
                    students_without_assessments_data = [
                        {'name': f"{x.user.first_name} {x.user.last_name}", 
                        'st_id': x.st_id,
                        } for x in all_students if x not in students_with_assessment]
                    without_assessments['assessments'].append({'title': _title, 'students': students_without_assessments_data})
                    
                    students_with_assessments_data = [
                        {'name': f"{x.student.user.first_name} {x.student.user.last_name}", 
                        'st_id': x.student.st_id,
                        'comment': x.comment,
                        'score': x.score,
                        } for x in assessments_with_title]
                    with_assessments['assessments'].append({
                        'title': _title, 
                        'students': students_with_assessments_data,
                        'description': assessments_with_title[0].description,
                        'percentage': assessments_with_title[0].percentage,
                        'total_score': assessments_with_title[0].total_score,
                        'date': assessments_with_title[0].date,
                        })
                
                without_assessments['assessments'].insert(0, {'title': 'New'})
                without_assessments_data['assignments'].append(without_assessments)
                with_assessments_data['assignments'].append(with_assessments)
            
            students_with_assessments_all.append(with_assessments_data)
            students_without_assessments_all.append(without_assessments_data)
            
        return Response({
            'with_assessments': students_with_assessments_all,
            'without_assessments': students_without_assessments_all,
        })
    
    elif request.method == 'POST':
        year = request.data['year']
        term = int(request.data['term'])
        subject_name = request.data['subject']
        st_class_name = request.data['studentsClassName']
        current_academic_year = AcademicYear.objects.select_related('period_division').get(school=school, name=year)
        assessment_title = request.data['title']
        if request.data['type'] == 'getFile':
            students = json.loads(request.data['selectedStudents'])
            if school.students_id:
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
                
            subject_obj = Subject.objects.get(schools=school, name=subject_name)
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
            file_path = f"{get_school_folder(school.name)}/staff/{teacher.user.username}/{filename}"
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

        elif request.data['type'] == 'uploadWithFile':
            file = request.data['file']
            subject_obj = Subject.objects.get(name=subject_name)
            if request.data['new'] == 'yes':
                if Assessment.objects.filter(school=school, teacher=teacher, subject=subject_obj, title=assessment_title, academic_year=current_academic_year, academic_term=term).exists():
                    return Response({'message': f"Assessment with title '{assessment_title}' already exists. Use a different title"}, status=400)
                description = request.data['description']
                total_score = float(request.data['totalScore'])
                percentage = float(request.data['percentage'])
                date = request.data['date']
            elif request.data['new'] == 'no':
                old_assessment = Assessment.objects.filter(school=school, teacher=teacher, subject=subject_obj, title=assessment_title, academic_year=current_academic_year, academic_term=term).first()
                description = old_assessment.description
                total_score = old_assessment.total_score
                percentage = old_assessment.percentage
                date = old_assessment.date
                
            try:
                wb = load_workbook(file)
            except Exception:
                return Response({'message': "Invalid file. Ensure you upload the excel file that you generated"}, status=400)
            
            ws = wb.active
            ws.protection = False

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
                    return Response({'message': f"Scores cannot exceed the total score for the assessment. Recheck the score for {row[0]}[{row[1]}] in the file"}, status=400)
                elif score < 0:
                    return Response({'message': f"Scores cannot be negative. Recheck the score for {row[0]}[{row[1]}] in the file"}, status=400)

            students_class = Classe.objects.prefetch_related('students').get(school=school, name=st_class_name)
            with transaction.atomic():
                assessments_to_create = []
                for _student in valid_rows:
                    if students_class.students.filter(school=school, st_id=_student[1]).exists():
                        student = Student.objects.get(school=school, st_id=_student[1])
                        st_assessment = Assessment(
                            student=student,
                            subject=subject_obj,
                            teacher=teacher,
                            student_class=students_class,
                            score=float(_student[2]),
                            student_year=student.current_year,
                            academic_year=current_academic_year,
                            title=assessment_title,
                            description=description,
                            percentage=percentage,
                            total_score=total_score,
                            comment=_student[3] if _student[3] else '',
                            academic_term=term,
                            school=school,
                            date=date,
                        )
                        assessments_to_create.append(st_assessment)
                    else:
                        transaction.set_rollback(True)
                        return Response({'message': f"Invalid student {_student[0]}[{_student[1]}]. Make sure you don't change anything in the excel file except the scores and comments"}, status=400)
                try:
                    Assessment.objects.bulk_create(assessments_to_create)
                except IntegrityError:
                    transaction.set_rollback(True)
                    return Response({'message': f"You have already uploaded Assessment for some of the students in the file. Click on get file to get a new updated file"}, status=400)
                except Exception:
                    transaction.set_rollback(True)
                    return Response({'message': f"An unexpected error occurred! Ensure you don't delete or change anything in the excel file except the scores and comments"}, status=400)
                
            return Response({'message': "Data uploaded and saved successfully"})

        elif request.data['type'] == 'uploadWithoutFile':
            students_class = Classe.objects.get(school=school, name=st_class_name)
            subject_obj = Subject.objects.get(name=subject_name)
            comment = request.data['comment']
            if request.data['new'] == 'yes':
                description = request.data['description']
                total_score = float(request.data['totalScore'])
                percentage = float(request.data['percentage'])
                date = request.data['date']
            elif request.data['new'] == 'no':
                old_assessment = Assessment.objects.filter(school=school, teacher=teacher, student_class=students_class, subject=subject_obj, title=assessment_title, academic_year=current_academic_year, academic_term=term).first()
                description = old_assessment.description
                total_score = old_assessment.total_score
                percentage = old_assessment.percentage
                date = old_assessment.date
            
            score = float(request.data['score'])
            if score > total_score:
                return Response({'message': f"The student(s) score cannot exceed the total score for the assessment!"}, status=400)
            
            with transaction.atomic():
                assessments_to_create = []
                for _st_id in request.data['selectedStudents'].split(','):
                    student = Student.objects.get(school=school, st_id=_st_id)
                    st_assessment = Assessment(
                        student=student,
                        subject=subject_obj,
                        teacher=teacher,
                        student_class=students_class,
                        score=score,
                        student_year=student.current_year,
                        academic_year=current_academic_year,
                        title=assessment_title,
                        description=description,
                        percentage=percentage,
                        total_score=total_score,
                        comment=comment,
                        academic_term=term,
                        school=school,
                        date=date,
                    )
                    assessments_to_create.append(st_assessment)
                
                try:
                    Assessment.objects.bulk_create(assessments_to_create)
                except Exception:
                    transaction.set_rollback(True)
                    return Response({'message': 'An unexpected error occurred! try again later'}, status=400)
            
            return Response({'message': "Data uploaded and saved successfully"})

        elif request.data['type'] == 'editAssessment':
            students_class = Classe.objects.get(school=school, name=st_class_name)
            subject_obj = Subject.objects.get(name=subject_name)
            if (request.data['editType'] == 'title'):
                assessments_to_update = []
                old_title = request.data['title']
                new_title = request.data['newTitle']
                assessments = list(Assessment.objects.filter(school=school, teacher=teacher, subject=subject_obj, student_class=students_class, title=old_title, academic_year=current_academic_year, academic_term=term))
                if len(assessments) == 0:
                    return Response({'message': 'An unexpected error occurred! try again later'}, status=400)
                for _assessment in assessments:
                    _assessment.title = new_title
                    assessments_to_update.append(_assessment)
                try:
                    Assessment.objects.bulk_update(assessments_to_update, ['title'])
                except Exception:
                    return Response({'message': 'An unexpected error occurred! try again later'}, status=400) 
            elif (request.data['editType'] == 'description'):
                assessments_to_update = []
                title = request.data['title']
                new_description = request.data['newDescription']
                assessments = list(Assessment.objects.filter(school=school, teacher=teacher, subject=subject_obj, student_class=students_class, title=title, academic_year=current_academic_year, academic_term=term))
                if len(assessments) == 0:
                    return Response({'message': 'An unexpected error occurred! try again later'}, status=400)   
                for _assessment in assessments:
                    _assessment.description = new_description
                    assessments_to_update.append(_assessment)
                try:
                    Assessment.objects.bulk_update(assessments_to_update, ['description'])
                except Exception:
                    return Response({'message': 'An unexpected error occurred! try again later'}, status=400) 
            elif (request.data['editType'] == 'totalScore'):
                assessments_to_update = []
                title = request.data['title']
                new_total_score = request.data['newTotalScore']
                assessments = list(Assessment.objects.filter(school=school, teacher=teacher, subject=subject_obj, student_class=students_class, title=title, academic_year=current_academic_year, academic_term=term))
                if len(assessments) == 0:
                    return Response({'message': 'An unexpected error occurred! try again later'}, status=400) 
                for _assessment in assessments:
                    _assessment.total_score = new_total_score
                    assessments_to_update.append(_assessment)
                try:
                    Assessment.objects.bulk_update(assessments_to_update, ['total_score'])
                except Exception:
                    return Response({'message': 'An unexpected error occurred! try again later'}, status=400) 
            elif (request.data['editType'] == 'percentage'):
                assessments_to_update = []
                title = request.data['title']
                new_percentage = request.data['newPercentage']
                assessments = list(Assessment.objects.filter(school=school, teacher=teacher, subject=subject_obj, student_class=students_class, title=title, academic_year=current_academic_year, academic_term=term))
                if len(assessments) == 0:
                    return Response({'message': 'An unexpected error occurred! try again later'}, status=400)    
                for _assessment in assessments:
                    _assessment.percentage = new_percentage
                    assessments_to_update.append(_assessment)
                try:
                    Assessment.objects.bulk_update(assessments_to_update, ['percentage'])
                except Exception:
                    return Response({'message': 'An unexpected error occurred! try again later'}, status=400)  
            elif (request.data['editType'] == 'date'):
                assessments_to_update = []
                title = request.data['title']
                new_date = request.data['newDate']
                assessments = list(Assessment.objects.filter(school=school, teacher=teacher, subject=subject_obj, student_class=students_class, title=title, academic_year=current_academic_year, academic_term=term))
                if len(assessments) == 0:
                    return Response({'message': 'An unexpected error occurred! try again later'}, status=400)    
                for _assessment in assessments:
                    _assessment.percentage = new_date
                    assessments_to_update.append(_assessment)
                try:
                    Assessment.objects.bulk_update(assessments_to_update, ['date'])
                except Exception:
                    return Response({'message': 'An unexpected error occurred! try again later'}, status=400)
            elif (request.data['editType'] == 'comment'):
                title = request.data['title']
                new_comment = request.data['newComment']
                student = Student.objects.get(school=school, st_id=request.data['studentId'])
                try:
                    assessment = Assessment.objects.get(school=school, teacher=teacher, subject=subject_obj, student=student, student_class=students_class, title=title, academic_year=current_academic_year, academic_term=term)
                    assessment.comment = new_comment
                    assessment.save()
                except Exception:
                    return Response({'message': 'An unexpected error occurred! try again later'}, status=400)     
            elif (request.data['editType'] == 'score'):
                title = request.data['title']
                new_score = request.data['newScore']
                student = Student.objects.get(school=school, st_id=request.data['studentId'])
                try:
                    assessment = Assessment.objects.get(school=school, teacher=teacher, subject=subject_obj, student=student, student_class=students_class, title=title, academic_year=current_academic_year, academic_term=term)
                    assessment.score = float(new_score)
                    assessment.save()
                except Exception:
                    return Response({'message': 'An unexpected error occurred! try again later'}, status=400)                
                
            return Response()
        
        elif request.data['type'] == 'deleteAssessment':
            student_class = Classe.objects.get(school=school, name=st_class_name)
            title = request.data['title']
            subject_obj = Subject.objects.get(name=subject_name)
            student = Student.objects.get(school=school, st_id=request.data['studentId'])
            with transaction.atomic():
                try:
                    assessment = Assessment.objects.get(school=school, teacher=teacher, student=student, subject=subject_obj, student_class=student_class, title=title, academic_year=current_academic_year, academic_term=term)
                    assessment.delete()
                    return Response()
                except Exception:
                    transaction.set_rollback(True)
                    return Response({'message': 'An unexpected error occurred! try again later'}, status=400)
            
            return Response()
    

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def teacher_exams(request):
    teacher = request.user.staff
    school = teacher.school
    
    if request.method == 'GET':
        current_term = int(request.GET.get('term'))
        current_academic_year = AcademicYear.objects.get(school=school, name=request.GET.get('year'))
        students_with_exams_all = []
        students_without_exams_all = []
            
        subject_assignments = list(SubjectAssignment.objects.select_related('teacher', 'students_class').prefetch_related('subjects').filter(school=school, teacher=teacher, academic_year=current_academic_year, academic_term=current_term))
        for assign in subject_assignments:
            all_students = assign.students_class.students.all()
            students_without_exams_obj = {'class_name': assign.students_class.name, 'exams': []}
            students_with_exams_obj = {'class_name': assign.students_class.name, 'exams': []}
            for _subject in assign.subjects.all():
                exam_obj_without = {'subject': _subject.name}
                exam_obj_with = {'subject': _subject.name}
                exams = list(Exam.objects.select_related('student__user').filter(school=school, teacher=teacher, subject=_subject, student_class=assign.students_class, academic_year=current_academic_year, academic_term=current_term).order_by('-score'))
                students_with_exams = [x.student for x in exams]
                students_without_exams_data = [
                    {'name': f"{x.user.first_name} {x.user.last_name}", 
                     'st_id': x.st_id,
                    } for x in all_students if x not in students_with_exams]
                
                exam_obj_without['students'] = students_without_exams_data
                
                students_with_exams_data = [{
                    'name': f"{x.student.user.first_name} {x.student.user.last_name}", 
                    'st_id': x.student.st_id,
                    'score': x.score,
                } for x in exams]
                exam_obj_with['students'] = students_with_exams_data
                
                students_without_exams_obj['exams'].append(exam_obj_without)
                students_with_exams_obj['exams'].append(exam_obj_with)
            
            students_with_exams_all.append(students_with_exams_obj) 
            students_without_exams_all.append(students_without_exams_obj)
            
        return Response({
            'with_exams': students_with_exams_all,
            'without_exams': students_without_exams_all,
        })
    
    elif request.method == 'POST':
        year = request.data['year']
        term = int(request.data['term'])
        subject_name = request.data['subject']
        st_class_name = request.data['studentsClassName']
        current_academic_year = AcademicYear.objects.select_related('period_division').get(school=school, name=year)
        if request.data['type'] == 'getFile':
            students = json.loads(request.data['selectedStudents'])
            if school.students_id:
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
            ws['A1'].value = f"SUBJECT: [{subject_name}]  ACADEMIC YEAR: [{year}]  CLASS: [{st_class_name}]  {current_academic_year.period_division.name}: [{term}]"
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
            file_path = f"{get_school_folder(school.name)}/staff/{teacher.user.username}/{filename}"
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

        elif request.data['type'] == 'uploadWithFile':
            file = request.data['file']
            try:
                wb = load_workbook(file)
            except Exception:
                return Response({'message': "Invalid file. Ensure you upload the excel file that you generated"}, status=400)
            
            ws = wb.active
            ws.protection = False

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

            students_class = Classe.objects.prefetch_related('students').get(school=school, name=st_class_name)
            subject_obj = Subject.objects.get(name=subject_name)
            with transaction.atomic():
                exams_to_create = []
                for _student in valid_rows:
                    if students_class.students.filter(school=school, st_id=_student[1]).exists():
                        st = Student.objects.get(school=school, st_id=_student[1])
                        st_exam = Exam(
                            student=st,
                            subject=subject_obj,
                            teacher=teacher,
                            student_class=students_class,
                            score=float(_student[2]),
                            student_year=st.current_year,
                            academic_year=current_academic_year,
                            academic_term=term,
                            school=school,
                        )
                        exams_to_create.append(st_exam)
                    else:
                        transaction.set_rollback(True)
                        return Response({'message': f"Invalid student {_student[0]}[{_student[1]}]. Make sure you don't change anything in the excel file except the scores"}, status=400)
                try:
                    Exam.objects.bulk_create(exams_to_create)
                except IntegrityError:
                    transaction.set_rollback(True)
                    return Response({'message': f"You have already uploaded exams score for some of the students in the file. Click on get file to get an updated file"}, status=400)
                except Exception:
                    transaction.set_rollback(True)
                    return Response({'message': f"Invalid data! Ensure you don't delete or change anything in the excel file"}, status=400)
                
            return Response({'message': "Data uploaded and saved successfully"})

        elif request.data['type'] == 'uploadWithoutFile':
            students_class = Classe.objects.get(school=school, name=st_class_name)
            subject_obj = Subject.objects.get(name=subject_name)
            score = float(request.data['score'])
            with transaction.atomic():
                exams_to_create = []
                for _st_id in request.data['selectedStudents'].split(','):
                    student = Student.objects.get(school=school, st_id=_st_id)
                    st_exam = Exam(
                        student=student,
                        subject=subject_obj,
                        teacher=teacher,
                        student_class=students_class,
                        score=score,
                        student_year=student.current_year,
                        academic_year=current_academic_year,
                        academic_term=term,
                        school=school,
                    )
                    exams_to_create.append(st_exam)
                try:
                    Exam.objects.bulk_create(exams_to_create)
                except IntegrityError:
                    transaction.set_rollback(True)
                    return Response({'message': 'An unexpected error occurred! try again later'}, status=400)
                except Exception:
                    transaction.set_rollback(True)
                    return Response({'message': "An unexpected error occurred! try again later"}, status=400)
            
            return Response({'message': "Data uploaded and saved successfully"})

        elif request.data['type'] == 'editExamScore':
            with transaction.atomic():
                try:
                    students_class = Classe.objects.get(school=school, name=st_class_name)
                    subject_obj = Subject.objects.get(name=subject_name)
                    student = Student.objects.get(school=school, st_id=request.data['studentId'])
                    st_exam = Exam.objects.get(student=student, subject=subject_obj, teacher=teacher, academic_year=current_academic_year, academic_term=term, school=school)
                    st_exam.score = float(request.data['score'])
                    st_exam.save()
                except Exception:
                    transaction.set_rollback(True)
                    return Response({'message': "An unexpected error occurred! try again later"}, status=400)
            
            return Response()
        
        elif request.data['type'] == 'deleteExam':
            with transaction.atomic():
                try:
                    student_class = Classe.objects.get(school=school, name=st_class_name)
                    subject_obj = Subject.objects.get(name=subject_name)
                    student = Student.objects.get(school=school, st_id=request.data['studentId'])
                    st_exam = Exam.objects.get(school=school, student=student, subject=subject_obj, student_class=student_class, teacher=teacher, academic_year=current_academic_year, academic_term=term)
                    st_exam.delete()
                except Exception:
                    transaction.set_rollback(True)
                    return Response(status=400)
            
            return Response()


# HOD
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_hod_data(request):
    staff = request.user.staff
    # Hod crate subject assignments
    if request.method == 'POST' and request.data['type'] == 'create':
        subject = Subject.objects.get(schools=staff.school, name=request.data['subject'])
        class_name = request.data['class_name'].split(' ', 1)
        students_class = Classe.objects.get(school=staff.school, name=class_name[0])
        academic_year = AcademicYear.objects.get(school=staff.school, name=request.data['year'])
        teacher = Staff.objects.get(school=staff.school, staff_id=request.data['staff_id'])
        if teacher.subjects.filter(name=subject.name).exists():
            if students_class.subjects.filter(name=subject.name).exists():
                with transaction.atomic():
                    try:
                        subjects_assignment = SubjectAssignment.objects.create(
                            hod=staff,
                            subject=subject,
                            students_class=students_class,
                            teacher=teacher,
                            academic_year=academic_year,
                            academic_term=int(request.data['term']),
                            school=staff.school
                        )
                        subjects_assignment.save()
                        response_data = get_hod_subject_assignments(staff, academic_year)
                        return Response(
                            {
                                'ms': f"subject assignment uploaded and saved successfully",
                                'data': response_data},
                            status=200)

                    except IntegrityError:
                      return Response({'ms': "Subject assignment with these details already exists"}, status=201)

            else:
                return Response({'ms': f"The class you selected don't study {request.data['subject']}"}, status=201 )
        else:
            return Response({'ms': f"The teacher you selected doesn't teach {request.data['subject']}"}, status=201)

        # Hod delete subject assignment
    elif request.method == 'POST' and request.data['type'] == 'delete':
        subject = Subject.objects.get(schools=staff.school, name=request.data['subject_name'])
        students_class = Classe.objects.get(school=staff.school, name=request.data['students_class_name'])
        academic_year = AcademicYear.objects.get(school=staff.school, name=request.data['year'])
        teacher = Staff.objects.get(school=staff.school, staff_id=request.data['teacher_id'])

        subjects_assignment = SubjectAssignment.objects.get(
            subject=subject,
            hod=staff,
            students_class=students_class,
            teacher=teacher,
            academic_year=academic_year,
            academic_term=int(request.data['term']),
            school=staff.school
        )
        subjects_assignment.delete()

        return Response(status=200)

    else:
        academic_year = AcademicYear.objects.get(school=staff.school, name=request.GET.get('year'))
        response_data = get_hod_subject_assignments(staff, academic_year)
        return Response(response_data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def hod_students_performance(request):
    staff = request.user.staff
    department = DepartmentSerializer(Department.objects.get(school=staff.school, teachers=staff)).data
    academic_year = AcademicYear.objects.get(school=staff.school, name=request.GET.get('year'))

    data = []
    if department:
        for subject in department['subjects']:
            first_year = {'term_one': [], 'term_two': [], 'term_three': []}
            second_year = {'term_one': [], 'term_two': [], 'term_three': []}
            third_year = {'term_one': [], 'term_two': [], 'term_three': []}

            subject_obj = Subject.objects.get(schools=staff.school, name=subject['name'])

            # Year One Student Exams
            result_one_one = ExamsSerializer(
                Exam.objects.filter(
                    school=staff.school,
                    academic_year=academic_year,
                    subject=subject_obj,
                    academic_term=1,
                    student_year=1,
                ),
                many=True).data
            if result_one_one:
                for result in result_one_one:
                    first_year['term_one'].append({
                        'name': f"{result['student']['user']['first_name']} {result['student']['user']['last_name']}",
                        'st_id': result['student']['st_id'],
                        'score': float(result['score']),
                    })

                first_year['term_one'] = sorted(first_year['term_one'], key=lambda x: x['score'], reverse=True)

            result_one_two = ExamsSerializer(
                Exam.objects.filter(
                    school=staff.school,
                    academic_year=academic_year,
                    subject=subject_obj,
                    academic_term=2,
                    student_year=1,
                ),
                many=True).data
            if result_one_two:
                for result in result_one_two:
                    first_year['term_two'].append({
                        'name': f"{result['student']['user']['first_name']} {result['student']['user']['last_name']}",
                        'st_id': result['student']['st_id'],
                        'score': float(result['score']),
                    })

                first_year['term_two'] = sorted(first_year['term_two'], key=lambda x: x['score'], reverse=True)

            result_one_three = ExamsSerializer(
                Exam.objects.filter(
                    school=staff.school,
                    academic_year=academic_year,
                    subject=subject_obj,
                    academic_term=3,
                    student_year=1,
                ),
                many=True).data
            if result_one_three:
                for result in result_one_three:
                    first_year['term_three'].append({
                        'name': f"{result['student']['user']['first_name']} {result['student']['user']['last_name']}",
                        'st_id': result['student']['st_id'],
                        'score': float(result['score']),
                    })

                first_year['term_three'] = sorted(first_year['term_three'], key=lambda x: x['score'], reverse=True)

            # Year Two Students Exams
            result_two_one = ExamsSerializer(
                Exam.objects.filter(
                    school=staff.school,
                    academic_year=academic_year,
                    subject=subject_obj,
                    academic_term=1,
                    student_year=2,
                ),
                many=True).data
            if result_two_one:
                for result in result_two_one:
                    second_year['term_one'].append({
                        'name': f"{result['student']['user']['first_name']} {result['student']['user']['last_name']}",
                        'st_id': result['student']['st_id'],
                        'score': float(result['score']),
                    })

                second_year['term_one'] = sorted(second_year['term_one'], key=lambda x: x['score'], reverse=True)

            result_two_two = ExamsSerializer(
                Exam.objects.filter(
                    school=staff.school,
                    academic_year=academic_year,
                    subject=subject_obj,
                    academic_term=2,
                    student_year=2,
                ),
                many=True).data
            if result_two_two:
                for result in result_two_two:
                    second_year['term_two'].append({
                        'name': f"{result['student']['user']['first_name']} {result['student']['user']['last_name']}",
                        'st_id': result['student']['st_id'],
                        'score': float(result['score']),
                    })

                second_year['term_two'] = sorted(second_year['term_two'], key=lambda x: x['score'], reverse=True)

            result_two_three = ExamsSerializer(
                Exam.objects.filter(
                    school=staff.school,
                    academic_year=academic_year,
                    subject=subject_obj,
                    academic_term=3,
                    student_year=2,
                ),
                many=True).data
            if result_two_three:
                for result in result_two_three:
                    second_year['term_three'].append({
                        'name': f"{result['student']['user']['first_name']} {result['student']['user']['last_name']}",
                        'st_id': result['student']['st_id'],
                        'score': float(result['score']),
                    })

                second_year['term_three'] = sorted(second_year['term_three'], key=lambda x: x['score'], reverse=True)

            # Year Three Students Exams
            result_three_one = ExamsSerializer(
                Exam.objects.filter(
                    school=staff.school,
                    academic_year=academic_year,
                    subject=subject_obj,
                    academic_term=1,
                    student_year=3,
                ),
                many=True).data
            if result_three_one:
                for result in result_three_one:
                    third_year['term_one'].append({
                        'name': f"{result['student']['user']['first_name']} {result['student']['user']['last_name']}",
                        'st_id': result['student']['st_id'],
                        'score': float(result['score']),
                    })

                third_year['term_one'] = sorted(third_year['term_one'], key=lambda x: x['score'],
                                                reverse=True)

            result_three_two = ExamsSerializer(
                Exam.objects.filter(
                    school=staff.school,
                    academic_year=academic_year,
                    subject=subject_obj,
                    academic_term=2,
                    student_year=3,
                ),
                many=True).data
            if result_three_two:
                for result in result_three_two:
                    third_year['term_two'].append({
                        'name': f"{result['student']['user']['first_name']} {result['student']['user']['last_name']}",
                        'st_id': result['student']['st_id'],
                        'score': float(result['score']),
                    })

                third_year['term_two'] = sorted(third_year['term_two'], key=lambda x: x['score'],
                                                reverse=True)

            result_three_three = ExamsSerializer(
                Exam.objects.filter(
                    school=staff.school,
                    academic_year=academic_year,
                    subject=subject_obj,
                    academic_term=3,
                    student_year=3,
                ),
                many=True).data
            if result_three_three:
                for result in result_three_three:
                    third_year['term_three'].append({
                        'name': f"{result['student']['user']['first_name']} {result['student']['user']['last_name']}",
                        'st_id': result['student']['st_id'],
                        'score': float(result['score']),
                    })

                third_year['term_three'] = sorted(third_year['term_three'], key=lambda x: x['score'],
                                                  reverse=True)

            data.append({
                'subject': subject['name'],
                'year_one': first_year,
                'year_two': second_year,
                'year_three': third_year,
            })

        return Response(data)

    else:
        return Response(status=401)