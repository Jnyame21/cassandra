# Django
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.core.validators import EmailValidator
from django.utils import timezone
from django.http import FileResponse
from django.forms import DateField
from django.db.models import Q

# Document Manipulation
import pandas as pd

from api.models import *
from api.serializer import *
import random
from datetime import datetime
import json
from api.utils import get_staff_creation_file, get_students_creation_file, ErrorMessageException, valid_phone_number, valid_email, staff_title_options, religion_options

# Django Restframework
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from pycountryinfo.countryinfo import PyCountryInfo
import imghdr


# Admin
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_school_admin_data(request):
    sch_admin = Staff.objects.select_related('school', 'current_role__level').get(user=request.user)
    school = sch_admin.school
    current_level = sch_admin.current_role.level
    current_academic_year = AcademicYear.objects.get(id=int(request.GET.get('year')))
    current_term = int(request.GET.get('term'))
    academic_years = AcademicYearSerializer(AcademicYear.objects.select_related('level').filter(school=school, level=current_level).order_by('-start_date'), many=True).data
    student_classes = Classe.objects.select_related('head_teacher__user', 'program').prefetch_related('subjects', 'students__user').filter(school=school, level=current_level).order_by('students_year')
    student_classes_data = ClassesSerializerOne(student_classes, many=True).data
    staff_roles = [x.identifier for x in StaffRole.objects.filter(schools=school, level=current_level) if x.name.lower() != 'administrator']
    subject_assignments_data = []
    if not current_level.has_departments:
        subject_assignments = SubjectAssignment.objects.prefetch_related('subjects').select_related('teacher__user', 'students_class').filter(school=school, level=current_level, academic_year=current_academic_year, academic_term=current_term)
        subject_assignments_data = SubjectAssignmentSerializerOne(subject_assignments, many=True).data
    departments_data = []
    programs = []
    if current_level.has_departments:
        department_objs = Department.objects.select_related('hod__user').prefetch_related('subjects', 'teachers__user').filter(school=school, level=current_level)
        departments_data = DepartmentNameHODSubjectsSerializer(department_objs, many=True).data
        
    if current_level.has_programs:
        programs = [x.identifier for x in Program.objects.filter(schools=school, level=current_level)]

    staff_objs = Staff.objects.select_related('user').prefetch_related('roles', 'departments', 'subjects').filter(school=school).order_by('-date_created')
    staff_data = StaffSerializerOne(staff_objs, many=True).data
    subjects = [x.identifier for x in Subject.objects.filter(schools=school, level=current_level)]

    released_results_objs = ReleasedResult.objects.select_related('academic_year', 'released_by__user').filter(school=school, level=current_level).order_by('-date')
    released_results_data = ReleasedResultsSerializer(released_results_objs, many=True).data
    
    return Response({
        'classes': student_classes_data,
        'departments': departments_data,
        'subjects': subjects,
        'staff': staff_data,
        'staff_roles': staff_roles,
        'programs': programs,
        'academic_years': academic_years,
        'subject_assignments': subject_assignments_data,
        'released_results': released_results_data,
    }, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def school_admin_academic_years(request):
    sch_admin = Staff.objects.select_related('school', 'current_role__level').get(user=request.user)
    school = sch_admin.school
    current_level = sch_admin.current_role.level
    data = request.data

    def parse_date(date: str):
        return datetime.strptime(date, "%Y-%m-%d").date()

    if data['type'] == 'create':
        new_year_name = data['newYear']
        current_year = AcademicYear.objects.get(school=school, level=current_level, name=data['year'])
        start_date = timezone.now().date()
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
            new_academic_year = AcademicYear.objects.create(
                name=new_year_name,
                school=school,
                level=current_level,
                start_date=start_date,
                end_date=end_date,
                term_1_end_date=term_1_end_date,
                term_2_start_date=term_2_start_date,
                term_2_end_date=term_2_end_date,
                term_3_start_date=term_3_start_date,
                term_3_end_date=term_3_end_date,
                students_graduation_date=students_graduation_date,
            )
            new_academic_year.save()
            return new_academic_year

        invalid_validation = validate_dates()
        if invalid_validation:
            return Response({'message': invalid_validation}, status=400)
        
        try:
            AcademicYear.objects.get(school=school, level=current_level, name=new_year_name)
            return Response({'message': f"Academic year with name {new_year_name} for the level '{current_level.name}' already exists"}, status=400)
        except AcademicYear.DoesNotExist:
            with transaction.atomic():
                try:
                    repeated_students = Student.objects.filter(school=school, level=current_level, st_id__in=repeated_students_ids).distinct()
                    new_academic_year = create_new_academic_year()
                    classes = Classe.objects.prefetch_related('students__st_class', 'students__academic_years', 'students__repeated_academic_years').filter(school=school, level=current_level)
                    graduated_classes = []
                    promoted_and_graduated_students = []
                    years_to_complete = int(current_level.years_to_complete)
                    for _class in classes:
                        students = _class.students.all()
                        if _class.students_year == years_to_complete:
                            graduated_class = GraduatedClasse(
                                school=school,
                                level=current_level,
                                name=f"{_class.name} CLASS OF {current_year.name}",
                                class_graduated_from=_class,
                                graduated_academic_year=current_year,
                            )
                            graduated_class_data = {'name': graduated_class.name, 'students': [], 'class_instance': graduated_class}
                            for _student in students:
                                if _student in repeated_students:
                                    _student.repeated_academic_years.add(current_year)
                                    _student.academic_years.add(new_academic_year)
                                else:
                                    _student.current_year = years_to_complete + 1
                                    _student.st_class = None
                                    _class.students.remove(_student)
                                    promoted_and_graduated_students.append(_student)
                                    graduated_class_data['students'].append(_student)
                            graduated_classes.append(graduated_class_data)
                        else:
                            new_students_class = _class.linked_class
                            if not new_students_class:
                                return Response({'message': f"No class has been linked to the {_class.name} class"}, status=400)
                            
                            for _student in students:
                                if _student in repeated_students:
                                    _student.repeated_academic_years.add(current_year)
                                    _student.academic_years.add(new_academic_year)
                                else:
                                    _student.current_year += 1
                                    _student.academic_years.add(new_academic_year)
                                    _student.st_class = new_students_class
                                    new_students_class.students.add(_student)
                                    _class.students.remove(_student)
                                    promoted_and_graduated_students.append(_student)

                    Student.objects.bulk_update(promoted_and_graduated_students, ['current_year', 'st_class'])
                    created_graduated_classes = GraduatedClasse.objects.prefetch_related('students').bulk_create([x['class_instance'] for x in graduated_classes])
                    for created_class, original_class in zip(created_graduated_classes, graduated_classes):
                        created_class.students.add(*original_class['students'])
                except Exception as e:
                    transaction.set_rollback(True)
                    return Response(status=400)

            new_academic_year_data = AcademicYearSerializer(new_academic_year).data
            return Response({
                'message': 'Operation successful',
                'new_year': new_academic_year_data,
            })

    elif data['type'] == 'delete':
        all_academic_years = AcademicYear.objects.filter(school=school, level=current_level).order_by('-end_date')
        current_year = all_academic_years[0]
        previous_year = all_academic_years[1]
        existing_assignments = SubjectAssignment.objects.filter(school=school, level=current_level, academic_year=current_year).exists()
        if existing_assignments:
            return Response({'message': "There are teachers subject assignments in this academic year"}, status=400)
        existing_attendance = StudentAttendance.objects.filter(school=school, level=current_level, academic_year=current_year).exists()
        if existing_attendance:
            return Response({'message': "There are students attendance data in this academic year"}, status=400)
        
        with transaction.atomic():
            try:
                classes = Classe.objects.select_related('linked_class__students__st_class', 'linked_class__students__academic_years').prefetch_related('students__repeated_academic_years').filter(school=school, level=current_level).order_by('students_year')
                promoted_graduated_students = []
                years_to_complete = current_level.years_to_complete
                graduated_class_objs = GraduatedClasse.objects.select_related('class_graduated_from').prefetch_related('students__st_class', 'students__academic_years').filter(graduated_academic_year=previous_year)
                graduated_classes_mapping = {x.class_graduated_from.id: x for x in graduated_class_objs}
                for _class in classes:
                    class_students = _class.students.all()
                    for _student in class_students:
                        _student.academic_years.remove(current_year)
                        _student.repeated_academic_years.remove(previous_year)
                    if _class.students_year == years_to_complete:
                        graduated_class = graduated_classes_mapping[_class.id]
                        graduated_class_students = graduated_class.students.all()
                        for _student in graduated_class_students:
                            _student.current_year -= 1
                            _student.st_class = _class
                            _student.academic_years.remove(current_year)
                            promoted_graduated_students.append(_student)
                        _class.students.add(*graduated_class_students)
                    else:
                        linked_class = _class.linked_class
                        if not linked_class:
                            return Response({'message': f"No class has been linked to the {_class.name} class"}, status=400)
                        promoted_students = linked_class.students.all()
                        for _student in promoted_students:
                            _student.current_year -= 1
                            _student.st_class = _class
                            _student.academic_years.remove(current_year)
                            promoted_graduated_students.append(_student)
                        _class.students.add(*promoted_students)
                    
                Student.objects.bulk_update(promoted_graduated_students, ['current_year', 'st_class'])
                graduated_class_objs.delete()
            except Exception as e:
                print(e)
                transaction.set_rollback(True)
                return Response(status=400)

        return Response(status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def school_admin_staff(request):
    data = request.data
    sch_admin = Staff.objects.select_related('school', 'current_role__level').get(user=request.user)
    current_level = sch_admin.current_role.level
    school = sch_admin.school

    if data['type'] == 'createWithoutFile':
        date_field = DateField()
        email_validator = EmailValidator()
        staff_id = None
        first_name = data['firstName'].strip()
        last_name = data['lastName'].strip()
        title = data['title'].title()
        gender = data['gender'].lower()
        img = data['img'] if data['img'] else ''
        if img and not imghdr.what(img):
            return Response({'message': f"Invalid image! Check the staff image"}, status=400)
        contact = data['contact'].strip()
        address = data['address'].strip()
        date_enrolled = data['dateEnrolled']
        region = data['region'].strip()
        religion = data['religion']
        alt_contact = data['altContact'].strip()
        pob = data['pob'].strip()
        email = data['email'].strip() if data['email'] else ''
        nationality = data['nationality'].strip()
        subjects = json.loads(data['subjects'])
        dob = data['dateOfBirth']
        try:
            date_field.clean(dob)
        except Exception:
            return Response({'message': f"{dob} is not a valid date. Check the date of birth of the staff"}, status=400)

        if date_enrolled:
            try:
                date_field.clean(date_enrolled)
            except Exception:
                return Response({'message': f"{date_enrolled} is not a valid date. Check the staff employment date"}, status=400)

        if email:
            try:
                email_validator(email)
            except Exception:
                return Response({'message': f"{email} is not a valid email. Check the staff email address"}, status=400)

        if not valid_phone_number(contact):
            return Response({'message': f"{contact} is not a valid phone number. Check the staff phone number"}, status=400)

        countryinfo = PyCountryInfo()
        if not countryinfo.is_valid_nationality(nationality.title()):
            return Response(
                {'message': f"{nationality} is not a valid nationality. Check the nationality of the staff"},
                status=400)

        if nationality.lower() == 'ghanaian' and not countryinfo.is_valid_country_province('Ghana', region.title()):
            return Response({'message': f"{region} is not a valid region in 'Ghana'!. Check the region of the staff"}, status=400)

        user_no = random.randint(100, 999)
        username = f"{first_name.replace(' ', '')[0].upper()}{last_name.replace(' ', '').lower()}{user_no}"
        if school.staff_id:
            staff_id = data['staff_id']
        else:
            staff_id = username
            
        with transaction.atomic():
            try:
                user = User.objects.create_user(
                    username=username,
                    password=username,
                    first_name=first_name.title(),
                    last_name=last_name.title(),
                )
                staff_obj = Staff.objects.create(
                    user=user,
                    staff_id=staff_id,
                    title=title,
                    gender=gender,
                    dob=dob,
                    school=school,
                    alt_contact=alt_contact,
                    contact=contact,
                    address=address.lower(),
                    email=email.lower(),
                    region=region.lower(),
                    religion=religion.lower(),
                    pob=pob.lower(),
                    date_enrolled=date_enrolled if date_enrolled else None,
                    nationality=nationality.lower(),
                    img=img,
                    is_active=True,
                )
                subjects_objs = Subject.objects.filter(identifier__in=subjects).distinct()
                staff_obj.subjects.set(subjects_objs)

            except Exception as e:
                transaction.set_rollback(True)
                return Response(status=400)

        staff_data = StaffSerializerOne(Staff.objects.select_related('user').prefetch_related('subjects', 'departments', 'roles').get(school=school, staff_id=staff_id)).data
        return Response(staff_data, status=200)

    elif data['type'] == 'getFile':
        byte_file = get_staff_creation_file(school)
        filename = 'staff-creation-file.xlsx'
        response = FileResponse(byte_file, as_attachment=True, filename=filename)
        response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response['Access-Control-Expose-Headers'] = 'Content-Disposition'
        return response

    elif data['type'] == 'createWithFile':
        df = None
        skipped_rows = 3
        date_field = DateField()
        email_validator = EmailValidator()
        countryinfo = PyCountryInfo()
        staff_to_create_ids = set()
        existing_staff_ids = []
        users_to_create = []
        staff_to_create = []
        staff_instances = []
        created_staff = []
        try:
            df = pd.read_excel(data['file'], header=1, sheet_name=0, skiprows=skipped_rows)
            # Drop the example row "Eg. Cassandra, Eg. Akua Afriyie, ..."
            df = df.drop(index=0)
            df = df.dropna(how='all')
        except Exception as e:
            return Response({'message': 'Invalid file! Make sure you upload the excel file you generated'}, status=400)

        if school.staff_id:
            existing_staff_ids = [x.staff_id for x in Staff.objects.filter(school=school)]

        def show_error_message(label_name: str, column_name: str, row_idx: int):
            return f"The {label_name} cannot be empty! Check the value in the '{column_name}' column in row {row_idx}"

        def get_data(row, index:int):
            row_index = index + 2 + skipped_rows
            first_name = str(row['FIRST NAME'].strip()) if pd.notna(row.get('FIRST NAME')) else None
            last_name = str(row['LAST NAME (MIDDLE NAME + SURNAME)']).strip() if pd.notna(row.get('LAST NAME (MIDDLE NAME + SURNAME)')) else None
            title = str(row['TITLE']).strip().replace('.', '').title() if pd.notna(row.get('TITLE')) else None
            staff_id = str(row['STAFF ID']).strip() if school.staff_id and pd.notna(row.get('STAFF ID')) else None
            gender = str(row['GENDER']).strip().lower() if pd.notna(row.get('GENDER')) else None
            dob = str(row['DATE OF BIRTH']).strip() if pd.notna(row.get('DATE OF BIRTH')) else None
            date_enrolled = str(row['DATE EMPLOYED(OPTIONAL)']).strip() if pd.notna(row.get('DATE EMPLOYED(OPTIONAL)')) else None
            religion = str(row['RELIGION']).strip() if pd.notna(row.get('RELIGION')) else None
            nationality = str(row['NATIONALITY']).strip() if pd.notna(row.get('NATIONALITY')) else None
            region = str(row['REGION/STATE']).strip() if pd.notna(row.get('REGION/STATE')) else None
            pob = str(row['HOME CITY/TOWN']).strip() if pd.notna(row.get('HOME CITY/TOWN')) else None
            contact = str(row['PHONE NUMBER']).strip() if pd.notna(row.get('PHONE NUMBER')) else None
            alt_contact = str(row['SECOND PHONE NUMBER(OPTIONAL)']).strip() if pd.notna(row.get('SECOND PHONE NUMBER(OPTIONAL)')) else ''
            address = str(row['RESIDENTIAL ADDRESS']).strip() if pd.notna(row.get('RESIDENTIAL ADDRESS')) else None
            email = str(row['EMAIL(OPTIONAL)']).strip() if pd.notna(row.get('EMAIL(OPTIONAL)')) else ''
            if not first_name:
                error_message = show_error_message('first name', 'FIRST NAME', row_index)
                raise ErrorMessageException(error_message)
            elif not last_name:
                error_message = show_error_message('last name', 'LAST NAME', row_index)
                raise ErrorMessageException(error_message)
            elif not gender:
                error_message = show_error_message('gender', 'GENDER', row_index)
                raise ErrorMessageException(error_message)
            elif gender not in ['male', 'female']:
                error_message = f"'{gender}' is not a valid gender! Check the value in the 'GENDER' column in row {row_index}. Valid values are {['Male', 'Female']}"
                raise ErrorMessageException(error_message)
            elif not dob:
                error_message = show_error_message('date of birth', 'DATE OF BIRTH', row_index)
                raise ErrorMessageException(error_message)
            elif not title:
                error_message = show_error_message('title', 'TITLE', row_index)
                raise ErrorMessageException(error_message)
            elif title not in staff_title_options:
                error_message = f"'{title}' is not a valid title! Check the value in the 'TITLE' column in row {row_index}. Valid values are {staff_title_options}"
                raise ErrorMessageException(error_message)
            elif school.staff_id and not staff_id:
                error_message = show_error_message('staff id', 'STAFF ID', row_index)
                raise ErrorMessageException(error_message)
            elif not religion:
                error_message = show_error_message('religion', 'RELIGION', row_index)
                raise ErrorMessageException(error_message)
            elif religion.title() not in religion_options:
                error_message = f"'{religion}' is not a valid religion! Check the value in the 'RELIGION' column in row {row_index}. Valid values are {religion_options}"
                raise ErrorMessageException(error_message)
            elif not nationality:
                error_message = show_error_message('nationality', 'NATIONALITY', row_index)
                raise ErrorMessageException(error_message)
            elif not countryinfo.is_valid_nationality(nationality.title()):
                error_message = f"'{nationality}' is not a valid nationality! Check the value in the 'NATIONALITY' column in row {row_index}."
                raise ErrorMessageException(error_message)
            elif not region:
                error_message = show_error_message('region', 'REGION/STATE', row_index)
                raise ErrorMessageException(error_message)
            elif nationality.lower() == 'ghanaian' and not countryinfo.is_valid_country_province('Ghana', region):
                error_message = f"'{region}' is not a valid region in 'Ghana'! Check the value in the 'REGION/STATE' column in row {row_index}."
                raise ErrorMessageException(error_message)
            elif not pob:
                error_message = show_error_message('home city/town', 'HOME CITY/TOWN', row_index)
                raise ErrorMessageException(error_message)
            elif not contact:
                error_message = show_error_message('phone number', 'PHONE NUMBER', row_index)
                raise ErrorMessageException(error_message)
            elif not valid_phone_number(contact):
                error_message = f"'{contact}' is not a valid phone number! Check the value in the 'PHONE NUMBER' column in row {row_index}."
                raise ErrorMessageException(error_message)
            elif alt_contact and not valid_phone_number(alt_contact):
                error_message = f"'{alt_contact}' is not a valid phone number! Check the value in the 'SECOND PHONE NUMBER' column in row {row_index}."
                raise ErrorMessageException(error_message)
            elif not address:
                error_message = show_error_message('residential addresss', 'RESIDENTIAL ADDRESS', row_index)
                raise ErrorMessageException(error_message)

            try:
                dob = datetime.strptime(dob, "%d-%m-%Y").strftime("%Y-%m-%d")
                date_field.clean(dob)
            except Exception:
                error_message = f"'{dob}' is not a valid date! Check the value in the 'DATE OF BIRTH' column in row {row_index}."
                raise ErrorMessageException(error_message)

            if date_enrolled:
                try:
                    date_enrolled = datetime.strptime(date_enrolled, "%d-%m-%Y").strftime("%Y-%m-%d")
                    date_field.clean(date_enrolled)
                except Exception:
                    error_message = f"'{date_enrolled}' is not a valid date! Check the value in the 'DATE EMPLOYED(OPTIONAL)' column in row {row_index}."
                    raise ErrorMessageException(error_message)

            if email:
                try:
                    email_validator(email)
                except Exception:
                    error_message = f"'{email}' is not a valid email address! Check the value in the 'EMAIL(OPTIONAL)' column in row {row_index}."
                    raise ErrorMessageException(error_message)
                
            user_no = random.randint(100, 999)
            username = f"{first_name.replace(' ', '')[0].upper()}{last_name.replace(' ', '').lower()}{user_no}"

            if school.staff_id:
                if staff_id in staff_to_create_ids:
                    error_message = f"Two staff cannot have the same staff ID. The staff ID in row {row_index} conflicts with another staff ID on the sheet"
                    raise ErrorMessageException(error_message)
                elif staff_id in existing_staff_ids:
                    error_message = f"Staff with ID '{staff_id}' already exists. Check the staff ID in row {row_index}"
                    raise ErrorMessageException(error_message)
            else:
                staff_id = username

            return {
                'first_name': first_name,
                'last_name': last_name,
                'username': username,
                'staff_id': staff_id,
                'title': title,
                'gender': gender,
                'dob': dob,
                'date_enrolled': date_enrolled,
                'religion': religion,
                'region': region,
                'nationality': nationality,
                'pob': pob,
                'contact': contact,
                'alt_contact': alt_contact,
                'email': email,
                'address': address,
            }

        with transaction.atomic():
            try:
                for index, row in df.iterrows():
                    staff_data = get_data(row, index)
                    user = User(
                        username=staff_data['username'],
                        first_name=staff_data['first_name'].title(),
                        last_name=staff_data['last_name'].title(),
                    )
                    user.set_password(staff_data['username'])
                    users_to_create.append(user)
                    staff_to_create.append((staff_data['username'], staff_data))
                    staff_to_create_ids.add(staff_data['staff_id'])

                User.objects.bulk_create(users_to_create)
                created_users = User.objects.filter(username__in=[user.username for user in users_to_create])
                user_mapping = {user.username: user for user in created_users}
                for username, staff_data in staff_to_create:
                    user = user_mapping[username]
                    staff = Staff(
                        user=user,
                        school=school,
                        staff_id=staff_data['staff_id'],
                        title=staff_data['title'],
                        gender=staff_data['gender'],
                        dob=staff_data['dob'],
                        date_enrolled=staff_data['date_enrolled'],
                        religion=staff_data['religion'].lower(),
                        region=staff_data['region'].lower(),
                        nationality=staff_data['nationality'].lower(),
                        pob=staff_data['pob'].lower(),
                        contact=staff_data['contact'],
                        alt_contact=staff_data['alt_contact'],
                        email=staff_data['email'].lower(),
                        address=staff_data['address'].lower(),
                        is_active=True,
                    )
                    staff_instances.append(staff)

                Staff.objects.bulk_create(staff_instances)
            except ErrorMessageException as e:
                return Response({'message': str(e)}, status=400)
            except Exception as e:
                transaction.set_rollback(True)
                return Response(status=400)

        created_staff = Staff.objects.select_related('user').prefetch_related('subjects', 'roles', 'departments').filter(school=school, staff_id__in=staff_to_create_ids)
        staff_data = StaffSerializerOne(created_staff, many=True).data
        return Response(staff_data, status=200)

    elif data['type'] == 'edit':
        with transaction.atomic():
            try:
                edit_type = data['editType']
                staff_id = data['staffId']
                new_value = data['newValue'].strip() if isinstance(data['newValue'], str) else data['newValue']
                if edit_type in ['first_name', 'last_name']:
                    staff = Staff.objects.select_related('user').get(school=school, staff_id=staff_id)
                    user = staff.user
                    user_no = random.randint(100, 999)
                    new_username = None
                    old_username = user.username
                    old_password = user.password
                    if edit_type == 'first_name':
                        user.first_name = new_value.title()
                        new_username = f"{new_value.replace(' ', '')[0].upper()}{user.last_name.replace(' ', '').lower()}{user_no}"
                    elif edit_type == 'last_name':
                        user.last_name = new_value.title()
                        new_username = f"{user.first_name.replace(' ', '')[0].upper()}{new_value.replace(' ', '').lower()}{user_no}"

                    if new_username:
                        user.username = new_username
                        if old_username == old_password:
                            user.set_password(new_username)
                        user.save()
                        if not school.staff_id:
                            staff.staff_id = new_username
                            staff.save()
                        return Response(
                            StaffSerializerOne(Staff.objects.get(school=school, staff_id=staff_id)).data['user'], 
                            status=200
                        )
                elif edit_type == 'title':
                    staff = Staff.objects.get(school=school, staff_id=staff_id)
                    staff.title = new_value.title()
                    staff.save()
                    return Response(StaffSerializerOne(Staff.objects.get(school=school, staff_id=staff_id)).data['user'], status=200)
                elif edit_type == 'gender':
                    staff = Staff.objects.get(school=school, staff_id=staff_id)
                    gender = new_value.lower()
                    staff.gender = gender
                    staff.save()
                    return Response(gender, status=200)
                elif edit_type == 'dob':
                    staff = Staff.objects.get(school=school, staff_id=staff_id)
                    staff.dob = new_value
                    staff.save()
                    return Response(new_value, status=200)
                elif edit_type == 'pob':
                    staff = Staff.objects.get(school=school, staff_id=staff_id)
                    staff.pob = new_value.lower()
                    staff.save()
                    return Response(new_value, status=200)
                elif edit_type == 'date_enrolled':
                    staff = Staff.objects.get(school=school, staff_id=staff_id)
                    staff.date_enrolled = new_value
                    staff.save()
                    return Response(new_value, status=200)
                elif edit_type == 'staff_id' and school.staff_id:
                    staff = Staff.objects.get(school=school, staff_id=staff_id)
                    staff.staff_id = new_value
                    staff.save()
                    return Response(new_value, status=200)
                elif edit_type == 'addSubjects':
                    staff = Staff.objects.prefetch_related('subjects').get(school=school, staff_id=staff_id)
                    subject_identifiers = json.loads(new_value)
                    subject_objs = Subject.objects.filter(schools=school, level=current_level, identifier__in=subject_identifiers)
                    staff.subjects.add(*subject_objs)
                    return Response([x.identifier for x in subject_objs], status=200)
                elif edit_type == 'removeSubjects':
                    current_academic_year = AcademicYear.objects.get(school=school, level=current_level, name=data['year'])
                    current_term = int(data['term'])
                    staff = Staff.objects.prefetch_related('subjects').get(school=school, staff_id=staff_id)
                    subject_identifiers = json.loads(new_value)
                    subject_objs = Subject.objects.select_related('level').filter(schools=school, identifier__in=subject_identifiers)
                    for _subj in subject_objs:
                        if SubjectAssignment.objects.filter(school=school, subjects=_subj, teacher=staff, academic_year=current_academic_year, academic_term=current_term).exists():
                            return Response({'message': f"This teacher has already been assigned to teach {_subj.name}({_subj.level.name})"}, status=400)
                    staff.subjects.remove(*subject_objs)
                    return Response(status=200)
                elif edit_type == 'region':
                    staff = Staff.objects.get(school=school, staff_id=staff_id)
                    staff_nationality = staff.nationality
                    countryinfo = PyCountryInfo()
                    staff_country = countryinfo.get_country_from_nationality(staff_nationality)
                    if staff_country.lower() == 'ghana' and not countryinfo.is_valid_country_province('Ghana', new_value.title()):
                        return Response({'message': f"'{new_value}' is not a valid region in 'Ghana'!"}, status=400)
                    staff.region = new_value.lower()
                    staff.save()
                    return Response(new_value, status=200)
                elif edit_type == 'nationality':
                    staff = Staff.objects.get(school=school, staff_id=staff_id)
                    staff.nationality = new_value.lower()
                    staff.save()
                    return Response(new_value, status=200)
                elif edit_type == 'religion':
                    staff = Staff.objects.get(school=school, staff_id=staff_id)
                    staff.religion = new_value.lower()
                    staff.save()
                    return Response(new_value, status=200)
                elif edit_type == 'address':
                    staff = Staff.objects.get(school=school, staff_id=staff_id)
                    staff.address = new_value.lower()
                    staff.save()
                    return Response(new_value, status=200)
                elif edit_type == 'contact':
                    if not valid_phone_number(new_value):
                        return Response({'message': f"'{new_value}' is not a valid phone number. Make sure you start with a '+' followed by the country code. Eg. +233596021383"}, status=400)
                    staff = Staff.objects.get(school=school, staff_id=staff_id)
                    staff.contact = new_value
                    staff.save()
                    return Response(new_value, status=200)
                elif edit_type == 'alt_contact':
                    if not valid_phone_number(new_value):
                        return Response({'message': f"'{new_value}' is not a valid phone number. Make sure you start with a '+' followed by the country code. Eg. +233596021383"}, status=400)
                    staff = Staff.objects.get(school=school, staff_id=staff_id)
                    staff.alt_contact = new_value
                    staff.save()
                    return Response(new_value, status=200)
                elif edit_type == 'email':
                    if not valid_email(new_value):
                        return Response({'message': f"'{new_value}' is not a valid email address"}, status=400)
                    staff = Staff.objects.get(school=school, staff_id=staff_id)
                    staff.email = new_value.lower()
                    staff.save()
                    return Response(new_value, status=200)
                elif edit_type == 'img':
                    if not imghdr.what(new_value):
                        return Response({'message': f"Invalid image"}, status=400)
                    staff = Staff.objects.get(school=school, staff_id=staff_id)
                    staff.img = new_value
                    staff.save()
                    return Response(StaffSerializerOne(Staff.objects.get(school=school, staff_id=staff_id)).data['img'], status=200)
                
            except:
                transaction.set_rollback(True)
                return Response(status=400)

        return Response(status=400)

    elif data['type'] == 'addRole':
        staff = Staff.objects.prefetch_related('departments', 'roles').get(school=school, staff_id=data['staffId'])
        role = StaffRole.objects.get(schools=school, identifier=data['roleIdentifier'])
        if role in staff.roles.all():
            return Response({'message': "The staff you selected already has this role"}, status=400)
        department = Department.objects.prefetch_related('teachers').get(school=school, identifier=data['departmentIdentifier']) if data['departmentIdentifier'] else None
        
        with transaction.atomic():
            try:
                staff.roles.add(role)
                if department:
                    staff.departments.add(department)
                    department.teachers.add(staff)
            
            except Exception as e:
                transaction.set_rollback(True)
                return Response(status=400)
        
        return Response({
            'role': role.identifier,
            'department': department.identifier if department else '',
        }, status=200) 
    
    elif data['type'] == 'removeRole':
        current_academic_year = AcademicYear.objects.get(school=school, level=current_level, name=data['year'])
        current_term = int(data['term'])
        staff = Staff.objects.prefetch_related('departments').get(school=school, staff_id=data['staffId'])
        role = StaffRole.objects.select_related('level').get(schools=school, identifier=data['roleIdentifier'])
        level = role.level
        if SubjectAssignment.objects.filter(school=school, level=level, teacher=staff, academic_year=current_academic_year, academic_term=current_term).exists():
            return Response({'message': f"This teacher has already been assigned to teach a subject under the level {level.name}"}, status=400)
        department = staff.departments.prefetch_related('teachers').filter(level=level).first()
        with transaction.atomic():
            try:
                staff.roles.remove(role)
                if department:
                    staff.departments.remove(department)
                    department.teachers.remove(staff)
                    
            except Exception as e:
                transaction.set_rollback(True)
                return Response(status=400)
        
        return Response({
            'department': department.identifier if department else '',
        }, status=200)
    
    elif data['type'] == 'setDepartmentHOD':
        departmentHOD = Staff.objects.select_related('user').get(school=school, staff_id=data['departmentHOD'])
        department = Department.objects.select_related('hod').get(school=school, identifier=data['departmentIdentifier'])
        department.hod = departmentHOD
        department.save()
        return Response({
            'user': f"{departmentHOD.title}. {departmentHOD.user.get_full_name()}",
            'staff_id': departmentHOD.staff_id,
        }, status=200)
        
    elif data['type'] == 'removeDepartmentHOD':
        department = Department.objects.select_related('hod').get(school=school, id=int(data['departmentId']))
        department.hod = None
        department.save()
        return Response(status=200)
        
    elif data['type'] == 'delete':
        staff_to_delete = Staff.objects.select_related('user').prefetch_related('levels').get(school=school, staff_id=data['staffId'])
        if staff_to_delete == sch_admin:
            return Response({'message': "You don't have permission to delete this staff"}, status=400)
        
        user = staff_to_delete.user
        if SubjectAssignment.objects.filter(school=school, teacher=staff_to_delete).exists():
            return Response({'message': "You don't have permission to delete this staff"}, status=400)

        students_classes = Classe.objects.select_related('head_teacher').filter(school=school, level__in=staff_to_delete.levels.all())
        for _class in students_classes:
            if _class.head_teacher == staff_to_delete:
                return Response({'message': "You don't have permission to delete this staff"}, status=400)

        with transaction.atomic():
            try:
                user.delete()
            except Exception as e:
                transaction.set_rollback(True)
                return Response(status=400)

        return Response(status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def school_admin_students(request):
    data = request.data
    sch_admin = Staff.objects.select_related('current_role__level', 'school').get(user=request.user)
    current_level = sch_admin.current_role.level
    school = sch_admin.school

    if data['type'] == 'assignClassHeadTeacher':
        staff_id = data['teacherId']
        new_head_teacher = Staff.objects.get(school=school, staff_id=staff_id)
        students_class = Classe.objects.select_related('head_teacher').get(school=school, level=current_level, name=data['studentsClass'])
        with transaction.atomic():
            try:
                students_class.head_teacher = new_head_teacher
                students_class.save()
            except Exception as e:
                transaction.set_rollback(True)
                return Response(status=400)

        new_head_teacher_data = StaffUserIdImgSerializer(new_head_teacher).data
        return Response(new_head_teacher_data, status=200)
    
    if data['type'] == 'removeClassHeadTeacher':
        students_class = Classe.objects.select_related('head_teacher').get(school=school, level=current_level, name=data['studentsClassName'])
        with transaction.atomic():
            try:
                students_class.head_teacher = None
                students_class.save()
            except Exception as e:
                transaction.set_rollback(True)
                return Response(status=400)

        return Response(status=200)

    elif data['type'] == 'createWithoutFile':
        date_field = DateField()
        email_validator = EmailValidator()
        st_id = None
        first_name = data['firstName'].strip()
        last_name = data['lastName'].strip()
        gender = data['gender'].lower()
        img = data['img'] if data['img'] else ''
        if img and not imghdr.what(img):
            return Response({'message': f"Invalid image! Check the student's image"}, status=400)
        contact = data['contact'].strip()
        address = data['address'].strip()
        date_enrolled = data['dateEnrolled']
        region = data['region'].strip()
        religion = data['religion']
        pob = data['pob'].strip()
        email = data['email'].strip() if data['email'] else ''
        nationality = data['nationality']
        dob = data['dob']
        guardian_fullname = data['guardianFullname'].strip().title()
        guardian_gender = data['guardianGender']
        guardian_contact = data['guardianContact'].strip()
        guardian_address = data['guardianAddress'].strip()
        guardian_email = data['guardianEmail'].strip() if data['guardianEmail'] else ''
        guardian_occupation = data['guardianOccupation'].strip()
        guardian_nationality = data['guardianNationality']
        try:
            date_field.clean(dob)
        except Exception:
            return Response({'message': f"{dob} is not a valid date. Check the date of birth of the student"}, status=400)

        if date_enrolled:
            try:
                date_field.clean(date_enrolled)
            except Exception:
                return Response(
                    {'message': f"{date_enrolled} is not a valid date. Check the student's enrollment date"}, status=400)

        if email:
            try:
                email_validator(email)
            except Exception:
                return Response({'message': f"{email} is not a valid email. Check the student's email address"}, status=400)

        if guardian_email:
            try:
                email_validator(guardian_email)
            except Exception:
                return Response(
                    {'message': f"{guardian_email} is not a valid email. Check the student's guardian email address"},
                    status=400)

        if not valid_phone_number(contact):
            return Response({'message': f"{contact} is not a valid phone number. Check the student's phone number"}, status=400)

        if not valid_phone_number(guardian_contact):
            return Response({'message': f"{guardian_contact} is not a valid phone number. Check the student's guardian phone number"}, status=400)

        countryinfo = PyCountryInfo()
        if not countryinfo.is_valid_nationality(nationality.title()):
            return Response(
                {'message': f"{nationality} is not a valid nationality. Check the nationality of the student"},
                status=400)

        if nationality.lower() == 'ghanaian' and not countryinfo.is_valid_country_province('Ghana', region.title()):
            return Response({'message': f"{region} is not a valid region in Ghana! Check the region of the student"}, status=400)

        if not countryinfo.is_valid_nationality(guardian_nationality.title()):
            return Response({'message': f"{guardian_nationality} is not a valid nationality. Check the nationality of the student's guardian"}, status=400)

        user_no = random.randint(100, 999)
        username = f"{first_name.replace(' ', '')[0].upper()}{last_name.replace(' ', '').lower()}{user_no}"
        if current_level.students_id:
            st_id = data['studentId']
        else:
            st_id = username

        if Student.objects.filter(school=school, st_id=st_id).exists():
            return Response({'message': f"Student with ID '{st_id}' already exists"}, status=400)

        student_class = Classe.objects.select_related('program', 'level').get(school=school, name=data['studentClassName'])
        current_academic_year = AcademicYear.objects.get(id=int(data['year']))
        current_academic_term = int(data['term'])
        if StudentResult.objects.filter(student_class=students_class, academic_year=current_academic_year, academic_term=current_academic_term).exists():
            return Response({'message': 'There are students results for this class. Wait for the next academic year or ensure there are no students results'}, status=400)
        
        students_year = student_class.students_year
        class_level = student_class.level
        student_academic_years = AcademicYear.objects.filter(school=school, level=student_class.level).order_by('-start_date')[:int(students_year)]
        with transaction.atomic():
            try:
                user = User.objects.create_user(
                    username=username,
                    password=username,
                    first_name=first_name.title(),
                    last_name=last_name.title(),
                )
                student_obj = Student.objects.create(
                    user=user,
                    school=school,
                    current_level=class_level,
                    st_id=st_id,
                    st_class=student_class,
                    current_program=student_class.program,
                    current_year=students_year,
                    gender=gender,
                    dob=dob,
                    contact=contact,
                    address=address.lower(),
                    email=email.lower(),
                    region=region.lower(),
                    religion=religion.lower(),
                    pob=pob.lower(),
                    date_enrolled=date_enrolled,
                    nationality=nationality.lower(),
                    img=img,
                    guardian=guardian_fullname.lower(),
                    guardian_gender=guardian_gender.lower(),
                    guardian_occupation=guardian_occupation.lower(),
                    guardian_contact=guardian_contact,
                    guardian_address=guardian_address.lower(),
                    guardian_email=guardian_email.lower(),
                    guardian_nationality=guardian_nationality.lower(),
                )
                student_obj.academic_years.set(student_academic_years)
                student_obj.programs.add(student_class.program)
                student_obj.levels.add(class_level)
                student_class.students.add(student_obj)

            except Exception as e:
                transaction.set_rollback(True)
                return Response(status=400)
            
        student_data = StudentSerializerOne(Student.objects.select_related('user').get(school=school, st_id=st_id)).data
        return Response(student_data, status=200)

    elif data['type'] == 'getFile':
        students_class = data['studentsClassName']
        file = get_students_creation_file(current_level, students_class)
        filename = f'{students_class}.xlsx'
        response = FileResponse(file, as_attachment=True, filename=filename)
        response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response['Access-Control-Expose-Headers'] = 'Content-Disposition'
        return response

    elif data['type'] == 'createWithFile':
        df = None
        skipped_rows = 3
        date_field = DateField()
        email_validator = EmailValidator()
        students_to_create_ids = set()
        existing_student_ids = []
        users_to_create = []
        students_to_create = []
        student_instances = []
        created_students = []
        try:
            df = pd.read_excel(data['file'], header=0, sheet_name=0, skiprows=skipped_rows)
            df = df.drop(index=0)
            df = df.dropna(how='all')
        except Exception as e:
            return Response({'message': 'Invalid file! Make sure you upload the excel file you generated'}, status=400)

        if current_level.students_id:
            existing_student_ids = [x.st_id for x in Student.objects.filter(school=school)]

        def show_error_message(label_name: str, column_name: str, row_idx: int):
            return f"The {label_name} cannot be empty! Check the value in the '{column_name}' column in row {row_idx + 2 + skipped_rows}"

        countryinfo = PyCountryInfo()

        def get_data(row):
            first_name = str(row['FIRST NAME']).strip().title() if row['FIRST NAME'] else ''
            last_name = str(row['LAST NAME (MIDDLE NAME + SURNAME)']).strip().title() if row['LAST NAME (MIDDLE NAME + SURNAME)'] else ''
            st_id = str(row['STUDENT ID']).strip() if current_level.students_id and row.get('STUDENT ID') else ''
            gender = str(row['GENDER']).strip().lower() if row['GENDER'] else ''
            dob = str(row['DATE OF BIRTH']).strip() if row['DATE OF BIRTH'] else ''
            date_enrolled = str(row['DATE ENROLLED']).strip() if row['DATE ENROLLED'] else ''
            religion = str(row['RELIGION']).strip().title() if row['RELIGION'] else ''
            nationality = str(row['NATIONALITY']).strip().title() if row['NATIONALITY'] else ''
            region = str(row['REGION/STATE']).strip() if row['REGION/STATE'] else ''
            pob = str(row['PLACE OF BIRTH']).strip() if row['PLACE OF BIRTH'] else ''
            contact = str(row['PHONE NUMBER']).strip()
            address = str(row['RESIDENTIAL ADDRESS']).strip() if row['RESIDENTIAL ADDRESS'] else ''
            email = str(row['EMAIL(OPTIONAL)']).strip() if row['EMAIL(OPTIONAL)'] else ''
            guardian = str(row['GUARDIAN FULL NAME']).strip().lower() if row['GUARDIAN FULL NAME'] else ''
            guardian_gender = str(row['GUARDIAN GENDER']).strip().lower() if row['GUARDIAN GENDER'] else ''
            guardian_occupation = str(row['GUARDIAN OCCUPATION']).strip().lower() if row['GUARDIAN OCCUPATION'] else ''
            guardian_nationality = str(row['GUARDIAN NATIONALITY']).strip().lower() if row['GUARDIAN NATIONALITY'] else ''
            guardian_contact = str(row['GUARDIAN PHONE NUMBER']).strip().lower() if row['GUARDIAN PHONE NUMBER'] else ''
            guardian_address = str(row['GUARDIAN RESIDENTIAL ADDRESS']).strip().lower() if row['GUARDIAN RESIDENTIAL ADDRESS'] else ''
            guardian_email = str(row['GUARDIAN EMAIL(OPTIONAL)']).strip().lower() if row['GUARDIAN EMAIL(OPTIONAL)'] else ''
            if not first_name:
                error_message = show_error_message('first name', 'FIRST NAME', index)
                raise ErrorMessageException(error_message)
            elif not last_name:
                error_message = show_error_message('last name', 'LAST NAME', index)
                raise ErrorMessageException(error_message)
            elif not gender:
                error_message = show_error_message('gender', 'GENDER', index)
                raise ErrorMessageException(error_message)
            elif gender.lower() not in ['male', 'female']:
                error_message = f"'{gender}' is not a valid gender! Check the value in the 'GENDER' column in row {index + 2 + skipped_rows}. Valid values are {['Male', 'Female']}"
                raise ErrorMessageException(error_message)
            elif not dob:
                error_message = show_error_message('date of birth', 'DATE OF BIRTH', index)
                raise ErrorMessageException(error_message)
            elif current_level.students_id and not st_id:
                error_message = show_error_message('student id', 'STUDENT ID', index)
                raise ErrorMessageException(error_message)
            elif not religion:
                error_message = show_error_message('religion', 'RELIGION', index)
                raise ErrorMessageException(error_message)
            elif religion not in religion_options:
                error_message = f"'{religion}' is not a valid religion! Check the value in the 'RELIGION' column in row {index + 2 + skipped_rows}. Valid values are {religion_options}"
                raise ErrorMessageException(error_message)
            elif not nationality:
                error_message = show_error_message('nationality', 'NATIONALITY', index)
                raise ErrorMessageException(error_message)
            elif not countryinfo.is_valid_nationality(nationality.title()):
                error_message = f"'{nationality}' is not a valid nationality! Check the value in the 'NATIONALITY' column in row {index + 2 + skipped_rows}."
                raise ErrorMessageException(error_message)
            elif not region:
                error_message = show_error_message('region', 'REGION/STATE', index)
                raise ErrorMessageException(error_message)

            elif nationality.lower() == 'ghanaian' and not countryinfo.is_valid_country_province('Ghana', region.title()):
                error_message = f"'{region}' is not a valid region in Ghana! Check the value in the 'REGION/STATE' column in row {index + 2 + skipped_rows}."
                raise ErrorMessageException(error_message)
            elif not pob:
                error_message = show_error_message('place of birth', 'PLACE OF BIRTH', index)
                raise ErrorMessageException(error_message)
            elif not contact:
                error_message = show_error_message('phone number', 'PHONE NUMBER', index)
                raise ErrorMessageException(error_message)
            elif not valid_phone_number(contact):
                error_message = f"'{contact}' is not a valid phone number! Check the value in the 'PHONE NUMBER' column in row {index + 2 + skipped_rows}."
                raise ErrorMessageException(error_message)
            elif not address:
                error_message = show_error_message('residential addresss', 'RESIDENTIAL ADDRESS', index)
                raise ErrorMessageException(error_message)
            elif not guardian:
                error_message = show_error_message('guardian fullname', 'GUARDIAN FULL NAME', index)
                raise ErrorMessageException(error_message)
            elif not guardian_occupation:
                error_message = show_error_message('guardian occupation', 'GUARDIAN OCCUPATION', index)
                raise ErrorMessageException(error_message)
            elif not countryinfo.is_valid_nationality(guardian_nationality.title()):
                error_message = show_error_message('guardian nationality', 'GUARDIAN NATIONALITY', index)
                raise ErrorMessageException(error_message)
            elif not guardian_gender:
                error_message = show_error_message('guardian gender', 'GUARDIAN GENDER', index)
                raise ErrorMessageException(error_message)
            elif not valid_phone_number(guardian_contact):
                error_message = f"'{contact}' is not a valid phone number! Check the value in the 'GUARDIAN PHONE NUMBER' column in row {index + 2 + skipped_rows}."
                raise ErrorMessageException(error_message)
            elif not guardian_address:
                error_message = show_error_message('guardian residential address', 'GUARDIAN RESIDENTIAL ADDRESS', index)
                raise ErrorMessageException(error_message)

            try:
                dob = datetime.strptime(dob, "%d-%m-%Y").strftime("%Y-%m-%d")
                date_field.clean(dob)
            except Exception:
                error_message = f"'{dob}' is not a valid date! Check the value in the 'DATE OF BIRTH' column in row {index + 2 + skipped_rows}."
                raise ErrorMessageException(error_message)

            if current_level.students_id:
                if st_id in students_to_create_ids:
                    error_message = f"Two students cannot have the same student ID. The student ID in row {index + 2 + skipped_rows} conflicts with another student ID on the sheet"
                    raise ErrorMessageException(error_message)
                elif st_id in existing_student_ids:
                    error_message = f"Student with ID '{st_id}' already exists. Check the student ID in row {index + 2 + skipped_rows}"
                    raise ErrorMessageException(error_message)
            else:
                st_id = username

            try:
                date_enrolled = datetime.strptime(date_enrolled, "%d-%m-%Y").strftime("%Y-%m-%d")
                date_field.clean(date_enrolled)
            except Exception:
                error_message = f"'{date_enrolled}' is not a valid date! Check the value in the 'DATE ENROLLED' column in row {index + 2 + skipped_rows}."
                raise ErrorMessageException(error_message)

            if email:
                try:
                    email_validator(email)
                except Exception:
                    error_message = f"'{email}' is not a valid email address! Check the value in the 'EMAIL(OPTIONAL)' column in row {index + 2 + skipped_rows}."
                    raise ErrorMessageException(error_message)

            if guardian_email:
                try:
                    email_validator(guardian_email)
                except Exception:
                    error_message = f"'{guardian_email}' is not a valid email address! Check the value in the 'GUARDIAN EMAIL(OPTIONAL)' column in row {index + 2 + skipped_rows}."
                    raise ErrorMessageException(error_message)

            user_no = random.randint(100, 999)
            username = f"{first_name.replace(' ', '')[0].upper()}{last_name.replace(' ', '').lower()}{user_no}"
            return {
                'first_name': first_name,
                'last_name': last_name,
                'username': username,
                'st_id': st_id,
                'gender': gender,
                'dob': dob,
                'date_enrolled': date_enrolled,
                'religion': religion,
                'region': region,
                'nationality': nationality,
                'pob': pob,
                'contact': contact,
                'email': email,
                'address': address,
                'guardian': guardian,
                'guardian_contact': guardian_contact,
                'guardian_gender': guardian_gender,
                'guardian_email': guardian_email,
                'guardian_occupation': guardian_occupation,
                'guardian_nationality': guardian_nationality,
                'guardian_address': guardian_address,
            }

        students_class = Classe.objects.prefetch_related('students').select_related('program', 'level').get(school=school, level=current_level, name=data['studentsClassName'])
        current_academic_year = AcademicYear.objects.get(id=int(data['year']))
        current_academic_term = int(data['term'])
        if StudentResult.objects.filter(student_class=students_class, academic_year=current_academic_year, academic_term=current_academic_term).exists():
            return Response({'message': 'There are students results for this class. Wait for the next academic year or ensure there are no students results'}, status=400)
        
        with transaction.atomic():
            try:
                for index, row in df.iterrows():
                    student_data = get_data(row)
                    user = User(
                        username=student_data['username'],
                        first_name=student_data['first_name'],
                        last_name=student_data['last_name'],
                    )
                    user.set_password(student_data['username'])
                    users_to_create.append(user)
                    students_to_create.append((student_data['username'], student_data))
                    students_to_create_ids.add(student_data['st_id'])

                User.objects.bulk_create(users_to_create)
                created_users = User.objects.filter(username__in=[user.username for user in users_to_create])
                user_mapping = {user.username: user for user in created_users}
                class_level = students_class.level
                students_year = students_class.students_year
                students_academic_years = AcademicYear.objects.filter(school=school).order_by('-start_date')[:int(students_year)]
                for username, student_data in students_to_create:
                    user = user_mapping[username]
                    student = Student(
                        user=user,
                        school=school,
                        current_level=class_level,
                        st_id=student_data['st_id'],
                        gender=student_data['gender'],
                        dob=student_data['dob'],
                        st_class=students_class,
                        current_program=students_class.program,
                        date_enrolled=student_data['date_enrolled'],
                        religion=student_data['religion'],
                        region=student_data['region'],
                        nationality=student_data['nationality'],
                        pob=student_data['pob'],
                        contact=student_data['contact'],
                        email=student_data['email'],
                        address=student_data['address'],
                        guardian=student_data['guardian'],
                        guardian_gender=student_data['guardian_gender'],
                        guardian_nationality=student_data['guardian_nationality'],
                        guardian_occupation=student_data['guardian_occupation'],
                        guardian_contact=student_data['guardian_contact'],
                        guardian_address=student_data['guardian_address'],
                        guardian_email=student_data['guardian_email'],
                    )
                    student_instances.append(student)

                Student.objects.bulk_create(student_instances)
                created_students = Student.objects.prefetch_related('academic_years', 'programs', 'levels').filter(school=school, st_id__in=students_to_create_ids)
                for _st in created_students:
                    _st.academic_years.set(students_academic_years)
                    _st.programs.add(students_class.program)
                    _st.levels.add(class_level)
                students_class.students.add(*created_students)
            except ErrorMessageException as e:
                transaction.set_rollback(True)
                return Response({'message': str(e)}, status=400)
            except Exception as e:
                transaction.set_rollback(True)
                return Response(status=400)
            
        created_students = Student.objects.select_related('user').filter(school=school, st_id__in=students_to_create_ids)
        students_data = StudentSerializerOne(created_students, many=True).data
        return Response(students_data, status=200)

    elif data['type'] == 'edit':
        with transaction.atomic():
            try:
                edit_type = data['editType']
                st_id = data['studentId']
                new_value = data['newValue'].strip() if isinstance(data['newValue'], str) else data['newValue']
                if edit_type in ['firstName', 'lastName']:
                    student = Student.objects.select_related('user').get(school=school, st_id=st_id)
                    user = student.user
                    user_no = random.randint(100, 999)
                    new_username = None
                    old_username = user.username
                    old_password = user.password
                    if edit_type == 'firstName':
                        user.first_name = new_value
                        new_username = f"{new_value.replace(' ', '')[0].upper()}{user.last_name.replace(' ', '').lower()}{user_no}"
                    elif edit_type == 'lastName':
                        user.last_name = new_value
                        new_username = f"{user.first_name.replace(' ', '')[0].upper()}{new_value.replace(' ', '').lower()}{user_no}"

                    if new_username:
                        user.username = new_username
                        if old_username == old_password:
                            user.set_password(new_username)
                        user.save()
                        if not current_level.students_id:
                            student.st_id = new_username
                            student.save()
                        return Response(
                            StudentSerializerOne(Student.objects.get(school=school, st_id=st_id)).data['user'],
                            status=200)
                elif edit_type == 'gender':
                    student = Student.objects.get(school=school, st_id=st_id)
                    student.gender = new_value
                    student.save()
                    return Response(new_value, status=200)
                elif edit_type == 'dob':
                    student = Student.objects.get(school=school, st_id=st_id)
                    student.dob = new_value
                    student.save()
                    return Response(new_value, status=200)
                elif edit_type == 'pob':
                    student = Student.objects.get(school=school, st_id=st_id)
                    student.pob = new_value
                    student.save()
                    return Response(new_value, status=200)
                elif edit_type == 'date_enrolled':
                    student = Student.objects.get(school=school, st_id=st_id)
                    student.date_enrolled = new_value
                    student.save()
                    return Response(new_value, status=200)
                elif edit_type == 'student_id' and current_level.students_id:
                    student = Student.objects.get(school=school, st_id=st_id)
                    student.st_id = new_value
                    student.save()
                    return Response(new_value, status=200)
                elif edit_type == 'region':
                    student = Student.objects.get(school=school, st_id=st_id)
                    student_nationality = student.nationality
                    countryinfo = PyCountryInfo()
                    student_country = countryinfo.get_country_from_nationality(student_nationality.title())
                    if student_country.lower() == 'ghana' and not countryinfo.is_valid_country_province('Ghana', new_value):
                        return Response({'message': f"'{new_value}' is not a valid region in Ghana!"}, status=400)
                    student.region = new_value
                    student.save()
                    return Response(new_value, status=200)

                elif edit_type == 'nationality':
                    student = Student.objects.get(school=school, st_id=st_id)
                    student.nationality = new_value
                    student.save()
                    return Response(new_value, status=200)

                elif edit_type == 'religion':
                    student = Student.objects.get(school=school, st_id=st_id)
                    student.religion = new_value
                    student.save()
                    return Response(new_value, status=200)

                elif edit_type == 'address':
                    student = Student.objects.get(school=school, st_id=st_id)
                    student.address = new_value
                    student.save()
                    return Response(new_value, status=200)

                elif edit_type == 'contact':
                    if not valid_phone_number(new_value):
                        return Response({'message': f"'{new_value}' is not a valid phone number. Ensure you include the country code and a plus(+) sign before the number"}, status=400)
                    student = Student.objects.get(school=school, st_id=st_id)
                    student.contact = new_value
                    student.save()
                    return Response(new_value, status=200)

                elif edit_type == 'email':
                    if not valid_email(new_value):
                        return Response({'message': f"'{new_value}' is not a valid email address"}, status=400)
                    student = Student.objects.get(school=school, st_id=st_id)
                    student.email = new_value
                    student.save()
                    return Response(new_value, status=200)

                elif edit_type == 'img':
                    if not imghdr.what(new_value):
                        return Response({'message': f"Invalid image"}, status=400)
                    student = Student.objects.get(school=school, st_id=st_id)
                    student.img = new_value
                    student.save()
                    return Response(StudentSerializerOne(Student.objects.get(school=school, st_id=st_id)).data['img'], status=200)

                elif edit_type == 'guardian':
                    student = Student.objects.get(school=school, st_id=st_id)
                    student.guardian = new_value
                    student.save()
                    return Response(new_value, status=200)

                elif edit_type == 'guardianOccupation':
                    student = Student.objects.get(school=school, st_id=st_id)
                    student.guardian_occupation = new_value
                    student.save()
                    return Response(new_value, status=200)

                elif edit_type == 'guardianAddress':
                    student = Student.objects.get(school=school, st_id=st_id)
                    student.guardian_address = new_value
                    student.save()
                    return Response(new_value, status=200)

                elif edit_type == 'guardianGender':
                    student = Student.objects.get(school=school, st_id=st_id)
                    student.guardian_gender = new_value
                    student.save()
                    return Response(new_value, status=200)

                elif edit_type == 'guardianContact':
                    if not valid_phone_number(new_value):
                        return Response({'message': f"'{new_value}' is not a valid phone number"}, status=400)
                    student = Student.objects.get(school=school, st_id=st_id)
                    student.guardian_contact = new_value
                    student.save()
                    return Response(new_value, status=200)
                elif edit_type == 'guardianNationality':
                    student = Student.objects.get(school=school, st_id=st_id)
                    student.guardian_nationality = new_value
                    student.save()
                    return Response(new_value, status=200)
                elif edit_type == 'guardianEmail':
                    if not valid_email(new_value):
                        return Response({'message': f"'{new_value}' is not a valid email address"}, status=400)
                    student = Student.objects.get(school=school, st_id=st_id)
                    student.guardian_email = new_value
                    student.save()
                    return Response(new_value, status=200)

                else:
                    raise Exception
            except Exception as e:
                transaction.set_rollback(True)
                return Response(status=400)


    elif data['type'] == 'delete':
        student_to_delete = Student.objects.select_related('user').get(school=school, st_id=data['studentId'])
        user = student_to_delete.user
        
        if StudentAttendance.objects.filter(Q(students_present=student_to_delete) | Q(students_absent=student_to_delete), school=school).exists():
            return Response({'message': "You don't have permission to delete this student"}, status=400)
        
        if Assessment.objects.filter(school=school, student=student_to_delete).exists():
            return Response({'message': "You don't have permission to delete this student"}, status=400)

        if Exam.objects.filter(school=school, student=student_to_delete).exists():
            return Response({'message': "You don't have permission to delete this student"}, status=400)

        if StudentResult.objects.filter(school=school, student=student_to_delete).exists():
            return Response({'message': "You don't have permission to delete this student"}, status=400)

        with transaction.atomic():
            try:
                user.delete()
            except Exception as e:
                transaction.set_rollback(True)
                return Response(status=400)

        return Response(status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def school_admin_subject_assignment(request):
    data = request.data
    sch_admin = Staff.objects.select_related('current_role__level', 'school').get(user=request.user)
    current_level = sch_admin.current_role.level
    school = sch_admin.school
    current_academic_year = AcademicYear.objects.get(school=school, level=current_level, name=data['year'])
    current_term = int(data['term'])
    
    if data['type'] == 'upload':
        students_class = Classe.objects.prefetch_related('subjects').get(school=school, level=current_level, name=data['studentsClassName'])
        teacher = Staff.objects.prefetch_related('subjects').select_related('user').get(school=school, staff_id=data['teacher'])
        subjects = json.loads(data['subjects'])
        subjects_obj = Subject.objects.filter(name__in=subjects).distinct()
        teacher_subjects = teacher.subjects.all()
        students_class_subjects = students_class.subjects.all()
        existing_subject_assignments = SubjectAssignment.objects.select_related('teacher__user').prefetch_related('subjects').filter(school=school, students_class=students_class, academic_year=current_academic_year, academic_term=current_term)
        for _subject in subjects_obj:
            if _subject not in teacher_subjects:
                return Response({'message': f"{teacher.title} {teacher.user.get_full_name()} doesn't teach {_subject.name}"}, status=400)
            elif _subject not in students_class_subjects:
                return Response({'message': f"The {students_class.name} class doesn't study {_subject.name}."}, status=400)
            for _assign in existing_subject_assignments:
                existing_subject_assignments_subjects = _assign.subjects.all()
                if _subject in existing_subject_assignments_subjects:
                    return Response({'message': f"{_assign.teacher.title} {_assign.teacher.user.get_full_name()} is already teaching the {students_class.name} {_subject.name}"}, status=400)

        with transaction.atomic():
            try:
                assignment_obj = SubjectAssignment.objects.create(
                    school=school,
                    assigned_by=sch_admin,
                    students_class=students_class,
                    teacher=teacher,
                    level=current_level,
                    academic_year=current_academic_year,
                    academic_term=current_term,
                )
                assignment_obj.subjects.set(subjects_obj)
                assignment_obj.save()
            except IntegrityError:
                transaction.set_rollback(True)
                return Response({'message': f"{teacher.title} {teacher.user.first_name} {teacher.user.last_name} is already teaching the {students_class.name} class {[_sub.name for _sub in teacher_subjects]}"}, status=400)
            except Exception:
                transaction.set_rollback(True)
                return Response(status=400)

        subject_assignment = SubjectAssignment.objects.prefetch_related('subjects').select_related('teacher__user', 'students_class').get(id=assignment_obj.id)
        subject_assignments_data = SubjectAssignmentSerializerOne(subject_assignment).data
        return Response(subject_assignments_data, status=200)

    elif data['type'] == 'delete':
        subject_assignment = SubjectAssignment.objects.select_related('teacher__user', 'students_class').prefetch_related('subjects').get(school=school, id=data['id'])
        assignment_subjects = subject_assignment.subjects.all()
        assignment_teacher = subject_assignment.teacher
        students_class = subject_assignment.students_class
        for _subj in assignment_subjects:
            existing_exams = Exam.objects.filter(school=school, student_class=students_class, teacher=assignment_teacher, subject=_subj, academic_year=current_academic_year, academic_term=current_term).first()
            if existing_exams:
                return Response({'message': f"{assignment_teacher.title} {assignment_teacher.user.get_full_name()} has already uploaded {_subj.name} exams data for students for the {current_academic_year.name} {current_academic_year.period_division} {current_term}."}, status=400)
            
            existing_assessments = Assessment.objects.filter(school=school, student_class=students_class, teacher=assignment_teacher, subject=_subj, academic_year=current_academic_year, academic_term=current_term).first()
            if existing_assessments:
                return Response({'message': f"{assignment_teacher.title} {assignment_teacher.user.get_full_name()} has already uploaded {_subj.name} assessment data for students for the {current_academic_year.name} {current_academic_year.period_division} {current_term}."}, status=400)
            
        with transaction.atomic():
            try:
                subject_assignment.delete()
                return Response(status=200)
            except Exception:
                transaction.set_rollback(True)
                return Response(status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def release_results(request):
    data = request.data
    sch_admin = Staff.objects.select_related('current_role__level', 'school').get(user=request.user)
    current_level = sch_admin.current_role.level
    school = sch_admin.school
    
    if data['type'] == 'upload':
        students_class = Classe.objects.prefetch_related('subjects', 'students').get(school=school, level=current_level, name=data['studentsClassName'])
        class_name = students_class.name
        class_subjects = students_class.subjects.all()
        academic_year = AcademicYear.objects.get(school=school, level=current_level, name=data['year'])
        term = int(data['term'])
        existing_released_results = ReleasedResult.objects.filter(school=school, level=current_level, students_class_name=class_name, academic_year=academic_year, academic_term=term).exists()
        if existing_released_results:
            return Response({'message': f"You have already released the {class_name} students results"}, status=400)
        
        results_subjects_names = set(StudentResult.objects.filter(school=school, level=current_level, subject__in=class_subjects).values_list('subject__name', flat=True))
        for subject in class_subjects:
            if subject.name not in results_subjects_names:
                return Response({'message': f"There are no results for the subject '{subject.name}'. Ensure there are results for all the subjects in this class."}, status=400)
        
        with transaction.atomic():
            released_result_obj = ReleasedResult.objects.create(
                school=school,
                level=current_level,
                academic_year=academic_year,
                academic_term=term,
                released_by=sch_admin,
                students_class_name=class_name,
            )
            released_result_obj.students.set(students_class.students.all())
        
        release_results_data = ReleasedResultsSerializer(released_result_obj).data
        return Response(release_results_data, status=200)

    elif data['type'] == 'delete':
        current_academic_year = AcademicYear.objects.get(id=int(data['year']))
        released_result = ReleasedResult.objects.select_related('academic_year').get(id=int(data['id']))
        if released_result.academic_year != current_academic_year:
            return Response({'message': f"You don't have permission to rollback this released results"}, status=400)
        
        released_result.delete()
        return Response(status=200)
 
 