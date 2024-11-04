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
import json

# Django Restframework
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


# Admin
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def school_admin_data(request):
    sch_admin = request.user.staff
    school = sch_admin.school

    if request.method == 'GET':
        academic_years = AcademicYearSerializer(AcademicYear.objects.filter(school=school).order_by('-start_date'), many=True).data
        student_classes = Classe.objects.filter(school=school).order_by('students_year')
        student_classes_data = ClassesSerializerOne(student_classes, many=True).data
        linked_classes = AdminLinkedClassSerializer(LinkedClasse.objects.filter(school=school), many=True).data
        departments = []
        programs = []
        if school.level.name == 'SHS':
            departments_data = DepartmentNameSerializer(Department.objects.filter(school=school), many=True).data
            departments = [_department['name'] for _department in departments_data]
            programs_data = ProgramNameSerializer(Program.objects.filter(schools=school), many=True).data
            programs = [_program['name'] for _program in programs_data]
            
        staff = StaffSerializerOne(Staff.objects.filter(school=school, is_active=True), many=True).data
        subjects = SubjectsSerializer(Subject.objects.filter(schools=school), many=True).data
        subject_names = [_subject['name'] for _subject in subjects]
        
        return Response({
            'classes': student_classes_data,
            #     'year_one': year_one,
            #     'year_two': year_two,
            #     'year_three': year_three
            # },
            # 'class_names': class_names_data,
            'departments': departments,
            # 'department_names': department_names,
            # 'heads': heads_data,
            'subjects': subject_names,
            'staff': staff,
            'programs': programs,
            'academic_years': academic_years,
            'linked_classes': linked_classes,
        }, status=200)
    
    elif request.method == 'POST':  
        data = request.data
        if data['type'] == 'assignClassHeadTeacher':
            staff_id = data['teacherId']
            new_head_teacher = Staff.objects.get(school=school, staff_id=staff_id)
            students_class = Classe.objects.get(school=school, name=data['studentsClass'])
            with transaction.atomic():
                try:
                    students_class.head_teacher = new_head_teacher
                    students_class.save()
                except Exception as e:
                    transaction.set_rollback(True)
                    return Response(status=400)
            
            new_head_teacher_data = StaffSerializerThree(new_head_teacher).data
            return Response(new_head_teacher_data, status=200)
        

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def school_admin_linked_class(request):
    sch_admin = request.user.staff
    school = sch_admin.school
    data = request.data
    from_class = Classe.objects.select_related('program').get(school=school, name=data['fromClass'])
    to_class = Classe.objects.select_related('program').get(school=school, name=data['toClass'])
    
    if data['type'] == 'create':
        if from_class.students_year >= to_class.students_year:  
            return Response({'message': f"The class the student will be promoted to must be above this class, {from_class.name}"}, status=400)
        
        if (from_class.program and not to_class.program) or (from_class.program and to_class.program != from_class.program):
            return Response({'message': "The two classes must be under the same program"}, status=400)
        
        existing_linked_class = LinkedClasse.objects.filter(school=school, from_class=from_class).exists()
        if existing_linked_class:
            return Response({'message': f"You have already linked a class to {from_class.name}"}, status=400)
        
        linked_class = LinkedClasse.objects.create(
            school=school,
            from_class=from_class,
            to_class=to_class,
        )
        with transaction.atomic():
            try:
                linked_class.save()
            except IntegrityError:
                transaction.set_rollback(True)
                return Response({'message': f'You have already linked a class to {to_class.name}'}, status=400)
            except Exception as e:
                transaction.set_rollback(True)
                return Response(status=400)
        
        new_linked_class_data = AdminLinkedClassSerializer(LinkedClasse.objects.get(school=school, from_class=from_class, to_class=to_class)).data
        return Response(new_linked_class_data, status=200)
    
    elif data['type'] == 'delete':
        linked_class = LinkedClasse.objects.get(school=school, from_class=from_class, to_class=to_class)
        with transaction.atomic():
            try:
                linked_class.delete()
            except Exception as e:
                transaction.set_rollback(True)
                return Response(status=400)
        
        return Response(status=200)
    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def school_admin_academic_years(request):
    sch_admin = request.user.staff
    school = sch_admin.school
    data = request.data
    
    def parse_date(date:str):
        return datetime.strptime(date, "%Y-%m-%d").date()
                
    if data['type'] == 'create':
        new_year_name = data['newYear']
        current_year = AcademicYear.objects.get(school=school, name=data['year'])
        start_date = parse_date(data['startDate'])
        end_date = parse_date(data['endDate'])
        students_graduation_date = parse_date(data['graduationDate']) if data['graduationDate'] else None 
        repeated_students_ids = json.loads(data['repeatedStudents'])
        period_division = int(data['periodDivision'])
        term_1_end_date = parse_date(data['term1EndDate'])
        term_2_start_date = parse_date(data['term2StartDate'])
        term_2_end_date = parse_date(data['term2EndDate'])
        term_3_start_date = None if period_division == 2 else parse_date(data['term3StartDate'])
        term_3_end_date = None if period_division == 2 else parse_date(data['term3EndDate'])
        period_division_name = data['periodDivisionName']
        current_date = timezone.now().date()
        duration = end_date - start_date
        
        def validate_dates():
            validation_error = None
            if current_year.end_date >= current_date:
                validation_error = "You cannot create a new academic year when the current academic year is still in progress"
        
            elif current_year.end_date >= start_date:
                validation_error = f"The academic year start date must be greater than the current academic year[ {current_year.name} ] end date"

            elif duration.days < 6 * 30:
                validation_error = "The duration between the academic year's start and end dates must be more than 6 months"

            elif start_date >= end_date:
                validation_error = "The academic year end date must be greater than the start date"

            elif term_1_end_date >= term_2_start_date:
                validation_error = f"{period_division_name} 2 start date must be greater than {period_division_name} 1 end date"

            elif term_2_start_date >= term_2_end_date:
                validation_error = f"{period_division_name} 2 end date must be greater than its start date"

            elif period_division == 2 and term_2_end_date > end_date:
                validation_error = f"The academic year end date must be greater or equal to {period_division} 2 end date"
                    
            elif period_division == 3:
                if term_2_end_date >= term_3_start_date:
                    validation_error = f"{period_division} 3 start date must be greater than {period_division} 2 end date"

                elif term_3_start_date >= term_3_end_date:
                    validation_error = f"{period_division} 3 end date must be greater than its start date"

                elif term_3_end_date > end_date:
                    validation_error = f"The academic year end date must be greater or equal to {period_division} 3 end date"
                    
            return validation_error
    
        def create_new_academic_year():
            academic_year = AcademicYear.objects.create(
                name=new_year_name,
                school=school,
                start_date=start_date,
                end_date=end_date,
                term_1_end_date=term_1_end_date,
                term_2_start_date=term_2_start_date,
                term_2_end_date=term_2_end_date,
                term_3_start_date=term_3_start_date,
                term_3_end_date=term_3_end_date,
                students_graduation_date=students_graduation_date,
            )
            academic_year.save()
            new_academic_year = AcademicYear.objects.get(school=school, name=new_year_name)
            return new_academic_year
        
        invalid_validation = validate_dates()
        if invalid_validation:
            return Response({'message': invalid_validation}, status=400)
        try:
            AcademicYear.objects.get(school=school, name=new_year_name)
            return Response({'message': f"Academic year with name {new_year_name} already exists"}, status=400)
        except AcademicYear.DoesNotExist:
            with transaction.atomic():
                try:
                    repeated_students = Student.objects.filter(school=school, st_id__in=repeated_students_ids)
                    all_repeated_students = []
                    for _student in repeated_students:
                        _student.repeated = True
                        all_repeated_students.append(_student)
                        
                    Student.objects.bulk_update(all_repeated_students, ['repeated'])
                    new_academic_year = create_new_academic_year()
                    classes = Classe.objects.prefetch_related('students').filter(school=school)
                    old_classes_to_update = []
                    new_classes_to_update = []
                    graduation_classes_to_create = []
                    graduated_students = []
                    promoted_students = []
                    repeated_students_to_update = []
                    years_to_complete = school.level.years_to_complete
                    for _class in classes:
                        try:
                            students = _class.students.all()
                            if _class.students_year == years_to_complete:
                                graduation_class = GraduatedClasse.objects.create(
                                    school=school,
                                    name=f"{_class.name} CLASS OF {current_year.name}",
                                    graduated_class_name=_class.name,
                                    graduation_year=current_year,
                                    students_year=years_to_complete,
                                    head_teacher=_class.head_teacher,
                                    program=_class.program,
                                )
                                graduation_class.subjects.add(_class.subjects.all())
                                for _student in students:
                                    if _student.repeated:
                                        _student.repeated_academic_years.add(current_year)
                                        _student.academic_years.add(new_academic_year)
                                        _student.repeated = False
                                        repeated_students_to_update.append(_student)
                                    else:
                                        _student.current_year += 1
                                        _student.has_completed = True
                                        _student.graduation_date = current_year.students_graduation_date
                                        _student.graduation_year = current_year
                                        _class.students.remove(_student)
                                        graduated_students.append(_student)
                                        graduation_class.students.add(_student)
                                graduation_classes_to_create.append(graduation_class)
                            else:
                                linked_class = LinkedClasse.objects.prefetch_related('to_class__students').get(school=school, from_class=_class)
                                new_students_class = linked_class.to_class
                                for _student in students:
                                    if _student.repeated:
                                        _student.repeated_academic_years.add(current_year)
                                        _student.repeated = False
                                        repeated_students_to_update.append(_student)
                                    else:
                                        _student.current_year += 1
                                        _student.linked_classes.add(linked_class)
                                        _student.academic_years.add(new_academic_year)
                                        _student.st_class = new_students_class
                                        new_students_class.students.add(_student)
                                        _class.students.remove(_student)
                                        promoted_students.append(_student)
                                new_classes_to_update.append(new_students_class)
                            old_classes_to_update.append(_class)
                        except LinkedClasse.DoesNotExist:
                            transaction.set_rollback(True)
                            return Response({'message': f"No class has been linked to the {_class.name} class"}, status=400)
                        except Exception as e:
                            transaction.set_rollback(True)
                            print(e)
                            return Response(status=400)
                    
                    Student.objects.bulk_update(graduated_students, ['current_year', 'has_completed', 'graduation_year', 'graduation_date'])
                    Student.objects.bulk_update(promoted_students, ['current_year', 'academic_years', 'st_class', 'linked_classes'])
                    Student.objects.bulk_update(repeated_students_to_update, ['repeated', 'repeated_academic_years'])
                    Classe.objects.bulk_update(new_classes_to_update, ['students_year', 'academic_years'])
                    Classe.objects.bulk_update(old_classes_to_update, ['students_year', 'academic_years'])
                    GraduatedClasse.objects.bulk_create(graduation_class)
                except Exception as e:
                    transaction.set_rollback(True)
                    print(e)
                    return Response(status=400)
                    
            new_academic_year_data = AcademicYearSerializer(new_academic_year).data
            return Response({
                'message': 'Operation successful',
                'new_year': new_academic_year_data,
            })

    elif data['type'] == 'delete':
        all_academic_years = AcademicYear.objects.filter(school=school).order_by('-end_date')
        current_year = all_academic_years[0]
        previous_year = all_academic_years[1]
        existing_assignments = SubjectAssignment.objects.filter(school=school, academic_year=current_year).exists()
        if existing_assignments:
            return Response({'message': "There are teachers coursework in this academic year"}, status=400)

        with transaction.atomic():
            try:
                classes = Classe.objects.prefetch_related('students').filter(school=school)
                old_classes_to_update = []
                new_classes_to_update = []
                graduated_students_old_classes = []
                graduated_classes_to_delete = []
                undo_graduated_students = []
                undo_promoted_students = []
                undo_repeated_students = []
                years_to_complete = school.level.years_to_complete
                for _class in classes:
                    try:
                        if _class.students_year == years_to_complete:
                            graduated_class = GraduatedClasse.objects.prefetch_related('students', 'subjects').select_related('head_teacher', 'program').get(school=school, graduated_class_name=_class.name, graduation_year=previous_year)
                            students = graduated_class.students.all()
                            for _student in students:
                                _student.current_year -= 1
                                _student.st_class = _class
                                _student.graduation_year = None
                                _student.graduation_date = None
                                _student.has_completed = False
                                undo_graduated_students.append(_student)
                            _class.subjects.set(graduated_class.subjects.all())
                            _class.head_teacher = graduated_class.head_teacher
                            _class.program = graduated_class.program
                            _class.name = graduated_class.graduated_class_name
                            _class.students_year = graduated_class.students_year
                            _class.students.set(students)
                            graduated_students_old_classes.append(_class)
                            graduated_classes_to_delete.append(graduated_class)
                        else:
                            linked_class = LinkedClasse.prefetch_related('to_class__students').objects.get(school=school, from_class=_class)
                            promoted_students_class = linked_class.to_class
                            promoted_students = promoted_students_class.students.all()
                            for _student in promoted_students:
                                if current_year in _student.academic_years.all() and previous_year not in _student.repeated_academic_years.all():
                                    _student.current_year -= 1
                                    _student.linked_classes.remove(linked_class)
                                    _student.academic_years.remove(current_year)
                                    _student.st_class = _class
                                    promoted_students_class.students.remove(_student)
                                    _class.students.add(_student)
                                    undo_promoted_students.append(_student)
                                elif current_year in _student.academic_years.all() and previous_year in _student.repeated_academic_years.all():
                                    _student.repeated_academic_years.remove(previous_year)
                                    _student.academic_years.remove(current_year)
                                    undo_repeated_students.append(_student)
                            old_classes_to_update.append(promoted_students_class)
                        new_classes_to_update.append(_class)
                    except LinkedClasse.DoesNotExist:
                        transaction.set_rollback(True)
                        return Response({'message': f"No class has been linked to the {_class} class"}, status=400)
                    except Exception:
                        transaction.set_rollback(True)
                        return Response(status=400)
                    
                Student.objects.bulk_update(undo_graduated_students, ['current_year', 'has_completed', 'graduation_year', 'graduation_date', 'st_class'])
                Student.objects.bulk_update(undo_promoted_students, ['current_year', 'academic_years', 'st_class', 'linked_classes'])
                Student.objects.bulk_update(undo_repeated_students, ['repeated_academic_years', 'academic_years'])
                Classe.objects.bulk_update(graduated_students_old_classes, ['students', 'name', 'students_year', 'head_teacher', 'program', 'subjects'])
                Classe.objects.bulk_update(old_classes_to_update, ['students'])
                Classe.objects.bulk_update(new_classes_to_update, ['students'])
                for _class in graduated_classes_to_delete:
                    _class.delete()
                
            except Exception:
                transaction.set_rollback(True)
                return Response(status=400)
            
    return Response()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_staff(request):
    data = request.data
    sch_admin = request.user.staff
    school = sch_admin.school
    
    if data['type'] == 'create':
        department = None
        staff_id = None
        first_name = data['firstName']
        last_name = data['lastName']
        role = data['role']
        gender = data['gender']
        subjects = json.loads(data['subjects'])
        dob = data['dateOfBirth']
        if school.has_departments:
            department = Department.objects.get(school=school, name=data['department'])

        user_no = random.randint(100, 999)
        username = f"{data['firstName'].replace(' ', '')[0].upper()}{data['lastName'].replace(' ', '').lower()}{user_no}"
        if school.staff_id:
            staff_id = data['staffId']
        else:
            staff_id = username
        
        if Staff.objects.filter(school=school, staff_id=staff_id).exists():
            return Response({'message': f"Staff with ID [ {staff_id} ] already exists"}, status=400)
        
        with transaction.atomic():
            try:
                user = User.objects.create_user(
                    username=username,
                    password=username,
                    first_name=first_name,
                    last_name=last_name,
                )
                user.save()
                staff_user = User.objects.get(username=username)
                staff_obj = Staff.objects.create(
                    user=staff_user,
                    staff_id=staff_id,
                    department=department,
                    role=role,
                    gender=gender,
                    dob=dob,
                    school=school,
                    is_active=True,
                )
                subjects_objs = Subject.objects.filter(schools=school, name__in=subjects).distinct()
                staff_obj.subjects.set(subjects_objs)

            except IntegrityError:
                return Response({'message': 'A user with these details already exists'}, status=400)
            except Exception as e:
                transaction.set_rollback(True)
                return Response(status=400)

            

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

    elif data['type'] == 'input-student':
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
    
    

