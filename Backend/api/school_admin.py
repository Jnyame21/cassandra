# Django
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.db.utils import IntegrityError as IntergrityError_unique_constraint
from django.core.files.storage import default_storage
from django.core.exceptions import SuspiciousOperation
from django.core.exceptions import ValidationError
from django.utils import timezone


# Document Manipulation
import pandas as pd
from openpyxl.styles import Font, Alignment, Protection
from openpyxl import Workbook, load_workbook

from api.models import *
from api.serializer import *
import random
import re
import io
from datetime import datetime

# Django Restframework
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


# Admin
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_sch_admin_data(request):
    sch_admin = request.user.staff

    if request.method == 'GET':
        # Students Data
        classes = ClasseWithSubjectsSerializer(Classe.objects.filter(school=sch_admin.school, is_active=True), many=True).data
        year_one_unsort = [x for x in classes if x['students_year'] == 1]
        year_one = sorted(year_one_unsort, key=lambda x: x['created_at'], reverse=True)
        year_two_unsort = [x for x in classes if x['students_year'] == 2]
        year_two = sorted(year_two_unsort, key=lambda x: x['created_at'], reverse=True)
        year_three_unsort = [x for x in classes if x['students_year'] == 3]
        year_three = sorted(year_three_unsort, key=lambda x: x['created_at'], reverse=True)

        clas_items = [class_item for class_item in sorted(classes, key=lambda y: y['created_at'], reverse=True)]
        class_names_data = []
        for item in clas_items:
            class_names_data.append(f"{item['name']} FORM-{item['students_year']}")

        # Staff Data
        departments = DepartmentSerializer(Department.objects.filter(school=sch_admin.school), many=True).data
        programs = ProgramSerializer(Program.objects.filter(schools=sch_admin.school), many=True).data
        department_names = [x['name'] for x in departments]
        programs_names = [x['name'] for x in programs]
        academic_years = AcademicYearSerializer(AcademicYear.objects.filter(school=sch_admin.school).order_by('-start_date'), many=True).data
        subject_names = []
        for program in programs:
            for subject in program['subjects']:
                if subject['name'] not in subject_names:
                    subject_names.append(subject['name'])

        # Head Data
        heads_data = HeadSerializer(Head.objects.filter(school=sch_admin.school), many=True).data

        return Response({
            'classes': {
                'year_one': year_one,
                'year_two': year_two,
                'year_three': year_three
            },
            'class_names': class_names_data,
            'departments': departments,
            'department_names': department_names,
            'heads': heads_data,
            'subjects': subject_names,
            'programs': programs_names,
            'academic_years': academic_years,
        })

    else:
        data = request.data
        if data['type'] == 'create-year':
            
            if not re.fullmatch("\d{4}/\d{4}", data['yearName']):
                return Response({
                    'ms': f"The academic year name must be in the format YYYY/YYY"
                }, status=201)
                
            current_year = AcademicYear.objects.get(school=sch_admin.school, name=data['year'])
            start_date = datetime.strptime(data['startDate'], "%Y-%m-%d").date()
            end_date = datetime.strptime(data['endDate'], "%Y-%m-%d").date()
            term_1_end_date = datetime.strptime(data['term1EndDate'], "%Y-%m-%d").date()
            term_2_start_date = datetime.strptime(data['term2StartDate'], "%Y-%m-%d").date()
            term_2_end_date = datetime.strptime(data['term2EndDate'], "%Y-%m-%d").date()
            current_date = timezone.now().date()

            duration = end_date - start_date
                
            if current_year.end_date >= current_date:
                return Response({
                    'ms': f"You cannot create a new academic year when the current academic year is still in progress"
                }, status=201)

            if current_year.end_date >= start_date:
                return Response({
                    'ms': f"The academic year start date must be greater than the current academic year end date"
                }, status=201)

            if duration.days < 6 * 30:
                return Response({
                    'ms': f"The duration between the academic year's start and end dates must be more than 6 months"
                }, status=201)

            try:
                AcademicYear.objects.get(school=sch_admin.school, name=data['yearName'])
                return Response({'ms': f"Academic year with name {data['yearName']} already exists"}, status=201)

            except AcademicYear.DoesNotExist:
                if start_date >= end_date:
                    return Response({
                        'ms': "The academic year end date must be greater than the start date"
                    }, status=201)

                elif term_1_end_date >= term_2_start_date:
                    return Response({
                        'ms': "Second semester/trimester start date must be greater than first semester/trimester end date"
                    }, status=201)

                elif term_2_start_date >= term_2_end_date:
                    return Response({
                        'ms': "Second semester/trimester end date must be greater than its start date"
                    }, status=201)

                elif not data['term3StartDate'] and term_2_end_date > end_date:
                    return Response({
                        'ms': "The academic year end date must be greater or equal to second semester end date"
                    }, status=201)

                if not data['term3StartDate'] and data['term3EndDate']:
                    return Response(
                        {'ms': "Third trimester start date cannot be empty when you specify its end date"},
                        status=201)

                if data['term3StartDate'] and data['term3StartDate'] != 'null':
                    if not data['term3EndDate']:
                        return Response(
                            {'ms': "Third trimester end date cannot be empty when you specify its start date"},
                            status=201)

                    term_3_start_date = datetime.strptime(data['term3StartDate'], "%Y-%m-%d").date()
                    term_3_end_date = datetime.strptime(data['term3EndDate'], "%Y-%m-%d").date()

                    if term_2_end_date >= term_3_start_date:
                        return Response({
                            'ms': "Third trimester start date must be greater than second trimester end date"
                        }, status=201)

                    elif term_3_start_date >= term_3_end_date:
                        return Response({'ms': "Third trimester end date must be greater than its end date"},
                                        status=201)

                    elif term_3_end_date > end_date:
                        return Response({
                            'ms': "The academic year end date must be greater or equal to trimester end date"
                        }, status=201)

                with transaction.atomic():
                    if data['term3StartDate'] and data['term3StartDate'] != 'null' and data['term3EndDate']:
                        academic_year = AcademicYear.objects.create(
                            name=data['yearName'],
                            school=sch_admin.school,
                            start_date=data['startDate'],
                            end_date=data['endDate'],
                            term_1_end_date=data['term2EndDate'],
                            term_2_start_date=data['term2StartDate'],
                            term_2_end_date=data['term2EndDate'],
                            term_3_start_date=data['term3StartDate'],
                            term_3_end_date=data['term3EndDate'],
                        )
                        academic_year.save()

                        new_academic_year = AcademicYear.objects.get(school=sch_admin.school, name=data['yearName'])
                        classes = Classe.objects.select_related('academic_years').prefetch_related('students').filter(
                            school=sch_admin.school,
                            is_active=True,
                        )

                        if classes.exists():
                            for clas in classes:
                                if clas.students_year == 3:
                                    clas.students_year = 4
                                    for student in clas.students.all():
                                        student.current_year = 4
                                        student.has_completed = True
                                        student.save()

                                    clas.is_active = False
                                    clas.save()

                                else:
                                    clas.students_year += 1
                                    clas.academic_years.add(new_academic_year)
                                    for student in clas.students.all():
                                        student.current_year += 1
                                        student.save()

                                    clas.save()

                        new_academic_data = AcademicYearSerializer(new_academic_year).data

                        return Response({
                            'ms': 'Academic year saved successfully',
                            'new_year': new_academic_data,
                        })

                    else:
                        academic_year = AcademicYear.objects.create(
                            name=data['yearName'],
                            school=sch_admin.school,
                            start_date=data['startDate'],
                            end_date=data['endDate'],
                            term_1_end_date=data['term2EndDate'],
                            term_2_start_date=data['term2StartDate'],
                            term_2_end_date=data['term2EndDate'],
                        )
                        academic_year.save()

                        new_academic_year = AcademicYear.objects.get(school=sch_admin.school, name=data['yearName'])
                        classes = Classe.objects.prefetch_related('students', 'academic_years').filter(
                            school=sch_admin.school,
                            is_active=True,
                        )

                        if classes.exists():
                            for clas in classes:
                                if clas.students_year == 3:
                                    clas.students_year = 4
                                    for student in clas.students.all():
                                        student.current_year = 4
                                        student.has_completed = True
                                        student.save()

                                    clas.is_active = False
                                    clas.save()

                                else:
                                    clas.students_year += 1
                                    clas.academic_years.add(new_academic_year)
                                    for student in clas.students.all():
                                        student.current_year += 1
                                        student.save()

                                    clas.save()

                        new_academic_data = AcademicYearSerializer(new_academic_year).data

                        return Response({
                            'ms': 'Academic year saved successfully',
                            'new_year': new_academic_data,
                        })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_staff(request):
    data = request.data
    sch_admin = request.user.staff
    if data['type'] == 'input-staff':
        department_name = data['departmentName']
        department = Department.objects.get(school=sch_admin.school, name=department_name)
        department_data = DepartmentSerializer(department).data

        user_no = random.randint(100, 999)
        username = f"{data['firstName'].replace(' ', '')[0].upper()}{data['lastName'].replace(' ', '').lower()}{user_no}"

        if Staff.objects.filter(school=sch_admin.school, staff_id=data['staffId']).exists():
            return Response({'ms': f"Staff with ID [ {data['staffId']} ] already exists"}, status=201)

        with transaction.atomic():
            try:
                user = User.objects.create_user(
                    username=username,
                    password=username,
                    first_name=data['firstName'].upper(),
                    last_name=data['lastName'].upper(),
                )
                user.save()

            except IntegrityError:
                return Response({'ms': 'A user with these details already exists'}, status=201)

            staff_user = User.objects.get(username=username)

            stf_obj = Staff.objects.create(
                user=staff_user,
                staff_id=data['staffId'],
                department=department,
                role='teacher',
                gender=data['gender'].upper(),
                dob=data['dob'].upper(),
                school=sch_admin.school
            )

            try:
                if isinstance(data['subjects'], str):
                    subjects = data['subjects'].split(',')
                    print(subjects)
                    for subject in subjects:
                        if subject != '':
                            subject_obj = Subject.objects.get(schools=sch_admin.school, name=subject)
                            try:
                                if subject_obj in department.subjects.all():
                                    stf_obj.subjects.add(subject_obj)
                                else:
                                    raise SuspiciousOperation

                            except SuspiciousOperation:
                                transaction.set_rollback(True)
                                return Response({'ms': f"The {department_name} department does not teach {subject}"},
                                                status=201)

                elif isinstance(data['subjects'], list):
                    for subject in data['subjects']:
                        subject_obj = Subject.objects.get(name=subject)
                        try:
                            if subject_obj in department.subjects:
                                stf_obj.subjects.add(subject_obj)
                            else:
                                raise SuspiciousOperation

                        except SuspiciousOperation:
                            transaction.set_rollback(True)
                            return Response({'ms': f"The {department_name} department does not teach {subject}"},
                                            status=201)

                stf_obj.save()

                staff_obj = Staff.objects.get(staff_id=data['staffId'])
                department.teachers.add(staff_obj)
                department.save()

                response_staff = SpecificStaffSerializer(staff_obj).data
                return Response({
                    'ms': 'Teacher successfully created and saved',
                    'staff': response_staff,
                    'department_name': department_data['name'],
                })

            except IntegrityError:
                return Response({'ms': 'Staff with these details already exists'}, status=201)

    elif data['type'] == 'get-staff-file':
        sch_admin_data = StaffSerializer(sch_admin).data
        department_name = data['departmentName']
        if Department.objects.filter(school=sch_admin.school, name=department_name).exists():
            wb = load_workbook('staticfiles/files/create_staff.xlsx')
            ws = wb.worksheets[0]
            filename = f"{department_name}.xlsx"
            ws.title = department_name
            byte_file = io.BytesIO()
            wb.save(byte_file)

            if settings.DEBUG:
                file_path = f"{get_school_folder(sch_admin_data['school']['name'])}/staff/{sch_admin_data['user']['username']}/{filename}"
                if default_storage.exists(file_path):
                    default_storage.delete(file_path)

                save_file = default_storage.save(file_path, byte_file)

                return Response({
                    'filename': f"{filename}.xlsx",
                    'file_path': f"http://localhost:8000{default_storage.url(save_file)}",
                })

            else:
                file_path = f"{get_school_folder(sch_admin_data['school']['name'])}/staff/{sch_admin_data['user']['username']}/{filename}"
                if default_storage.exists(file_path):
                    default_storage.delete(file_path)

                save_file = default_storage.save(file_path, byte_file)

                return Response({
                    'filename': f"{filename}.xlsx",
                    'file_path': default_storage.url(save_file),
                })

    elif data['type'] == 'upload-staff-file':
        department_name = data['departmentName']
        wb = load_workbook(data['file'])
        if department_name == wb.sheetnames[0]:
            wb.close()
            df = pd.read_excel(data['file'], sheet_name=department_name)
            df_data = df.iloc[3:, :6].dropna().values.tolist()

            existing_staff = Staff.objects.filter(school=sch_admin.school,
                                                  staff_id__in=[stf[2] for stf in df_data]).first()
            if existing_staff:
                return Response({
                    'ms': f"Staff with ID [ {SpecificStaffSerializer(existing_staff).data['staff_id']} ] already exists"},
                    status=201)

            with transaction.atomic():
                staff_ids = []
                department = Department.objects.get(school=sch_admin.school, name=department_name)
                user_no = random.randint(100, 999)

                for stf in df_data:
                    username = f"{stf[0].replace(' ', '')[0].upper()}{stf[1].replace(' ', '').lower()}{user_no}"
                    user = User.objects.create_user(
                        username=username,
                        password=username,
                        first_name=stf[0].upper(),
                        last_name=stf[1].upper(),
                    )
                    user.save()

                    staff_user = User.objects.get(username=username)

                    if str(stf[3]).upper() == 'MALE' or str(stf[3]).upper() == 'FEMALE':
                        pass

                    else:
                        transaction.set_rollback(True)
                        return Response({
                            'ms': f"{stf[3]} is not a valid gender. Valid values are 'MALE' or 'FEMALE'. Recheck the gender for {stf[0]} {stf[1]} in the file"},
                            status=201)

                    try:
                        stf_obj = Staff.objects.create(
                            user=staff_user,
                            staff_id=stf[2],
                            role='teacher',
                            department=department,
                            gender=stf[3].upper(),
                            dob=stf[4],
                            school=sch_admin.school
                        )

                    except IntergrityError_unique_constraint:
                        return Response({
                            'ms': f"{stf[0]} {stf[1]}'s staff ID matches with another teacher's staff ID. Recheck that the ID {stf[2]} is unique in the file"
                        }, status=201)

                    except ValidationError:
                        transaction.set_rollback(True)
                        return Response({
                            'ms': f"{stf[4]} is not a valid date, Recheck the date of birth of {stf[0]} {stf[1]} in the file"},
                            status=201)

                    subjects = stf[5].split(',')
                    for subject in subjects:
                        try:
                            subject_obj = Subject.objects.get(schools=sch_admin.school, name=subject.strip().upper())
                            if subject_obj in department.subjects.all():
                                stf_obj.subjects.add(subject_obj)
                            else:
                                raise SuspiciousOperation

                        except Subject.DoesNotExist:
                            transaction.set_rollback(True)
                            return Response({
                                'ms': f"{subject} is not a valid subject name. Recheck the subject(s) for {stf[0]} {stf[1]} in the file"
                            }, status=201)

                        except SuspiciousOperation:
                            transaction.set_rollback(True)
                            return Response({
                                'ms': f"The {department_name} department does not teach {subject}. Recheck the subject(s) of {stf[0]} {stf[1]}"
                            }, status=201)

                    stf_obj.save()

                    staff_ids.append(stf[2])

                for staff_id in staff_ids:
                    staff_obj = Staff.objects.get(school=sch_admin.school, staff_id=staff_id)
                    department.teachers.add(staff_obj)

                department.save()

            department_data = DepartmentSerializer(Department.objects.get(school=sch_admin.school, name=department_name)).data
            return Response({
                'ms': 'File uploaded and teachers saved successfully',
                'data': department_data,
            })

        else:
            return Response({'ms': 'The first sheet name must be the same as the selected department'}, status=201)

    elif data['type'] == 'delete-staff':
        staff_data = SpecificStaffSerializer(Staff.objects.get(school=sch_admin.school, staff_id=data['staffId'])).data
        user = User.objects.get(username=staff_data['user']['username'])
        with transaction.atomic():
            # delete user object
            user.delete()
            teacher = Staff.objects.get(staff_id=data['staffId'])
            department = Department.objects.get(school=sch_admin.school, teachers=teacher)
            # remove staff from department
            department.teachers.remove(teacher)
            department.save()
            # delete staff object
            teacher.delete()

        return Response({
            'department_name': DepartmentSerializer(department).data['name'],
        })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_head(request):
    data = request.data
    sch_admin = request.user.staff
    if data['type'] == 'create-head':
        user_no = random.randint(100, 999)
        username = f"{data['firstName'].replace(' ', '')[0].upper()}{data['lastName'].replace(' ', '').lower()}{user_no}"

        if Head.objects.filter(school=sch_admin.school, head_id=data['headId']).exists():
            return Response({'ms': f"Head with ID [ {data['headId']} ] already exists"}, status=201)

        with transaction.atomic():
            try:
                user = User.objects.create_user(
                    username=username,
                    password=username,
                    first_name=data['firstName'].upper(),
                    last_name=data['lastName'].upper(),
                )
                user.save()

            except IntegrityError:
                return Response({'ms': 'A user with these details already exists'}, status=201)

            head_user = User.objects.get(username=username)
            head_obj = Head.objects.create(
                user=head_user,
                head_id=data['headId'],
                role=data['role'].lower().replace(' ', '_'),
                gender=data['gender'].upper(),
                dob=data['dob'].upper(),
                school=sch_admin.school
            )

            try:
                head_obj.save()

                new_head = Head.objects.get(head_id=data['headId'])

                response_head = HeadSerializer(new_head).data
                return Response(response_head)

            except IntegrityError:
                return Response({'ms': 'Head with these details already exists'}, status=201)

    elif data['type'] == 'delete-head':
        head = Head.objects.select_related('user').get(school=sch_admin.school, head_id=data['headId'])
        user = User.objects.get(username=head.user.username)
        with transaction.atomic():
            # delete user object
            user.delete()
            # delete head object
            head.delete()

        return Response(status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_students(request):
    sch_admin = request.user.staff
    data = request.data
    
    if data['type'] == 'create-class':
        program = Program.objects.get(name=data['program'])
        academic_year = AcademicYear.objects.get(school=sch_admin.school, name=data['year'])
        class_name = f"{data['year'].split('/')[0]}-{data['className'].replace(' ', '-')}"
        program_data = ProgramSerializer(program).data
        students_year = int(data['studentsYear'])
        program_subjects = [sub['name'] for sub in program_data['subjects']]
        subjects = data['subjects'].split(',')

        try:
            Classe.objects.get(school=sch_admin.school, name=class_name.upper())
            return Response({'ms': 'Class with this name already exists'}, status=201)

        except Classe.DoesNotExist:
            for subject in subjects:
                if subject not in program_subjects:
                    return Response({'ms': f"Students enrolled in {data['program']} do not study {subject}"},
                                    status=201)

            with transaction.atomic():
                clas = Classe.objects.create(
                    school=sch_admin.school,
                    program=program,
                    name=class_name.upper(),
                    students_year=students_year,
                    date_enrolled=data['enrollmentDate'],
                    completion_date=data['completionDate']
                )

                clas.academic_years.add(academic_year)
                for subject in subjects:
                    if subject != '':
                        subject_obj = Subject.objects.get(schools=sch_admin.school, name=subject)
                        clas.subjects.add(subject_obj)

                clas.save()

                new_class = ClasseWithSubjectsSerializer(Classe.objects.get(school=sch_admin.school, name=class_name.upper())).data
                return Response({
                    'ms': "Class successfully created",
                    'new_class': new_class,
                    'class_name': f"{class_name.upper()} FORM-{new_class['students_year']}"
                })

    if data['type'] == 'input-student':
        class_name = data['className'].split()[0]
        clas = Classe.objects.select_related('program').get(school=sch_admin.school, name=class_name)
        class_data = ClasseSerializer(clas).data

        user_no = random.randint(100, 999)
        username = f"{data['firstName'].replace(' ', '')[0].upper()}{data['lastName'].replace(' ', '').lower()}{user_no}"

        existing_student_ids = set(Student.objects.filter(
            school=sch_admin.school,
        ).values_list('st_id', flat=True))

        st_id = data['studentId']
        if st_id in existing_student_ids:
            return Response({'ms': f'Student with ID {st_id} already exists'}, status=201)

        with transaction.atomic():
            try:
                user = User.objects.create_user(
                    username=username,
                    password=username,
                    first_name=data['firstName'].upper(),
                    last_name=data['lastName'].upper(),
                )
                user.save()

            except IntegrityError:
                return Response({'ms': 'A user with these details already exists'}, status=201)

            st_user = User.objects.get(username=username)

            student = Student.objects.create(
                user=st_user,
                program=clas.program,
                st_class=clas,
                current_year=class_data['students_year'],
                date_enrolled=class_data['date_enrolled'],
                st_id=st_id,
                gender=data['gender'].upper(),
                dob=data['dob'].upper(),
                school=sch_admin.school
            )

            try:
                student.save()
                st_obj = Student.objects.get(school=sch_admin.school, st_id=st_id)
                clas.students.add(st_obj)
                clas.save()

                response_student = SpecificStudentSerializer(st_obj).data
                return Response({
                    'ms': 'student successfully created and saved',
                    'student': response_student,
                    'year': 'yearOne' if class_data['students_year'] == 1 else ('yearTwo' if class_data['students_year'] == 2 else 'yearThree'),
                    'class_name': class_data['name'],
                })

            except IntegrityError:
                return Response({'ms': 'student with these details already exists'}, status=201)

    elif data['type'] == 'get-students-file':
        sch_admin_data = StaffSerializer(sch_admin).data
        class_name = data['className'].split()[0]
        clas = Classe.objects.filter(school=sch_admin.school, name=class_name).first()
        if clas:
            clas_data = ClasseSerializer(clas).data
            wb = load_workbook('staticfiles/files/students_admission.xlsx')
            ws = wb.worksheets[0]
            filename = f"{clas_data['name']}-FORM-{clas_data['students_year']}.xlsx"
            ws.title = f"{clas_data['name']} FORM-{clas_data['students_year']}"
            byte_file = io.BytesIO()
            wb.save(byte_file)

            if settings.DEBUG:
                file_path = f"{get_school_folder(sch_admin_data['school']['name'])}/staff/{sch_admin_data['user']['username']}/{filename}"
                if default_storage.exists(file_path):
                    default_storage.delete(file_path)

                save_file = default_storage.save(file_path, byte_file)

                return Response({
                    'filename': f"{filename}.xlsx",
                    'file_path': f"http://localhost:8000{default_storage.url(save_file)}",
                })

            else:
                file_path = f"{get_school_folder(sch_admin_data['school']['name'])}/staff/{sch_admin_data['user']['username']}/{filename}"
                if default_storage.exists(file_path):
                    default_storage.delete(file_path)

                save_file = default_storage.save(file_path, byte_file)

                return Response({
                    'filename': f"{filename}.xlsx",
                    'file_path': default_storage.url(save_file),
                })

    elif data['type'] == 'upload-students-file':
        class_name = data['className'].split()[0]
        wb = load_workbook(data['file'])
        if data['className'] == wb.sheetnames[0]:
            wb.close()
            df = pd.read_excel(data['file'], sheet_name=data['className'])
            df_data = df.iloc[2:, :5].dropna().values.tolist()

            existing_student_ids = set(Student.objects.filter(
                school=sch_admin.school,
            ).values_list('st_id', flat=True))

            with transaction.atomic():
                clas = Classe.objects.select_related('program').get(school=sch_admin.school, name=class_name)
                user_no = random.randint(100, 999)

                for st in df_data:
                    if str(st[2]) in existing_student_ids:
                        transaction.set_rollback(True)
                        return Response({'ms': f"Student with ID {st[2]} already exists"}, status=201)
                    
                    username = f"{st[0].replace(' ', '')[0].upper()}{st[1].replace(' ', '').lower()}{user_no}"
                    user = User.objects.create_user(
                        username=username,
                        password=username,
                        first_name=st[0].upper(),
                        last_name=st[1].upper(),
                    )
                    user.save()

                    st_user = User.objects.get(username=username)

                    try:
                        student = Student.objects.create(
                            user=st_user,
                            program=clas.program,
                            st_id=st[2],
                            current_year=clas.students_year,
                            st_class=clas,
                            date_enrolled=clas.date_enrolled,
                            gender=st[3].upper(),
                            dob=st[4],
                            school=sch_admin.school,
                        )
                        student.save()
                        clas.students.add(student)

                    except ValidationError:
                        transaction.set_rollback(True)
                        return Response({
                            'ms': f"{st[4]} is not a valid date, recheck the date of birth of {st[0]} {st[1]} in the file"},
                            status=201)
                        
                    except IntegrityError:
                        transaction.set_rollback(True)
                        return Response({
                            'ms': f"Student ID {st[2]} has been assigned to two students, recheck the students ids in the file"},
                            status=201)

                clas.save()

            class_data = ClasseSerializer(Classe.objects.get(school=sch_admin.school, name=class_name)).data
            return Response({
                'ms': 'File uploaded and students saved successfully',
                'data': class_data,
                'year': 'yearOne' if class_data['students_year'] == 1 else (
                    'yearTwo' if class_data['students_year'] == 2 else 'yearThree'),
            })

        else:
            return Response({'ms': 'The first sheet name must be same as the selected class'}, status=201)

    elif data['type'] == 'delete-student':
        st_data = SpecificStudentSerializer(Student.objects.get(st_id=data['stId'])).data
        class_data = ClasseSerializer(Classe.objects.get(name=data['className'])).data
        user = User.objects.get(username=st_data['user']['username'])

        with transaction.atomic():
            # delete user object
            user.delete()
            student = Student.objects.get(st_id=data['stId'])
            clas = Classe.objects.get(name=data['className'])
            # remove student from class
            clas.students.remove(student)
            clas.save()
            # delete student object
            student.delete()

        return Response({
            'class_name': class_data['name'],
            'year': 'yearOne' if class_data['students_year'] == 1 else (
                'yearTwo' if class_data['students_year'] == 2 else 'yearThree'),
        })

    elif data['type'] == 'delete-subject':
        subject = Subject.objects.get(name=data['subject'])
        clas = Classe.objects.get(school=sch_admin.school, name=data['className'])
        class_data = ClasseWithoutStudentsSerializer(clas).data

        with transaction.atomic():
            # remove subject from class
            clas.subjects.remove(subject)
            clas.save()

        return Response({
            'class_name': class_data['name'],
            'year': 'yearOne' if class_data['students_year'] == 1 else (
                'yearTwo' if class_data['students_year'] == 2 else 'yearThree'),
        })

    elif data['type'] == 'delete-class':
        clas = Classe.objects.get(school=sch_admin.school, name=data['className'])

        with transaction.atomic():
            # remove subject from class
            clas.delete()

        return Response(status=200)
    
    

