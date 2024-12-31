# Django Restframework
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.core.validators import EmailValidator
from api.utils import get_staff_creation_file, get_students_creation_file, ErrorMessageException, valid_phone_number, valid_email
from api.models import *
from api.serializer import (
    SchoolSerializer, SuperuserEducationalLevelSerializer, SuperuserProgramSerializer, SuperuserSubjectsSerializer, SuperuserDepartmentSerializer, 
    SuperuserGradingSystemSerializer, SuperuserGradingSystemSerializer, SuperuserClasseSerializer, StaffUserIdSerializer, SuperuserGradingSystemRangeSerializer,
    AcademicYearSerializer, StaffRoleSerializer, StaffSerializerOne
)

import imghdr
from django.db import transaction
import json
from pycountryinfo.countryinfo import PyCountryInfo
from django.forms import DateField


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_superuser_data(request):
    schools_data = SchoolSerializer(School.objects.all().order_by('-date_created'), many=True).data
    levels = SuperuserEducationalLevelSerializer(EducationalLevel.objects.prefetch_related('schools').all(), many=True).data
    programs = SuperuserProgramSerializer(Program.objects.prefetch_related('subjects', 'schools').select_related('level').all(), many=True).data
    subjects = SuperuserSubjectsSerializer(Subject.objects.select_related('level').prefetch_related('schools').all(), many=True).data
    grading_system_ranges = SuperuserGradingSystemRangeSerializer(GradingSystemRange.objects.all(), many=True).data
    grading_systems = SuperuserGradingSystemSerializer(GradingSystem.objects.select_related('level').prefetch_related('schools', 'ranges').all(), many=True).data
    staff_roles = StaffRoleSerializer(StaffRole.objects.prefetch_related('levels').all(), many=True).data
    class_data = {}
    department_data = {}
    academic_year_data = {}
    staff_data = {}
    schools = School.objects.all()
    for _school in schools:
        academic_years = AcademicYear.objects.filter(school=_school)
        academic_year_data[_school.identifier] = AcademicYearSerializer(academic_years, many=True).data
        departments = Department.objects.select_related('level', 'school', 'hod').prefetch_related('subjects').filter(school=_school)
        department_data[_school.identifier] = SuperuserDepartmentSerializer(departments, many=True).data
        classes = Classe.objects.select_related('level', 'program', 'head_teacher__user', 'linked_class').prefetch_related('subjects').filter(school=_school)
        class_data[_school.identifier] = SuperuserClasseSerializer(classes, many=True).data
        staff = Staff.objects.select_related('user').prefetch_related('subjects', 'levels', 'roles', 'departments').filter(school=_school)
        staff_data[_school.identifier] = StaffSerializerOne(staff, many=True).data
    
    return Response({
        'schools': schools_data,
        'levels': levels,
        'programs': programs,
        'grading_systems': grading_systems,
        'subjects': subjects,
        'departments': department_data,
        'classes': class_data,
        'grading_system_ranges': grading_system_ranges,
        'academic_years': academic_year_data,
        'staff_roles': staff_roles,
        'staff': staff_data,
    }, status=200)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def superuser_schools(request):
    data = request.data
    if data['type'] == 'create':
        name = data['name'].strip()
        short_name = data['shortName'].strip()
        code = data['code'].strip()
        logo = data['logo']
        if logo and not imghdr.what(logo):
            logo = None
        address = data['address'].strip()
        region = data['region'].strip()
        city_town = data['cityTown'].strip()
        postal_address = data['postalAddress'].strip()
        contact = data['contact'].strip()
        alt_contact = data['altContact'].strip()
        email = data['email'].strip()
        staff_id = json.loads(data['staffId'])
        identifier = f"{name} | {city_town} | {contact}"
        
        with transaction.atomic():
            School.objects.create(
                name=name,
                short_name=short_name,
                identifier=identifier,
                code=code,
                logo=logo,
                address=address,
                postal_address=postal_address,
                contact=contact,
                alt_contact=alt_contact,
                email=email,
                region=region,
                city_town=city_town,
                staff_id=staff_id,
            )
        
        school_data = SchoolSerializer(School.objects.get(identifier=identifier)).data
        
        return Response(school_data, status=200)  
    
    elif data['type'] == 'delete':
        identifier = data['identifier']
        school = School.objects.get(identifier=identifier)
        if Student.objects.filter(school=school).exists():
            return Response({'message': f'There are students in this school [{school.name}]. Delete the students before'}, status=400)
        elif Classe.objects.filter(school=school).exists():
            return Response({'message': f'There are classes in this school [{school.name}]. Delete the classes before'}, status=400)
        elif AcademicYear.objects.filter(school=school).exists():
            return Response({'message': f'There are academic year data in this school [{school.name}]. Delete those data before'}, status=400)
        elif Department.objects.filter(school=school).exists():
            return Response({'message': f'There are department data in this school [{school.name}]. Delete those data before'}, status=400)
        elif GraduatedClasse.objects.filter(school=school).exists():
            return Response({'message': f'There are graduated classes data in this school [{school.name}]. Delete those data before'}, status=400)
        elif LinkedClasse.objects.filter(school=school).exists():
            return Response({'message': f'There are linked classes data in this school [{school.name}]. Delete those data before'}, status=400)
        elif SubjectAssignment.objects.filter(school=school).exists():
            return Response({'message': f'There are subject assignments data in this school [{school.name}]. Delete those data before'}, status=400)
        elif Assessment.objects.filter(school=school).exists():
            return Response({'message': f'There are assessments data in this school [{school.name}]. Delete those data before'}, status=400)
        elif Exam.objects.filter(school=school).exists():
            return Response({'message': f'There are exams data in this school [{school.name}]. Delete those data before'}, status=400)
        elif StudentResult.objects.filter(school=school).exists():
            return Response({'message': f'There are student results data in this school [{school.name}]. Delete those data before'}, status=400)
        elif StudentAttendance.objects.filter(school=school).exists():
            return Response({'message': f'There are students attendance data in this school [{school.name}]. Delete those data before'}, status=400)
        
        with transaction.atomic():
            school.delete()
        
        return Response(status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def superuser_levels(request):
    data = request.data
    if data['type'] == 'create':
        name = data['name'].strip().upper()
        years_to_complete = data['yearsToComplete']
        has_departments = json.loads(data['hasDepartments'])
        has_programs = json.loads(data['hasPrograms'])
        students_id = json.loads(data['studentsId'])
        students_index_no = json.loads(data['studentsIndexNo'])
        identifier = f"{name} | {years_to_complete} | {has_departments} | {has_programs} | {students_id} | {students_index_no}"
        if EducationalLevel.objects.filter(identifier=identifier).exists():
            return Response({'message': f'Level with identifier [ {identifier} ] already exists'}, status=400)
        
        with transaction.atomic():
            try:
                EducationalLevel.objects.create(
                    name=name,
                    years_to_complete=years_to_complete,
                    has_departments=has_departments,
                    has_programs=has_programs,
                    students_id=students_id,
                    students_index_no=students_index_no,
                    identifier=identifier,
                )
            except Exception:
                return Response(status=400)
        
        level_data = SuperuserEducationalLevelSerializer(EducationalLevel.objects.get(identifier=identifier)).data
        
        return Response(level_data, status=200)  
    
    elif data['type'].split('S')[-1] == 'chool':
        level_identifier = data['levelIdentifier']
        school_identifier = data['schoolIdentifier']
        level = EducationalLevel.objects.prefetch_related('schools').get(identifier=level_identifier)
        school = School.objects.get(identifier=school_identifier)
        try:
            level.schools.add(school) if data['type'].split('S')[0] == 'add' else level.schools.remove(school)
        except Exception:
            return Response(status=400)         
        
        return Response(status=200)
    
    elif data['type'] == 'delete':
        identifier = data['identifier']
        level = EducationalLevel.objects.get(identifier=identifier)
        if Student.objects.filter(level=level).exists():
            return Response({'message': f'There are students in this level. Delete the students before'}, status=400)
        elif Classe.objects.filter(level=level).exists():
            return Response({'message': f'There are classes in this level. Delete the classes before'}, status=400)
        elif AcademicYear.objects.filter(level=level).exists():
            return Response({'message': f'There are academic year data in this level. Delete those data before'}, status=400)
        elif Department.objects.filter(level=level).exists():
            return Response({'message': f'There are department data in this level. Delete those data before'}, status=400)
        elif LinkedClasse.objects.filter(level=level).exists():
            return Response({'message': f'There are linked classes data in this level. Delete those data before'}, status=400)
        elif SubjectAssignment.objects.filter(level=level).exists():
            return Response({'message': f'There are subject assignments data in this level. Delete those data before'}, status=400)
        elif Assessment.objects.filter(level=level).exists():
            return Response({'message': f'There are assessments data in this level. Delete those data before'}, status=400)
        elif Exam.objects.filter(level=level).exists():
            return Response({'message': f'There are exams data in this level. Delete those data before'}, status=400)
        elif StudentResult.objects.filter(level=level).exists():
            return Response({'message': f'There are student results data in this level. Delete those data before'}, status=400)
        elif StudentAttendance.objects.filter(level=level).exists():
            return Response({'message': f'There are students attendance data in this level. Delete those data before'}, status=400)
        
        with transaction.atomic():
            level.delete()
        
        return Response(status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def superuser_subjects(request):
    data = request.data
    if data['type'] == 'create':
        name = data['name'].strip().upper()
        level_identifier = data['levelIdentifier']
        identifier = f"{name} | {level_identifier}"
        if Subject.objects.filter(identifier=identifier).exists():
            return Response({'message': f'Subject with identifier [ {identifier} ] already exists'}, status=400)
        
        level = EducationalLevel.objects.get(identifier=level_identifier)
        with transaction.atomic():
            try:
                Subject.objects.create(
                    name=name,
                    identifier=identifier,
                    level=level,
                )
            except Exception:
                return Response(status=400)
        
        subject_data = SuperuserSubjectsSerializer(Subject.objects.get(identifier=identifier)).data
        
        return Response(subject_data, status=200)  
    
    elif data['type'].split('S')[-1] == 'chool':
        subject_identifier = data['subjectIdentifier']
        school_identifier = data['schoolIdentifier']
        subject = Subject.objects.prefetch_related('schools').get(identifier=subject_identifier)
        school = School.objects.get(identifier=school_identifier)
        try:
            subject.schools.add(school) if data['type'].split('S')[0] == 'add' else subject.schools.remove(school)
        except Exception:
            return Response(status=400)         
        
        return Response(status=200)
    
    elif data['type'] == 'delete':
        identifier = data['identifier']
        subject = Subject.objects.get(identifier=identifier)
        if Assessment.objects.filter(subject=subject).exists():
            return Response({'message': f'There are assessments data for this subject. Delete those data before'}, status=400)
        elif Exam.objects.filter(subject=subject).exists():
            return Response({'message': f'There are exams data for this subject. Delete those data before'}, status=400)
        elif StudentResult.objects.filter(subject=subject).exists():
            return Response({'message': f'There are student results data for this subject. Delete those data before'}, status=400)
        
        with transaction.atomic():
            subject.delete()
        
        return Response(status=200)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def superuser_programs(request):
    data = request.data
    if data['type'] == 'create':
        name = data['name'].strip().upper()
        level_identifier = data['levelIdentifier']
        identifier = f"{name} | {level_identifier}"
        if Program.objects.filter(identifier=identifier).exists():
            return Response({'message': f'Program with identifier [ {identifier} ] already exists'}, status=400)
        
        level = EducationalLevel.objects.get(identifier=level_identifier)
        with transaction.atomic():
            try:
                Program.objects.create(
                    name=name,
                    identifier=identifier,
                    level=level,
                )
            except Exception:
                return Response(status=400)
        
        program_data = SuperuserProgramSerializer(Program.objects.get(identifier=identifier)).data
        
        return Response(program_data, status=200)  
    
    elif data['type'].split('S')[-1] == 'chool':
        program_identifier = data['programIdentifier']
        school_identifier = data['schoolIdentifier']
        program = Program.objects.prefetch_related('schools').get(identifier=program_identifier)
        school = School.objects.get(identifier=school_identifier)
        try:
            program.schools.add(school) if data['type'].split('S')[0] == 'add' else program.schools.remove(school)
        except Exception:
            return Response(status=400)         
        
        return Response(status=200)
    
    elif data['type'].split('S')[-1] == 'ubject':
        program_identifier = data['programIdentifier']
        subject_identifier = data['subjectIdentifier']
        program = Program.objects.prefetch_related('subjects').get(identifier=program_identifier)
        subject = Subject.objects.get(identifier=subject_identifier)
        try:
            program.subjects.add(subject) if data['type'].split('S')[0] == 'add' else program.subjects.remove(subject)
        except Exception:
            return Response(status=400)         
        
        return Response(status=200)
    
    elif data['type'] == 'delete':
        identifier = data['identifier']
        program = Program.objects.get(identifier=identifier)
        if Classe.objects.filter(program=program).exists():
            return Response({'message': f'There are classes doing this program. Remove the program from the classes before'}, status=400)
        elif Student.objects.filter(program=program).exists():
            return Response({'message': f'There are students doing this program. Remove the program from the students before'}, status=400)
        
        with transaction.atomic():
            program.delete()
        
        return Response(status=200)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def superuser_departments(request):
    data = request.data
    if data['type'] == 'create':
        name = data['name'].strip().upper()
        level_identifier = data['levelIdentifier']
        school_identifier = data['schoolIdentifier']
        identifier = f"{name} | {level_identifier} | {school_identifier}"
        if Department.objects.filter(identifier=identifier).exists():
            return Response({'message': f'Department with identifier [ {identifier} ] already exists'}, status=400)
        
        level = EducationalLevel.objects.get(identifier=level_identifier)
        school = School.objects.get(identifier=school_identifier)
        with transaction.atomic():
            try:
                Department.objects.create(
                    name=name,
                    identifier=identifier,
                    level=level,
                    school=school,
                )
            except Exception:
                return Response(status=400)
        
        department_data = SuperuserDepartmentSerializer(Department.objects.get(identifier=identifier)).data        
        
        return Response(department_data, status=200)  
    
    elif data['type'].split('S')[-1] == 'ubject':
        subject_identifiers = json.loads(data['subjectIdentifiers'])
        department = Department.objects.prefetch_related('subjects').get(id=int(data['departmentId']))
        subject = Subject.objects.filter(identifier__in=subject_identifiers)
        try:
            department.subjects.add(*subject) if data['type'].split('S')[0] == 'add' else department.subjects.remove(*subject)
        except Exception as e:
            return Response(status=400)         
        
        return Response(status=200)
    
    elif data['type'] == 'delete':
        department = Department.objects.select_related('hod').prefetch_related('teachers').get(id=int(data['id']))
        if department.hod:
            return Response({'message': f'There is an hod for this department. Remove it before'}, status=400)
        elif department.teachers.all().exists():
            return Response({'message': f'There are teachers in this department. Remove them before'}, status=400)
        
        with transaction.atomic():
            department.delete()
        
        return Response(status=200)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def superuser_classes(request):
    data = request.data
    if data['type'] == 'create':
        name = data['name'].strip().upper()
        level_identifier = data['levelIdentifier']
        school_identifier = data['schoolIdentifier']
        students_year = int(data['studentsYear'])
        program = data['programIdentifier'] if data['programIdentifier'] else None
        identifier = f"{name} | {students_year} | {level_identifier} | {school_identifier}"
        if Classe.objects.filter(identifier=identifier).exists():
            return Response({'message': f'Class with identifier [ {identifier} ] already exists'}, status=400)
        
        level = EducationalLevel.objects.get(identifier=level_identifier)
        school = School.objects.get(identifier=school_identifier)
        with transaction.atomic():
            try:
                Classe.objects.create(
                    name=name,
                    identifier=identifier,
                    level=level,
                    school=school,
                    students_year=students_year,
                    program=Program.objects.get(identifier=program) if program else None,
                )
            except Exception:
                return Response(status=400)
        
        classe_data = SuperuserClasseSerializer(Classe.objects.get(identifier=identifier)).data        
        return Response(classe_data, status=200)  
    
    elif data['type'] == 'linkClass':
        classe = Classe.objects.select_related('linked_class').get(id=int(data['id']))
        to_class = Classe.objects.get(id=int(data['toClassId']))
        try:
            classe.linked_class = to_class
            classe.save()
        except Exception:
            return Response(status=400)
        
        return Response(to_class.identifier, status=200)
    
    elif data['type'] == 'unLinkClass':
        classe = Classe.objects.get(id=int(data['id']))
        try:
            classe.linked_class = None
            classe.save()
        except Exception:
            return Response(status=400)
        
        return Response(status=200)
        
    elif data['type'].split('S')[-1] == 'ubject':
        subject_identifiers = json.loads(data['subjectIdentifiers'])
        classe = Classe.objects.prefetch_related('subjects').get(id=data['classId'])
        subject = Subject.objects.filter(identifier__in=subject_identifiers)
        try:
            classe.subjects.add(*subject) if data['type'].split('S')[0] == 'add' else classe.subjects.remove(*subject)
        except Exception as e:
            return Response(status=400)         
        
        return Response(status=200)
    
    elif data['type'] == 'delete':
        classe = Classe.objects.prefetch_related('students').get(id=int(data['id']))
        if classe.students.all().exists():
            return Response({'message': f'There are students in this class. Remove them before'}, status=400)
        elif LinkedClasse.objects.filter(Q(from_class=classe) | Q(to_class=classe)).exists():
            return Response({'message': f'There is a linked class for this class. Remove it before'}, status=400)
        elif Assessment.objects.filter(student_class=classe).exists():
            return Response({'message': f'There are students assessment data for this class. Remove those data before'}, status=400)
        elif StudentResult.objects.filter(student_class=classe).exists():
            return Response({'message': f'There are students results data for this class. Remove those data before'}, status=400)
        elif Exam.objects.filter(student_class=classe).exists():
            return Response({'message': f'There are students exams data for this class. Remove those data before'}, status=400)
        elif StudentAttendance.objects.filter(students_class=classe).exists():
            return Response({'message': f'There are students attendance data for this class. Remove those data before'}, status=400)
        
        with transaction.atomic():
            classe.delete()
        
        return Response(status=200)
    
     
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def superuser_grading_system_ranges(request):
    data = request.data
    if data['type'] == 'create':
        label = data['label'].strip().upper()
        lower_limit = float(data['lowerLimit'])
        upper_limit = float(data['upperLimit'])
        remark = data['remark'].strip().upper()
        identifier = f"{label} | {upper_limit} | {lower_limit} | {remark}"
        if GradingSystemRange.objects.filter(identifier=identifier).exists():
            return Response({'message': f'Grading system range with identifier [ {identifier} ] already exists'}, status=400)
        with transaction.atomic():
            try:
                GradingSystemRange.objects.create(
                    label=label,
                    identifier=identifier,
                    lower_limit=lower_limit,
                    upper_limit=upper_limit,
                    remark=remark,
                )
            except Exception:
                return Response(status=400)
        
        grading_system_range_data = SuperuserGradingSystemRangeSerializer(GradingSystemRange.objects.get(identifier=identifier)).data        
        return Response(grading_system_range_data, status=200)  
    
    elif data['type'] == 'delete':
        grading_system_range = GradingSystemRange.objects.get(id=int(data['id']))
        if GradingSystem.objects.filter(ranges=grading_system_range).exists():
            return Response({'message': f'There are grading systems using this range. Remove the range from the grading system before'}, status=400)
        
        with transaction.atomic():
            grading_system_range.delete()
        
        return Response(status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def superuser_grading_systems(request):
    data = request.data
    if data['type'] == 'create':
        level = EducationalLevel.objects.get(identifier=data['levelIdentifier'])
        grading_system = None
        with transaction.atomic():
            try:
                grading_system = GradingSystem.objects.create(
                    level=level,
                )
            except Exception:
                return Response(status=400)
        
        grading_system_data = SuperuserGradingSystemSerializer(grading_system).data
        return Response(grading_system_data, status=200)
    
    elif data['type'].split('S')[-1] == 'chool':
        school = School.objects.get(identifier=data['schoolIdentifier'])
        grading_system = GradingSystem.objects.prefetch_related('schools').get(id=int(data['gradingSystemId']))
        try:
            grading_system.schools.add(school) if data['type'].split('S')[0] == 'add' else grading_system.schools.remove(school)
        except Exception as e:
            return Response(status=400)         
        
        return Response(status=200)
    
    elif data['type'].split('R')[-1] == 'ange':
        grading_system_ranges = GradingSystemRange.objects.filter(identifier__in=json.loads(data['rangesIdentifiers']))
        grading_system = GradingSystem.objects.prefetch_related('ranges').get(id=int(data['gradingSystemId']))
        try:
            grading_system.ranges.add(*grading_system_ranges) if data['type'].split('S')[0] == 'add' else grading_system.ranges.remove(*grading_system_ranges)
        except Exception as e:
            return Response(status=400)         
        
        return Response(status=200)
    
    elif data['type'] == 'delete':
        grading_system = GradingSystem.objects.prefetch_related('schools').get(id=int(data['id']))
        if grading_system.schools.all().exists():
            return Response({'message': f'There are schools using this grading system. Remove the schools before'}, status=400)
        
        with transaction.atomic():
            grading_system.delete()
        
        return Response(status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def superuser_academic_years(request):
    data = request.data
    if data['type'] == 'create':
        school = School.objects.get(identifier=data['schoolIdentifier'])
        level = EducationalLevel.objects.get(identifier=data['levelIdentifier'])
        name = data['name'].strip()
        start_date = data['startDate']
        end_date = data['endDate']
        term_1_end_date = data['termOneEndDate']
        term_2_start_date = data['termTwoStartDate']
        term_2_end_date = data['termTwoEndDate']
        term_3_start_date = data['termThreeStartDate'] if data['termThreeStartDate'] else None
        term_3_end_date = data['termThreeEndDate'] if data['termThreeEndDate'] else None
        period_division = data['periodDivision']
        no_divisions = data['noDivisions']
        students_graduation_date = data['studentsGraduationDate'] if data['studentsGraduationDate'] else None
        if AcademicYear.objects.filter(school=school, level=level, name=name).exists():
            return Response({'message': f'Academic year with this name already exists'}, status=400)
        
        existing_academic_year = AcademicYear.objects.filter(school=school, level=level).order_by('-start_date').first()
        if existing_academic_year and existing_academic_year.end_date <= timezone.now().date():
            return Response({'message': f'The current academic year has not ended'}, status=400)
        
        with transaction.atomic():
            try:
                AcademicYear.objects.create(
                    school=school,
                    level=level,
                    name=name,
                    start_date=start_date,
                    end_date=end_date,
                    term_1_end_date=term_1_end_date,
                    term_2_start_date=term_2_start_date,
                    term_2_end_date=term_2_end_date,
                    term_3_start_date=term_3_start_date,
                    term_3_end_date=term_3_end_date,
                    period_division=period_division,
                    no_divisions=no_divisions,
                    students_graduation_date=students_graduation_date,
                )
            except Exception:
                return Response(status=400)
        
        academic_year_data = AcademicYearSerializer(AcademicYear.objects.get(school=school, level=level, name=name)).data
        return Response(academic_year_data, status=200)  
    
    elif data['type'] == 'delete':
        academic_year = AcademicYear.objects.get(id=int(data['id']))
        
        if SubjectAssignment.objects.filter(academic_year=academic_year).exists():
            return Response({'message': f'There are subject assignment data with this academic year'}, status=400)
        if StudentAttendance.objects.filter(academic_year=academic_year).exists():
            return Response({'message': f'There are student attendance data with this academic year'}, status=400)
        if Assessment.objects.filter(academic_year=academic_year).exists():
            return Response({'message': f'There are student assessment data with this academic year'}, status=400)
        if Exam.objects.filter(academic_year=academic_year).exists():
            return Response({'message': f'There are exams data with this academic year'}, status=400)
        if StudentResult.objects.filter(academic_year=academic_year).exists():
            return Response({'message': f'There are student results data with this academic year'}, status=400)
        
        with transaction.atomic():
            academic_year.delete()
        
        return Response(status=200)
    


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def superuser_staff(request):
    data = request.data

    if data['type'] == 'createWithoutFile':
        date_field = DateField()
        email_validator = EmailValidator()
        department = None
        staff_id = None
        school = School.objects.get(identifier=data['schoolIdentifier'])
        levels = EducationalLevel.objects.filter(schools=school, name__in=json.loads(data['levels']))
        first_name = data['firstName'].strip()
        last_name = data['lastName'].strip()
        title = data['title'].title()
        role = data['role'].lower()
        gender = data['gender'].lower()
        img = data['img'] if data['img'] else ''
        if img and not imghdr.what(img):
            return Response({'message': f"Invalid image! Check the staff image"}, status=400)
        contact = data['contact'].strip()
        address = data['address'].strip()
        date_enrolled = data['dateEnrolled']
        levels = json.loads(data['levels'])
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

        if current_level.has_departments and role == 'teacher':
            department = Department.objects.get(school=school, level=current_level, name=data['department'])

        user_no = random.randint(100, 999)
        username = f"{first_name.replace(' ', '')[0].upper()}{last_name.replace(' ', '').lower()}{user_no}"
        if school.staff_id:
            staff_id = data['staff_id']
        else:
            staff_id = username

        if Staff.objects.filter(school=school, staff_id=staff_id).exists():
            return Response({'message': f"Staff with ID [ {staff_id} ] already exists"}, status=400)

        if role.lower() in ['head master', 'head mistress', 'assistant head master', 'assistant head mistress']:
            
            return Response({'message': f"Staff with a role of '{role}' already exists"}, status=400)

        if role == 'head' and gender == 'male':
            role = 'head master'
        elif role == 'head' and gender == 'female':
            role = 'head mistress'
        elif role == 'assistant head' and gender == 'male':
            role = 'assistant head master'
        elif role == 'assistant head' and gender == 'female':
            role = 'assistant head mistress'
            
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
                    department=department,
                    role=role,
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
                    date_enrolled=date_enrolled,
                    nationality=nationality.lower(),
                    img=img,
                    is_active=True,
                )
                levels = EducationalLevel.objects.filter(name__in=levels)
                staff.levels.set(levels)
                subjects_objs = Subject.objects.filter(level=current_level, name__in=subjects).distinct()
                staff_obj.subjects.set(subjects_objs)
                user.save()
                staff_obj.save()
                if department:
                    department.teachers.add(staff_obj)

            except Exception as e:
                print(e)
                transaction.set_rollback(True)
                return Response(status=400)

        staff_data = StaffSerializerOne(Staff.objects.get(school=school, staff_id=staff_id)).data
        return Response(staff_data, status=200)

    elif data['type'] == 'setDepartmentHOD':
        staff_hod = Staff.objects.select_related('department').get(school=school, staff_id=data['staffId'])
        department = Department.objects.prefetch_related('teachers').select_related('hod').get(school=school, level=current_level, name=data['department'])
        previous_hod_id = None
        if staff_hod not in department.teachers.all():
            transaction.set_rollback(True)
            return Response({'message': f"The staff you selected is not in the {department} department"}, status=400)

        with transaction.atomic():
            try:
                if department.hod:
                    previous_hod = department.hod
                    previous_hod_new_role = StaffRole.objects.get(name='teacher')
                    previous_hod.role = previous_hod_new_role
                    previous_hod_id = previous_hod.staff_id
                    previous_hod.save()
                department.hod = staff_hod
                staff_hod_new_role = StaffRole.objects.get(name='hod')
                staff_hod.role = staff_hod_new_role
                department.save()
                staff_hod.save()
            except:
                transaction.set_rollback(True)
                return Response(status=400)

        return Response({'previous_hod_id': previous_hod_id}, status=200)

    elif data['type'] == 'getFile':
        filepath = get_staff_creation_file(sch_admin)
        filename = 'staff-creation-file.xlsx'
        response = FileResponse(filepath, as_attachment=True, filename=filename)
        response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response['Access-Control-Expose-Headers'] = 'Content-Disposition'
        return response

    elif data['type'] == 'createWithFile':
        df = None
        title_options = ['Mr', 'Miss', 'Mrs', 'Dr', 'Prof', 'Rev', 'Sir', 'Hon', 'Madam', 'Pastor', 'Imam', 'Bishop', 'Archbishop']
        religion_options = ['Christianity', 'Islam', 'Traditional African Religions', 'Buddhism', 'Hinduism', 'Sikhism', 'Judaism', 'Other', 'None']
        skipped_rows = 0
        date_field = DateField()
        email_validator = EmailValidator()
        staff_to_create_ids = set()
        existing_staff_ids = []
        staff_to_create_roles = set()
        users_to_create = []
        staff_to_create = []
        staff_instances = []
        staff_departments = []
        staff_subjects_mappings = {}
        staff_levels_mappings = {}
        created_staff = []
        try:
            if current_level.has_departments:
                df = pd.read_excel(data['file'], header=0, sheet_name=0, skiprows=8)
                skipped_rows = 8
            else:
                df = pd.read_excel(data['file'], header=0, sheet_name=0, skiprows=7)
                skipped_rows = 7

            df = df.drop(index=0)
            df = df.dropna(how='all')
        except Exception as e:
            return Response({'message': 'Invalid file! Make sure you upload the excel file you generated'}, status=400)

        all_existing_staff = Staff.objects.filter(school=school)
        if current_level.staff_id:
            existing_staff_ids = [x.staff_id for x in all_existing_staff]

        def show_error_message(label_name: str, column_name: str, row_idx: int):
            return f"The {label_name} cannot be empty! Check the value in the '{column_name}' column in row {row_idx + 2 + skipped_rows}"

        countryinfo = PyCountryInfo()

        def get_data(row):
            first_name = str(row['FIRST NAME'].strip()) if row['FIRST NAME'] else None
            last_name = str(row['LAST NAME (MIDDLE NAME + SURNAME)']).strip() if row['LAST NAME (MIDDLE NAME + SURNAME)'] else None
            title = str(row['TITLE']).strip().replace('.', '').title() if row['TITLE'] else None
            staff_id = str(row['STAFF ID']).strip() if school.staff_id and row.get('STAFF ID') else None
            gender = str(row['GENDER']).strip().lower() if row['GENDER'] else None
            dob = str(row['DATE OF BIRTH']).strip() if row['DATE OF BIRTH'] else None
            subjects = str(row['SUBJECT(S)']).strip() if row['SUBJECT(S)'] else None
            levels = str(row['LEVEL(S)']).strip() if row['LEVEL(S)'] else None
            department = str(row['DEPARTMENT']).strip() if school.has_departments and row.get('DEPARTMENT') else None
            date_enrolled = str(row['DATE EMPLOYED(OPTIONAL)']).strip() if row['DATE EMPLOYED(OPTIONAL)'] else None
            religion = str(row['RELIGION']).strip() if row['RELIGION'] else None
            nationality = str(row['NATIONALITY']).strip() if row['NATIONALITY'] else None
            region = str(row['REGION/STATE']).strip() if row['REGION/STATE'] else None
            pob = str(row['PLACE OF BIRTH']).strip() if row['PLACE OF BIRTH'] else None
            contact = str(row['PHONE NUMBER']).strip()
            alt_contact = str(row['SECOND PHONE NUMBER(OPTIONAL)']).strip() if row['SECOND PHONE NUMBER(OPTIONAL)'] else None
            address = str(row['RESIDENTIAL ADDRESS']).strip() if row['RESIDENTIAL ADDRESS'] else None
            email = str(row['EMAIL(OPTIONAL)']).strip() if row['EMAIL(OPTIONAL)'] else None
            if not first_name:
                error_message = show_error_message('first name', 'FIRST NAME', index)
                raise ErrorMessageException(error_message)
            elif not last_name:
                error_message = show_error_message('last name', 'LAST NAME', index)
                raise ErrorMessageException(error_message)
            elif not gender:
                error_message = show_error_message('gender', 'GENDER', index)
                raise ErrorMessageException(error_message)
            elif gender not in ['male', 'female']:
                error_message = f"'{gender}' is not a valid gender! Check the value in the 'GENDER' column in row {index + 2 + skipped_rows}. Valid values are {['Male', 'Female']}"
                raise ErrorMessageException(error_message)
            elif not dob:
                error_message = show_error_message('date of birth', 'DATE OF BIRTH', index)
                raise ErrorMessageException(error_message)
            elif not title:
                error_message = show_error_message('title', 'TITLE', index)
                raise ErrorMessageException(error_message)
            elif title not in title_options:
                error_message = f"'{title}' is not a valid title! Check the value in the 'TITLE' column in row {index + 2 + skipped_rows}. Valid values are {title_options}"
                raise ErrorMessageException(error_message)
            elif school.staff_id and not staff_id:
                error_message = show_error_message('staff id', 'STAFF ID', index)
                raise ErrorMessageException(error_message)
            elif not role:
                error_message = show_error_message('role', 'ROLE', index)
                raise ErrorMessageException(error_message)
            elif current_level.has_departments and not department:
                error_message = show_error_message('department', 'DEPARTMENT', index)
                raise ErrorMessageException(error_message)
            elif not levels:
                error_message = show_error_message('levels', 'LEVEL(S)', index)
                raise ErrorMessageException(error_message)
            elif not religion:
                error_message = show_error_message('religion', 'RELIGION', index)
                raise ErrorMessageException(error_message)
            elif religion.title() not in religion_options:
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
            elif nationality.lower() == 'ghanaian' and not countryinfo.is_valid_country_province('Ghana', region):
                error_message = f"'{region}' is not a valid region in 'Ghana'! Check the value in the 'REGION/STATE' column in row {index + 2 + skipped_rows}."
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
            elif alt_contact and not valid_phone_number(alt_contact):
                error_message = f"'{alt_contact}' is not a valid phone number! Check the value in the 'SECOND PHONE NUMBER' column in row {index + 2 + skipped_rows}."
                raise ErrorMessageException(error_message)
            elif not address:
                error_message = show_error_message('residential addresss', 'RESIDENTIAL ADDRESS', index)
                raise ErrorMessageException(error_message)

            try:
                dob = datetime.strptime(dob, "%d-%m-%Y").strftime("%Y-%m-%d")
                date_field.clean(dob)
            except Exception:
                error_message = f"'{dob}' is not a valid date! Check the value in the 'DATE OF BIRTH' column in row {index + 2 + skipped_rows}."
                raise ErrorMessageException(error_message)

            if date_enrolled:
                try:
                    date_enrolled = datetime.strptime(date_enrolled, "%d-%m-%Y").strftime("%Y-%m-%d")
                    date_field.clean(date_enrolled)
                except Exception:
                    error_message = f"'{date_enrolled}' is not a valid date! Check the value in the 'DATE EMPLOYED(OPTIONAL)' column in row {index + 2 + skipped_rows}."
                    raise ErrorMessageException(error_message)

            if email:
                try:
                    email_validator(email)
                except Exception:
                    error_message = f"'{email}' is not a valid email address! Check the value in the 'EMAIL(OPTIONAL)' column in row {index + 2 + skipped_rows}."
                    raise ErrorMessageException(error_message)
                
            try:
                level_objs = EducationalLevel.objects.filter(name__in=[x.strip().upper() for x in levels.split(',')]).distinct()
                if len(level_objs) == 0:
                    raise (ValueError)
                else:
                    levels = level_objs
            except Exception as e:
                error_message = f"'{levels}' is/are not a valid level(s)! Check the value in the 'LEVEL(S)' column in row {index + 2 + skipped_rows}."
                raise ErrorMessageException(error_message)
                
            if subjects:
                try:
                    subjects_objs = Subject.objects.filter(level=current_level, name__in=[x.strip().upper() for x in subjects.split(',')]).distinct()
                    if len(subjects_objs) == 0:
                        raise (ValueError)
                    else:
                        subjects = subjects_objs
                except Exception as e:
                    error_message = f"'{subjects}' is/are not a valid subject(s)! Check the value in the 'SUBJECT(S)' column in row {index + 2 + skipped_rows}."
                    raise ErrorMessageException(error_message)

            if current_level.has_departments:
                try:
                    department = Department.objects.get(school=school, level=current_level, name=department.strip().upper())
                except Exception as e:
                    error_message = f"'{department}' is not a valid department! Check the value in the 'DEPARTMENT' column in row {index + 2 + skipped_rows}."
                    raise ErrorMessageException(error_message)

            user_no = random.randint(100, 999)
            username = f"{first_name.replace(' ', '')[0].upper()}{last_name.replace(' ', '').lower()}{user_no}"

            if current_level.staff_id:
                if staff_id in staff_to_create_ids:
                    error_message = f"Two staff cannot have the same staff ID. The staff ID in row {index + 2 + skipped_rows} conflicts with another staff ID on the sheet"
                    raise ErrorMessageException(error_message)
                elif staff_id in existing_staff_ids:
                    error_message = f"Staff with ID '{staff_id}' already exists. Check the staff ID in row {index + 2 + skipped_rows}"
                    raise ErrorMessageException(error_message)
            else:
                staff_id = username

            return {
                'first_name': first_name,
                'last_name': last_name,
                'username': username,
                'staff_id': staff_id,
                'title': title,
                'department': department,
                'levels': levels,
                'gender': gender,
                'subjects': subjects,
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
                    staff_data = get_data(row)
                    user = User(
                        username=staff_data['username'],
                        first_name=staff_data['first_name'].title(),
                        last_name=staff_data['last_name'].title(),
                    )
                    user.set_password(staff_data['username'])
                    users_to_create.append(user)
                    staff_to_create.append((staff_data['username'], staff_data))
                    staff_to_create_ids.add(staff_data['staff_id'])
                    staff_to_create_roles.add(staff_data['role'])

                User.objects.bulk_create(users_to_create)
                created_users = User.objects.filter(username__in=[user.username for user in users_to_create])
                user_mapping = {user.username: user for user in created_users}
                teachers_role = StaffRole.object.get(name='teacher')
                for username, staff_data in staff_to_create:
                    user = user_mapping[username]
                    staff = Staff(
                        user=user,
                        school=school,
                        staff_id=staff_data['staff_id'],
                        title=staff_data['title'],
                        department=staff_data['department'],
                        role=teachers_role,
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
                    staff_subjects_mappings[staff_data['staff_id']] = staff_data['subjects']
                    staff_levels_mappings[staff_data['staff_id']] = staff_data['levels']
                    staff_instances.append(staff)
                    if school.has_departments and staff_data['department']:
                        staff_departments.append(staff_data['department'])

                Staff.objects.bulk_create(staff_instances)
                created_staff = Staff.objects.select_related('department').prefetch_related('subjects', 'levels').filter(school=school, staff_id__in=staff_to_create_ids)
                for _staff in created_staff:
                    staff_subjects = staff_subjects_mappings[_staff.staff_id]
                    staff_levels = staff_levels_mappings[_staff.staff_id]
                    _staff.subjects.set(staff_subjects)
                    _staff.levels.set(staff_levels)
                    if _staff.department and _staff.department in staff_departments:
                        department_index = staff_departments.index(_staff.department)
                        staff_departments[department_index].teachers.add(_staff)

            except ErrorMessageException as e:
                return Response({'message': str(e)}, status=400)
            except Exception as e:
                transaction.set_rollback(True)
                print(e)
                return Response(status=400)

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
                            status=200)
                elif edit_type == 'title':
                    staff = Staff.objects.get(school=school, staff_id=staff_id)
                    staff.title = new_value.title()
                    staff.save()
                    return Response(
                        StaffSerializerOne(Staff.objects.get(school=school, staff_id=staff_id)).data['user'],
                        status=200)
                elif edit_type == 'gender':
                    staff = Staff.objects.select_related('role').get(school=school, staff_id=staff_id)
                    role = staff.role.name
                    if role.lower() in ['headmaster', 'headmistress', 'assistant headmaster', 'assistant headmistress']:
                        if new_value == 'male' and role in ['headmaster', 'headmistress']:
                            role = 'headmaster'
                        elif new_value == 'female' and role in ['headmaster', 'headmistress']:
                            role = 'headmistress'
                        elif new_value == 'male' and role in ['assistant headmaster', 'assistant headmistress']:
                            role = 'assistant headmaster'
                        elif new_value == 'female' and role in ['assistant headmaster', 'assistant headmistress']:
                            role = 'assistant headmistress'

                        # existing_staff = Staff.objects.filter(school=school, role=role).first()
                        # if existing_staff and existing_staff.staff_id != staff_id:
                        #     old_staff_name = f"{existing_staff.title} {existing_staff.user.get_full_name()}"
                        #     new_staff_name = f"{staff.title} {staff.user.get_full_name()}"
                        #     transaction.set_rollback(True)
                        #     return Response({'message': f"{old_staff_name} is currently the {existing_staff.role}. Changing {new_staff_name}'s gender to {new_value} will also update their role to '{role}', which conflicts with {old_staff_name}'s role. Only one staff member can hold the position of {role}."}, status=400)
                    staff.gender = new_value.lower()
                    new_role = StaffRole.objects.get(name=role)
                    staff.role = new_role
                    staff.save()
                    return Response({'gender': new_value, 'role': role}, status=200)
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
                elif edit_type == 'role':
                    staff = Staff.objects.select_related('department').prefetch_related('subjects').get(school=school, staff_id=staff_id)
                    new_role = new_value.lower()
                    staff_gender = staff.gender.lower()
                    previous_role = staff.role
                    staff_department = staff.department.name if staff.department else None
                    staff_subjects = [x.name for x in staff.subjects.all()]
                    if previous_role == 'teacher':
                        old_department = staff.department
                        old_department.teachers.remove(staff)
                        staff.department = None
                        staff_department = None
                        staff_subjects = []
                        staff.subjects.set([])
                    if new_role == 'head' and staff_gender == 'male':
                        new_role = 'headmaster'
                    if new_role == 'head' and staff_gender == 'female':
                        new_role = 'headmistress'
                    if new_role == 'assistant head' and staff_gender == 'male':
                        new_role = 'assistant headmaster'
                    if new_role == 'assistant head' and staff_gender == 'female':
                        new_role = 'assistant headmistress'

                    if new_role == 'teacher':
                        if current_level.has_departments:
                            new_department = Department.objects.prefetch_related('teachers').get(school=school, level=current_level, name=data['department'])
                            new_department.teachers.add(staff)
                            staff.department = new_department
                            staff_department = new_department.name
                        new_subjects = json.loads(data['subjects'])
                        subject_objs = Subject.objects.filter(level=current_level, name__in=new_subjects)
                        staff.subjects.set(subject_objs)
                        staff_subjects = new_subjects

                    staff_role = StaffRole.objects.get(name=new_role)
                    staff.role = staff_role
                    staff.save()
                    
                    return Response({
                        'role': new_role,
                        'department': staff_department,
                        'subjects': staff_subjects,
                    }, status=200)

                elif edit_type == 'subjects':
                    staff = Staff.objects.prefetch_related('subjects').get(school=school, staff_id=staff_id)
                    subjects = json.loads(new_value)
                    subject_objs = Subject.objects.filter(level=current_level, name__in=subjects)
                    staff.subjects.set(subject_objs)
                    staff.save()
                    return Response(subjects, status=200)

                elif edit_type == 'department' and school.has_departments:
                    staff = Staff.objects.get(school=school, staff_id=staff_id)
                    old_department = staff.department
                    old_department.teachers.remove(staff)
                    new_department = Department.objects.get(school=school, level=current_level, name=new_value)
                    staff.department = new_department
                    new_department.teachers.add(staff)
                    staff.save()
                    return Response(new_value, status=200)

                elif edit_type == 'region':
                    staff = Staff.objects.get(school=school, staff_id=staff_id)
                    staff_nationality = staff.nationality
                    countryinfo = PyCountryInfo()
                    staff_country = countryinfo.get_country_from_nationality(staff_nationality)
                    if staff_country.lower() == 'ghana' and not countryinfo.is_valid_country_province('Ghana', new_value):
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
                        return Response({'message': f"'{new_value}' is not a valid phone number"}, status=400)
                    staff = Staff.objects.get(school=school, staff_id=staff_id)
                    staff.contact = new_value
                    staff.save()
                    return Response(new_value, status=200)

                elif edit_type == 'alt_contact':
                    if not valid_phone_number(new_value):
                        return Response({'message': f"'{new_value}' is not a valid phone number"}, status=400)
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
                    return Response(StaffSerializerOne(Staff.objects.get(school=school, staff_id=staff_id)).data['img'],
                                    status=200)
            except:
                transaction.set_rollback(True)
                return Response(status=400)

        return Response(status=400)

    elif data['type'] == 'delete':
        staff_to_delete = Staff.objects.get(school=school, staff_id=data['staffId'])
        user = staff_to_delete.user
        if SubjectAssignment.objects.filter(school=school, level=current_level, teacher=staff_to_delete).exists():
            return Response({'message': "You don't have permission to delete this staff"}, status=400)

        students_classes = Classe.objects.filter(school=school, level=current_level)
        for _class in students_classes:
            if _class.head_teacher == staff_to_delete:
                return Response({'message': "You don't have permission to delete this staff"}, status=400)

        with transaction.atomic():
            try:
                staff_to_delete.delete()
            except Exception as e:
                transaction.set_rollback(True)
                return Response(status=400)

        return Response(status=200)
    
    
    