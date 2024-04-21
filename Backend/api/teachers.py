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


# TEACHER
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def teacher_students_attendance(request):
    teacher = request.user.staff
    if request.method == 'POST':
        data = request.data
        academic_year = AcademicYear.objects.get(school=teacher.school, name=data['year'])
        subject = Subject.objects.get(schools=teacher.school, name=data['subject'])
        students_class = Classe.objects.prefetch_related('students').get(school=teacher.school, name=data['className'])
        if data['type'] == 'create':
            students = data['absentStudents'].split(',')
            try:
                existing_attendance = StudentAttendance.objects.get(
                    school=teacher.school,
                    date=data['date'],
                    teacher=teacher,
                    subject=subject,
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
                        subject=subject,
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
                    subject=subject,
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
                        subject=subject,
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

    else:
        academic_year = AcademicYear.objects.get(school=teacher.school, name=request.GET.get('year'))
        term = request.GET.get('term')
        subject_assignments = SubjectAssignment.objects.prefetch_related('subject').filter(
            school=teacher.school,
            academic_year=academic_year,
            academic_term=term,
            teacher=teacher,
        )
        students_attendance = []
        if subject_assignments.exists():
            for assign in subject_assignments:
                assign_data = SubjectAssignmentWithoutStudentsSerializer(assign).data
                attendance = StudentsAttendanceSerializer(StudentAttendance.objects.filter(
                    school=teacher.school,
                    academic_year=academic_year,
                    academic_term=term,
                    students_class=assign.students_class,
                    subject=assign.subject
                ).order_by('-date'), many=True).data

                students_attendance.append({
                    'subject': assign_data['subject']['name'],
                    'class_name': assign_data['students_class']['name'],
                    'students_year': assign_data['students_class']['students_year'],
                    'attendance': attendance,
                })

        return Response(students_attendance)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_teacher_subject_assignments(request):
    sch = request.user.staff.school
    try:
        year = request.GET.get('year')
        teacher = request.user.staff
        academic_year = AcademicYear.objects.get(school=sch, name=year)
        term1_subjects_assignments = SubjectAssignmentSerializer(
            SubjectAssignment.objects.filter(teacher=teacher, academic_year=academic_year, academic_term=1), many=True)
        term2_subjects_assignments = SubjectAssignmentSerializer(
            SubjectAssignment.objects.filter(teacher=teacher, academic_year=academic_year, academic_term=2), many=True)
        term3_subjects_assignments = SubjectAssignmentSerializer(
            SubjectAssignment.objects.filter(teacher=teacher, academic_year=academic_year, academic_term=3), many=True)
        return Response(
            {'subject_assignments': {
                'term1': term1_subjects_assignments.data, 
                'term2': term2_subjects_assignments.data, 
                'term3': term3_subjects_assignments.data
                }
            }
        )
    except request.user.staff.DoesNotExist:
        return Response(status=401)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def teacher_student_results(request):
    sch = request.user.staff.school
    try:
        teacher = request.user.staff
        staff = StaffSerializer(teacher).data
        if request.method == 'POST':
            year = request.data['year']
            term = int(request.data['term'])
            subject = request.data['subject']
            academic_year = AcademicYear.objects.get(school=sch, name=year)
            if request.data['score'] == 'generate':
                st_class = request.data['students_class']
                st_year = request.data['students_year']
                students = request.data['st_id']
                data = [
                    ['STUDENT NAME', 'STUDENT ID', 'SCORE']
                ]

                if len(students) == 0:
                    return Response({
                        'ms': "You have already uploaded results for students in this class",
                    }, status=201)
                    
                for st in students:
                    row = [st['name'], st['st_id'], 'not set']
                    data.append(row)

                wb = Workbook()
                ws = wb.active
                ws.title = subject

                ws.merge_cells('A1:I3')

                if sch.semesters:
                    ws['A1'].value = f"SUBJECT: [{subject}] - ACADEMIC YEAR: [{year}] - CLASS: [{st_class} FORM {st_year}] - SEMESTER: [{term}]"
                else:
                    ws['A1'].value = f"SUBJECT: [{subject}] - ACADEMIC YEAR: [{year}] - CLASS: [{st_class} FORM {st_year}] - TRIMESTER: [{term}]"

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
                ws.column_dimensions['B'].width = 40
                ws.column_dimensions['C'].width = 25
                ws.column_dimensions['D'].width = 25

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

                filename = f"{subject.replace(' ', '-')}-{st_class}-FORM-{st_year}-Results.xlsx"
                byte_file = io.BytesIO()
                wb.save(byte_file)

                if settings.DEBUG:
                    file_path = f"{get_school_folder(staff['school']['name'])}/staff/{staff['user']['username']}/{filename}"
                    if default_storage.exists(file_path):
                        default_storage.delete(file_path)

                    save_file = default_storage.save(file_path, byte_file)

                    return Response({
                        'filename': filename,
                        'message': 'File generated successfully',
                        'file_path': f"http://localhost:8000{default_storage.url(save_file)}",
                    })

                else:
                    file_path = f"media/{get_school_folder(staff['school']['name'])}/staff/{staff['user']['username']}/{filename}"
                    if default_storage.exists(file_path):
                        default_storage.delete(file_path)

                    save_file = default_storage.save(file_path, byte_file)

                    return Response({
                        'filename': filename,
                        'message': 'File generated successfully',
                        'file_path': default_storage.url(save_file),
                    })

            elif request.data['score'] == 'upload':
                wb = load_workbook(request.data['st_id'])
                ws = wb.active
                ws.protection = False

                if sch.semesters:
                    if ws[
                        'A1'].value != f"SUBJECT: [{subject}] - ACADEMIC YEAR: [{year}] - CLASS: [{request.data['students_class']} FORM {request.data['students_year']}] - SEMESTER: [{term}]":
                        return Response({'message': "Invalid file. You must upload the same file you generated."},
                                        status=201)
                else:
                    if ws[
                        'A1'].value != f"SUBJECT: [{subject}] - ACADEMIC YEAR: [{year}] - CLASS: [{request.data['students_class']} FORM {request.data['students_year']}] - TRIMESTER: [{term}]":
                        return Response({'message': "Invalid file. You must upload the same file you generated."},
                                        status=201)

                df = pd.read_excel(request.data['st_id'])
                uncleaned_data = df.values.tolist()
                first_clean_data = []
                for row in uncleaned_data:
                    first_clean_row = [item for item in row if not pd.isna(item)]
                    if first_clean_row:
                        first_clean_data.append(first_clean_row)

                first_clean_data.pop(0)
                if not first_clean_data:
                    return Response({'message': f"There are no students data in the uploaded file"}, status=201)

                students_results = [[float(item) if isinstance(item, (int, float)) else item for item in row] for row in
                                    first_clean_data]
                for row in students_results:
                    for item in row:
                        if row.index(item) == 2 and not isinstance(item, float):
                            return Response({
                                'message': f"You have not assigned a score to {row[0]}"},
                                status=201)
                        elif row.index(item) == 2 and item > 100:
                            return Response({
                                'message': f"Scores cannot be more than 100. Recheck the score for {row[0]} in the file"},
                                status=201)
                        elif row.index(item) == 2 and item < 0:
                            return Response({
                                'message': f"Scores cannot be negative. Recheck the score for {row[0]} in the file"},
                                status=201)

                students_id = []
                students_score = []
                for row in students_results:
                    for item in row:
                        if row.index(item) == 1:
                            students_id.append(item)
                        if row.index(item) == 2:
                            students_score.append(item)

                students_class = Classe.objects.get(
                    school=sch,
                    name=request.data['students_class'],
                    students_year=request.data['students_year']
                )
                with transaction.atomic():
                    for st_id, st_score in zip(students_id, students_score):
                        if students_class.students.filter(st_id=st_id).exists():
                            st_subject = Subject.objects.get(name=subject)
                            if students_class.subjects.filter(name=st_subject.name).exists():
                                st = Student.objects.get(st_id=st_id)
                                try:
                                    st_result = Result.objects.create(
                                        student=st,
                                        subject=st_subject,
                                        teacher=teacher,
                                        score=st_score,
                                        student_year=st.current_year,
                                        academic_year=academic_year,
                                        academic_term=term,
                                        school=sch
                                    )
                                    st_result.save()

                                except IntegrityError:
                                    return Response(
                                        {
                                            'message': f"You have already uploaded result for student with ID {st.st_id}"
                                        }, status=201)

                            else:
                                transaction.set_rollback(True)
                                return Response(
                                    {
                                        'message': f"Student does not study {subject}"
                                    },
                                    status=201)

                        else:
                            transaction.set_rollback(True)
                            return Response(
                                {
                                    'message': f"Students must be in {request.data['students_class']} {request.data['students_year']}"
                                },
                                status=201)

                    data = teacher_results_upload(teacher, academic_year, term)
                    return Response({'data': data, 'message': "Results uploaded and saved successfully"}, status=200)

            elif request.data['score'] == 'edit':
                student_classe = Classe.objects.get(
                    school=sch, name=request.data['student_class'],
                    students_year=request.data['student_year']
                )
                student_subject = Subject.objects.get(schools=sch, name=request.data['subject'])
                st = student_classe.students.get(st_id=request.data['st_id'])
                result = Result.objects.get(
                    student=st,
                    teacher=teacher,
                    subject=student_subject,
                    academic_year=academic_year,
                    academic_term=term,
                    school=sch
                )
                with transaction.atomic():
                    try:
                        mark = float(request.data['mark'])
                        result.score = mark
                        result.save()

                    except ValueError:
                        return Response({'message': "The score must be a number"}, status=202)

                data = teacher_results_upload(teacher, academic_year, term)
                return Response(data, status=200)

            else:
                score = float(request.data['score'])
                academic_year = AcademicYear.objects.get(school=sch, name=year)

                if isinstance(request.data['st_id'], list):
                    students_id = request.data['st_id']
                    for st_id in students_id:
                        student = Student.objects.get(school=sch, st_id=st_id)
                        if student.program.subjects.filter(name=subject).exists():
                            subject_obj = Subject.objects.get(name=subject)
                            new_result = Result.objects.create(
                                student=student,
                                subject=subject_obj,
                                student_year=student.current_year,
                                teacher=teacher,
                                score=score,
                                academic_year=academic_year,
                                academic_term=term,
                                school=sch
                            )
                            new_result.save()

                        else:
                            return Response(status=404)

                    response_data = teacher_results_upload(teacher, academic_year, term)
                    return Response(response_data)

                elif isinstance(request.data['st_id'], str):
                    student_id = request.data['st_id']
                    student = Student.objects.get(st_id=student_id)
                    if student.program.subjects.filter(name=subject).exists():
                        subject_obj = Subject.objects.get(name=subject)
                        new_result = Result.objects.create(
                            student=student,
                            subject=subject_obj,
                            teacher=teacher,
                            score=score,
                            student_year=student.current_year,
                            academic_year=academic_year,
                            academic_term=term,
                            school=sch
                        )
                        new_result.save()

                        response_data = teacher_results_upload(teacher, academic_year, term)
                        return Response(response_data)

                    else:
                        return Response(status=404)
                else:
                    return Response(status=401)

        else:
            year = request.GET.get('year')
            term = request.GET.get('term')
            academic_year = AcademicYear.objects.get(school=sch, name=year)
            response_data = teacher_results_upload(teacher, academic_year, term)

            return Response(response_data)

    except request.user.staff.DoesNotExist:
        return Response(status=401)


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

            # Year One Student Results
            result_one_one = ResultsSerializer(
                Result.objects.filter(
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

            result_one_two = ResultsSerializer(
                Result.objects.filter(
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

            result_one_three = ResultsSerializer(
                Result.objects.filter(
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

            # Year Two Students Results
            result_two_one = ResultsSerializer(
                Result.objects.filter(
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

            result_two_two = ResultsSerializer(
                Result.objects.filter(
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

            result_two_three = ResultsSerializer(
                Result.objects.filter(
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

            # Year Three Students Results
            result_three_one = ResultsSerializer(
                Result.objects.filter(
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

            result_three_two = ResultsSerializer(
                Result.objects.filter(
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

            result_three_three = ResultsSerializer(
                Result.objects.filter(
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