from rest_framework import serializers
from api.models import *
from django.contrib.auth.models import User
import os
from django.conf import settings
from pathlib import Path
from Backend.production import ALLOWED_HOSTS

BASE_DIR = Path(__file__).resolve().parent.parent
production_domain = ALLOWED_HOSTS[0]

def get_image(data, type):
    property_reference = 'img'
    if type == 'student':
        default_img = 'students_img.jpg'
    elif type == 'staff':
        default_img = 'staff_img.jpg'
    elif type == 'school_logo':
        default_img = 'school-logo.png'
        property_reference = 'logo'
    elif type == 'signature':
        default_img = 'signature.png'
    
    img = None
    if settings.DEBUG:
        if data[property_reference] and data[property_reference] != 'null':
            img = f"http://localhost:8000{data[property_reference]}"
        else:
            img = f"http://localhost:8000/static/images/{default_img}"
    else:
        if data[property_reference] and data[property_reference] != 'null':
            img = data[property_reference]
        else:
            img = f"https://{production_domain}/static/images/{default_img}"
    
    return img
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'last_login', 'email']


# School Serializers
class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['logo'] = get_image(data, 'school_logo')

        return data
        

# Educational Level Serializers
class SuperuserEducationalLevelSerializer(serializers.ModelSerializer):
    schools = serializers.SerializerMethodField()
    class Meta:
        model = EducationalLevel
        fields = '__all__'
        
    def get_schools(self, obj):
        return [x.identifier for x in obj.schools.all()]
    
     
class EducationalLevelSerializer(serializers.ModelSerializer):
    schools = serializers.SerializerMethodField()
    class Meta:
        model = EducationalLevel
        fields = '__all__'
        
    def get_schools(self, obj):
        return [x.name for x in obj.schools.all()]


class EducationalLevelWithoutSchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationalLevel
        fields = ('name', 'identifier', 'has_programs', 'has_departments', 'students_id', 'students_index_no', 'years_to_complete')
        
        
class EducationalLevelNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationalLevel
        fields = ('name',)
        
        
# Grading System Range Serializers
class SuperuserGradingSystemRangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradingSystemRange
        fields = '__all__'
        
        
# Grading System Serializers
class SuperuserGradingSystemSerializer(serializers.ModelSerializer):
    level = serializers.SerializerMethodField()
    schools = serializers.SerializerMethodField()
    ranges = serializers.SerializerMethodField()
    class Meta:
        model = GradingSystem
        fields = '__all__'
        
    def get_level(self, obj):
        return obj.level.identifier if obj.level else None
    
    def get_schools(self, obj):
        return [x.identifier for x in obj.schools.all()]
    
    def get_ranges(self, obj):
        return [x.identifier for x in obj.ranges.all()]
    

class GradingSystemSerializer(serializers.ModelSerializer):
    level = EducationalLevelSerializer()
    class Meta:
        model = GradingSystem
        fields = '__all__'
        
        
# Academic year serializers
class AcademicYearSerializer(serializers.ModelSerializer):
    level = serializers.SerializerMethodField()
    
    class Meta:
        model = AcademicYear
        fields = ["name", 'id', "start_date", "end_date", 'level', "term_1_end_date", "term_2_start_date", "term_2_end_date", "term_3_start_date", "term_3_end_date", "period_division", "no_divisions", "students_graduation_date"]
        
    def get_level(self, obj):
        return obj.level.identifier if obj.level else None


# Subject Serializers
class SuperuserSubjectsSerializer(serializers.ModelSerializer):
    level = serializers.SerializerMethodField()
    schools = serializers.SerializerMethodField()
    
    class Meta:
        model = Subject
        fields = '__all__'
        
    def get_level(self, obj):
        return obj.level.identifier if obj.level else None
    
    def get_schools(self, obj):
        return [x.identifier for x in obj.schools.all()]
    

class SubjectIdentiferSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Subject
        fields = ('identifier',)
    
    
class SubjectsSerializer(serializers.ModelSerializer):
    level = serializers.SerializerMethodField()
    schools = serializers.SerializerMethodField()
    
    class Meta:
        model = Subject
        fields = '__all__'
        
    def get_level(self, obj):
        return obj.level.name if obj.level else None
    
    def get_school(self, obj):
        return [x.name for x in obj.school.all()]


# Program Serializer
class SuperuserProgramSerializer(serializers.ModelSerializer):
    subjects = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()
    schools = serializers.SerializerMethodField()
    
    class Meta:
        model = Program
        fields = '__all__'
        
    def get_subjects(self, obj):
        return [x.identifier for x in obj.subjects.all()]
    
    def get_schools(self, obj):
        return [x.identifier for x in obj.schools.all()]
    
    def get_level(self, obj):
        return obj.level.identifier if obj.level else None
    
    
class ProgramSerializer(serializers.ModelSerializer):
    subjects = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()
    schools = serializers.SerializerMethodField()
    
    class Meta:
        model = Program
        fields = '__all__'
        
    def get_subjects(self, obj):
        return [x.name for x in obj.subjects.all()]
    
    def get_school(self, obj):
        return [x.name for x in obj.school.all()]
    
    def get_level(self, obj):
        return obj.level.name if obj.level else None


class ProgramNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ('name',)
        
        
#  Student Serializers
class StudentSerializer(serializers.ModelSerializer):
    school = SchoolSerializer()
    current_level = EducationalLevelWithoutSchoolSerializer()
    current_program = serializers.SerializerMethodField()
    st_class = serializers.SerializerMethodField()
    levels = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['img'] = get_image(data, 'student')

        return data

    def get_st_class(self, obj):
        if obj.st_class:
            return obj.st_class.name
        return None
    
    def get_current_level(self, obj):
        return obj.current_level.identifier if obj.current_level else None
    
    def get_levels(self, obj):
        return [x.identifier for x in obj.levels.all()] 
    
    def get_current_program(self, obj):
        return obj.current_program.identifier if obj.current_program else None


# class SpecificStudentSerializer(serializers.ModelSerializer):
#     user = UserSerializer()
#     program = ProgramNameSerializer()

#     class Meta:
#         model = Student
#         fields = ('user', 'img', 'st_id', 'gender', 'has_completed', 'current_year', 'program', 'dob', 'date_created')

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     if settings.DEBUG:
    #         if data['img'] and data['img'] != 'null':
    #             data['img'] = f"http://localhost:8000{data['img']}"
    #         else:
    #             data['img'] = f"http://localhost:8000/static/images/students_img.jpg"
    #     else:
    #         if data['img'] and data['img'] != 'null':
    #             pass
    #         else:
    #             data['img'] = f"https://{production_domain}/static/images/students_img.jpg"

    #     return data


# class SpecificStudentWithoutImageSerializer(serializers.ModelSerializer):
#     user = UserSerializer()
#     program = ProgramNameSerializer()

#     class Meta:
#         model = Student
#         fields = ('user', 'st_id', 'gender', 'current_year', 'program', 'date_created')

class StudentSerializerOne(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = (
            'user', 'st_id', 'gender', 'date_enrolled', 'address', 'contact', 'pob', 'religion', 'region', 'index_no', 'img', 'dob', 'gender', 'nationality', 'guardian', 
            'guardian_gender', 'guardian_nationality', 'guardian_contact', 'guardian_email', 'guardian_address', 'guardian_occupation', 'email'
        )
        
    def get_user(self, obj):
        return obj.user.get_full_name()
    
    def to_representation(self, instance):  
        data = super().to_representation(instance)
        data['img'] = get_image(data, 'student')
        
        return data


class StudentSerializerTwo(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ('user', 'st_id', 'gender', 'contact', 'guardian_contact', 'img')    

    def get_user(self, obj):
        return obj.user.get_full_name()
    
    def to_representation(self, instance):  
        data = super().to_representation(instance)
        data['img'] = get_image(data, 'student')
        
        return data


class StudentSerializerThree(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ('user', 'st_id')
    
    def get_user(self, obj):
        return obj.user.get_full_name()
    
  
class StudentSerializerFour(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ('user', 'gender', 'contact', 'img')    

    def get_user(self, obj):
        return obj.user.get_full_name()
    
    def to_representation(self, instance):  
        data = super().to_representation(instance)
        data['img'] = get_image(data, 'student')
        
        return data


class StudentUserIdSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ('user', 'st_id')
    
    def get_user(self, obj):
        return obj.user.get_full_name()
    

# Staff Role Serializers
class StaffRoleSerializer(serializers.ModelSerializer):
    level = serializers.SerializerMethodField()
    schools = serializers.SerializerMethodField()
    
    class Meta:
        model = StaffRole
        fields = "__all__"
        
    def get_schools(self, obj):
        return [x.identifier for x in obj.schools.all()]
    
    def get_level(self, obj):
        return obj.level.identifier if obj.level else None


class StaffRoleSerializerOne(serializers.ModelSerializer):
    level = EducationalLevelWithoutSchoolSerializer()
    
    class Meta:
        model = StaffRole
        fields = ('name', 'level', 'identifier')
    
    
# Staff Serializers 
class StaffSerializer(serializers.ModelSerializer):
    school = SchoolSerializer()
    subjects = serializers.SerializerMethodField()
    departments = serializers.SerializerMethodField()
    roles = serializers.SerializerMethodField()
    current_role = StaffRoleSerializerOne()

    class Meta:
        model = Staff
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['img'] = get_image(data, 'staff')

        return data

    def get_roles(self, obj):
        return [x.identifier for x in obj.roles.all()]
    
    def get_departments(self, obj):
        return [x.identifier for x in obj.departments.all()]
    
    def get_subjects(self, obj):
        return [_subject.identifier for _subject in obj.subjects.all()]
    

class SpecificStaffSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    subjects = SubjectsSerializer(many=True)
    roles = serializers.SerializerMethodField()

    class Meta:
        model = Staff
        fields = ('staff_id', 'contact', 'img', 'gender', 'user', 'subjects', 'department', 'roles', 'dob', 'date_created')

    def get_roles(self, obj):
        return [x.name for x in obj.roles.all()]
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if settings.DEBUG:
            if data['img'] and data['img'] != 'null':
                data['img'] = f"http://localhost:8000{data['img']}"
            else:
                data['img'] = f"http://localhost:8000/static/images/staff_img.jpg"
        else:
            if data['img'] and data['img'] != 'null':
                pass
            else:
                data['img'] = f"https://{production_domain}/static/images/staff_img.jpg"

        return data


class StaffSerializerOne(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    subjects = serializers.SerializerMethodField()
    departments = serializers.SerializerMethodField()
    roles = serializers.SerializerMethodField()
    current_role = serializers.SerializerMethodField()

    class Meta:
        model = Staff
        fields = ('staff_id', 'contact', 'alt_contact', 'img', 'current_role', 'gender', 'user', 'subjects', 'departments', 'roles', 'dob', 'nationality', 'pob', 'region', 'religion', 'email', 'address', 'date_enrolled', 'is_active')

    def get_user(self, obj):
        return f"{obj.title}. {obj.user.get_full_name()}"
    
    def get_roles(self, obj):
        return [x.identifier for x in obj.roles.all()]
    
    def get_departments(self, obj):
        return [x.identifier for x in obj.departments.all()]
    
    def get_subjects(self, obj):
        return [_subject.identifier for _subject in obj.subjects.all()]
    
    def get_current_role(self, obj):
        return obj.current_role.identifier if obj.current_role else None
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['img'] = get_image(data, 'staff')
       
        return data


class StaffSerializerTwo(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    subjects = serializers.SerializerMethodField()
    departments = serializers.SerializerMethodField()
    roles = serializers.SerializerMethodField()

    class Meta:
        model = Staff
        fields = ('staff_id', 'contact', 'img', 'gender', 'is_active', 'nationality', 'user', 'subjects', 'roles', 'departments', 'email', 'alt_contact', 'address')

    def get_subjects(self, obj):
        return [_subject.identifier for _subject in obj.subjects.all()]
    
    def get_roles(self, obj):
        return [x.identifier for x in obj.roles.all()]
        
    def get_user(self, obj):
        return f"{obj.title}. {obj.user.get_full_name()}"
    
    def get_departments(self, obj):
        return [x.identifier for x in obj.departments.all()]
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['img'] = get_image(data, 'staff')
       
        return data
    
    
class StaffUserIdImgSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Staff
        fields = ('staff_id', 'img', 'user')

    def get_user(self, obj):
        return f"{obj.title}. {obj.user.get_full_name()}"
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['img'] = get_image(data, 'staff')
       
        return data


class StaffSerializerFour(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Staff
        fields = ('img', 'user', 'contact', 'gender', 'email')

    def get_user(self, obj):
        return f"{obj.title}. {obj.user.get_full_name()}"
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['img'] = get_image(data, 'staff')
       
        return data
    

class StaffUserIdSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Staff
        fields = ('staff_id', 'user')

    def get_user(self, obj):
        return f"{obj.title}. {obj.user.get_full_name()}"
    
    
class SpecificStaffWithoutImageSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    subjects = SubjectsSerializer(many=True)
    departments = 'DepartmentNameSerializer'
    roles = serializers.SerializerMethodField()

    class Meta:
        model = Staff
        fields = ('staff_id', 'contact', 'gender', 'user', 'subjects', 'departments', 'roles', 'date_created')
        
    def get_role(self, obj):
        return obj.role.name
    
    
# Department Serializers
class SuperuserDepartmentSerializer(serializers.ModelSerializer):
    subjects = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()
    hod = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = "__all__"
    
    def get_subjects(self, obj):
        return [subject.identifier for subject in obj.subjects.all()]
    
    def get_level(self, obj):
        return obj.level.identifier if obj.level else None
    
    def get_hod(self, obj):
      return f"{obj.hod.title}. {obj.hod.user.get_full_name()}" if obj.hod else None 
        
        
class DepartmentSerializer(serializers.ModelSerializer):
    teachers = SpecificStaffSerializer(many=True)
    hod = SpecificStaffSerializer()
    subjects = SubjectsSerializer(many=True)

    class Meta:
        model = Department
        fields = "__all__"


class DepartmentNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('name',)
        
        
class DepartmentNameSubjectsSerializer(serializers.ModelSerializer):
    subjects = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = ('name', 'subjects', )
    
    def get_subjects(self, obj):
        return [subject.name for subject in obj.subjects.all()]
    

class DepartmentSerializerOne(serializers.ModelSerializer):
    subjects = serializers.SerializerMethodField()
    teachers = StaffUserIdSerializer(many=True)
    hod = StaffUserIdSerializer()
    
    class Meta:
        model = Department
        fields = ('name', 'subjects', 'teachers', 'id', 'hod')
    
    def get_subjects(self, obj):
        return [subject.name for subject in obj.subjects.all()]
    
class DepartmentNameHODSubjectsSerializer(serializers.ModelSerializer):
    subjects = serializers.SerializerMethodField()
    hod = StaffUserIdSerializer()
    teachers = StaffUserIdSerializer(many=True)
    class Meta:
        model = Department
        fields = ('name', 'subjects', 'hod', 'identifier', 'id', 'teachers')
    
    def get_subjects(self, obj):
        return [subject.identifier for subject in obj.subjects.all()]
       
       
class DepartmentNameSubjectsTeachersDataSerializer(serializers.ModelSerializer):
    subjects = serializers.SerializerMethodField()
    teachers = StaffSerializerTwo(many=True)

    class Meta:
        model = Department
        fields = ('subjects', 'teachers', 'name')
    
    def get_subjects(self, obj):
        return [subject.name for subject in obj.subjects.all()]


# Classe Serializers
class SuperuserClasseSerializer(serializers.ModelSerializer):
    program = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()
    head_teacher = StaffUserIdSerializer()
    subjects = serializers.SerializerMethodField()
    school = serializers.SerializerMethodField()
    linked_class = serializers.SerializerMethodField()

    class Meta:
        model = Classe
        fields = ('name', 'id', 'level', 'students_year', 'head_teacher', 'program', 'identifier', 'school', 'subjects', 'linked_class')
    
    def get_program(self, obj):
        return obj.program.identifier if obj.program else None
    
    def get_subjects(self, obj):
        return [subject.identifier for subject in obj.subjects.all()]
    
    def get_school(self, obj):
        return obj.school.identifier if obj.school else None
    
    def get_level(self, obj):
        return obj.level.identifier if obj.level else None
    
    def get_linked_class(self, obj):
        return obj.linked_class.identifier if obj.linked_class else None
        
        
class ClasseSerializer(serializers.ModelSerializer):
    students = StudentSerializerTwo(many=True)
    program = ProgramNameSerializer()
    head_teacher = SpecificStaffWithoutImageSerializer()

    class Meta:
        model = Classe
        fields = "__all__"
        
        
class ClasseWithSubjectsSerializer(serializers.ModelSerializer):
    students = StudentSerializerTwo(many=True)
    subjects = SubjectsSerializer(many=True)
    program = ProgramNameSerializer()
    head_teacher = SpecificStaffSerializer()

    class Meta:
        model = Classe
        fields = "__all__"

class ClassesSerializerOne(serializers.ModelSerializer):
    students = StudentSerializerOne(many=True)
    subjects = serializers.SerializerMethodField()
    program = serializers.SerializerMethodField()
    head_teacher = StaffUserIdImgSerializer()

    class Meta:
        model = Classe
        fields = ('name', 'students', 'students_year', 'head_teacher', 'program', 'subjects')
   
    def get_subjects(self, obj):
        return [_subject.name for _subject in obj.subjects.all()]
    
    def get_program(self, obj):
        return obj.program.name


class ClassesSerializerTwo(serializers.ModelSerializer):
    students = StudentSerializerTwo(many=True)

    class Meta:
        model = Classe
        fields = ('name', 'students')
    
    
class ClasseWithoutStudentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Classe
        fields = ('name', 'students_year')


# Linked class serializers
class AdminLinkedClassSerializer(serializers.ModelSerializer):
    from_class = serializers.SerializerMethodField()
    to_class = serializers.SerializerMethodField()

    class Meta:
        model = LinkedClasse
        fields = ('to_class', 'from_class')
    
    def get_from_class(self, obj):  
        return obj.from_class.name
    
    def get_to_class(self, obj):
        return obj.to_class.name
    
    
# Subject Assignment Serializers
class SubjectAssignmentSerializer(serializers.ModelSerializer):
    students_class = ClasseSerializer()
    subjects = SubjectsSerializer(many=True)
    assigned_by = SpecificStaffWithoutImageSerializer()
    teacher = SpecificStaffSerializer()

    class Meta:
        model = SubjectAssignment
        fields = ('students_class', 'subjects', 'teacher', 'academic_term', 'date_created', 'assigned_by')


class SubjectAssignmentSerializerOne(serializers.ModelSerializer):
    students_class = serializers.SerializerMethodField()
    subjects = serializers.SerializerMethodField()
    teacher = StaffUserIdSerializer()

    class Meta:
        model = SubjectAssignment
        fields = ('students_class', 'subjects', 'teacher', 'id')
        
    def get_students_class(self, obj):
        return obj.students_class.name
    
    def get_subjects(self, obj):
        return [subject.name for subject in obj.subjects.all()]
     
    
class SubjectAssignmentWithoutStudentsSerializer(serializers.ModelSerializer):
    students_class = ClasseWithoutStudentsSerializer()
    subjects = SubjectsSerializer(many=True)
    assigned_by = SpecificStaffWithoutImageSerializer()
    teacher = SpecificStaffSerializer()

    class Meta:
        model = SubjectAssignment
        fields = ('students_class', 'subjects', 'teacher', 'academic_term', 'date_created', 'assigned_by')

 
class SubjectAssignmentSerializerTwo(serializers.ModelSerializer):
    students_class = ClassesSerializerTwo()
    subjects = serializers.SerializerMethodField()

    class Meta:
        model = SubjectAssignment
        fields = ('students_class', 'subjects')

    def get_subjects(self, obj):
        return [subject.name for subject in obj.subjects.all()]


class SubjectAssignmentSerializerThree(serializers.ModelSerializer):
    subjects = serializers.SerializerMethodField()
    teacher = StaffUserIdImgSerializer()

    class Meta:
        model = SubjectAssignment
        fields = ('subjects', 'teacher')
    
    def get_subjects(self, obj):
        return [subject.name for subject in obj.subjects.all()]
    
    
# Exams Serializers
class ExamsSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField()
    subject = SubjectsSerializer()
    academic_year = AcademicYearSerializer()
    teacher = SpecificStaffWithoutImageSerializer()

    class Meta:
        model = Exam
        fields = "__all__"
    
    def get_student(self, obj):
        return {
            'name': obj.student.user.get_full_name(),
            'st_id': obj.student.st_id,
        }
        
        
class ExamsSerializerWithoutStudentTeacher(serializers.ModelSerializer):
    subject = SubjectsSerializer()

    class Meta:
        model = Exam
        fields = ('subject', 'academic_term', 'score', 'date_created')


class StudentExamsSerializer(serializers.ModelSerializer):
    subject = SubjectsSerializer()

    class Meta:
        model = Exam
        fields = ('subject', 'score', 'date_created')

    
class ExamSerializerOne(serializers.ModelSerializer):
    subject = SubjectsSerializer()

    class Meta:
        model = Exam
        fields = ('subject', 'score', 'total_score')
        

# Assessment Serializers
class AssessmentSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField()
    subject = SubjectsSerializer()
    academic_year = AcademicYearSerializer()
    teacher = SpecificStaffWithoutImageSerializer()

    class Meta:
        model = Assessment
        fields = "__all__"
    
    def get_student(self, obj):
        return {
            'name': obj.student.user.get_full_name(),
            'st_id': obj.student.st_id,
        }
        
        
class AssessmentSerializerWithoutStudentTeacher(serializers.ModelSerializer):
    subject = SubjectsSerializer()

    class Meta:
        model = Assessment
        fields = ('subject', 'academic_term', 'score', 'assessment_date', 'percentage', 'title', 'total_score', 'description', 'comment')


class AssessmentSerializerOne(serializers.ModelSerializer):
    subject = serializers.SerializerMethodField()

    class Meta:
        model = Assessment
        fields = ('subject', 'score', 'assessment_date', 'title', 'total_score', 'description', 'comment')
    
    def get_subject(self, obj):
        return obj.subject.name
        
        
# Result Serializer 
class TeacherGetStudentResultSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField()

    class Meta:
        model = StudentResult
        fields = ('result', 'total_assessment_score', 'exam_score', 'student', 'remark', 'grade')
    
    def get_student(self, obj):
        return {
            'name': f"{obj.student.user.first_name} {obj.student.user.last_name}",
            'st_id': obj.student.st_id,
        }


class ResultSerializerOne(serializers.ModelSerializer):
    subject = serializers.SerializerMethodField()
    
    class Meta:
        model = StudentResult
        fields = ('result', 'subject', 'total_assessment_score', 'exam_score', 'total_assessment_percentage', 'exam_percentage', 'remark', 'grade', 'position')
    
    def get_subject(self, obj):
        return obj.subject.name
 

# Students Attendance
class StudentsAttendanceSerializer(serializers.ModelSerializer):
    students_present = StudentUserIdSerializer(many=True)
    students_absent = StudentUserIdSerializer(many=True)

    class Meta:
        model = StudentAttendance
        fields = ('date', 'students_present', 'students_absent')

    # def get_students_class(self, obj):
    #     return obj.students_class.name


# ReleasedResult
class ReleasedResultsSerializer(serializers.ModelSerializer):
    students_class = serializers.SerializerMethodField()
    academic_year = serializers.SerializerMethodField()
    released_by = serializers.SerializerMethodField()
    
    class Meta:
        model = ReleasedResult
        fields = ('students_class', 'date', 'academic_year', 'academic_term', 'released_by', 'id')

    def get_students_class(self, obj):
        return obj.students_class.name

    def get_academic_year(self, obj):
        return obj.academic_year.name
    
    def get_released_by(self, obj):
        return f'{obj.released_by.title}. {obj.released_by.user.get_full_name()}'

# class NotificationSerializer(serializers.ModelSerializer):
#     from_head = HeadNotificationSerializer()
#     from_staff = StaffNotificationSerializer()
#     from_student = StudentNotificationSerializer()
#     to_staff = StaffNotificationSerializer(many=True)
#     to_student = StudentNotificationSerializer(many=True)

#     class Meta:
#         model = Notification
#         fields = "__all__"
        
        
class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Extract the filename from the file path
        one_level_up_path = os.path.dirname(data['path'])
        filename = os.path.basename(data['path'])
        data['path'] = f"/static/{os.path.join(os.path.basename(one_level_up_path), filename)}"
        return data


# Universities serializer
# class UniversitySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = University
#         fields = '__all__'
        
# class KnustProgramSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = KnustProgram
#         fields = '__all__'
        
# class UGProgramSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UGProgram
#         fields = '__all__'
        
# class UCCProgramSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UCCProgram
#         fields = '__all__'
        
        
        
