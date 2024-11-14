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

class EducationalLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationalLevel
        fields = '__all__'
        

class SchoolSerializer(serializers.ModelSerializer):
    level = EducationalLevelSerializer()
    class Meta:
        model = School
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['logo'] = get_image(data, 'school_logo')

        return data


class SpecificSchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ('name')


class GradingSystemSerializer(serializers.ModelSerializer):
    school = SpecificSchoolSerializer()
    class Meta:
        model = GradingSystem
        fields = '__all__'

        
class AcademicYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = '__all__'

        
# Subject Serializers
class SubjectsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        fields = '__all__'


class ProgramSerializer(serializers.ModelSerializer):
    subjects = SubjectsSerializer(many=True)
    
    class Meta:
        model = Program
        fields = '__all__'

class ProgramNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ('name',)
        
        
#  Student Serializers
class StudentSerializer(serializers.ModelSerializer):
    school = SchoolSerializer()
    st_class = serializers.SerializerMethodField()
    program = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['img'] = get_image(data, 'student')

        return data

    def get_st_class(self, obj):
        return obj.st_class.name
    
    def get_program(self, obj):
        if obj.program:
            return obj.program.name
        return None


class SpecificStudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    level = EducationalLevelSerializer()
    program = ProgramNameSerializer()

    class Meta:
        model = Student
        fields = ('user', 'img', 'st_id', 'gender', 'has_completed', 'current_year', 'program', 'dob', 'level', 'date_created')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if settings.DEBUG:
            if data['img'] and data['img'] != 'null':
                data['img'] = f"http://localhost:8000{data['img']}"
            else:
                data['img'] = f"http://localhost:8000/static/images/students_img.jpg"
        else:
            if data['img'] and data['img'] != 'null':
                pass
            else:
                data['img'] = f"https://{production_domain}/static/images/students_img.jpg"

        return data


class SpecificStudentWithoutImageSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    level = EducationalLevelSerializer()
    program = ProgramNameSerializer()

    class Meta:
        model = Student
        fields = ('user', 'st_id', 'gender', 'has_completed', 'current_year', 'program', 'level', 'date_created')

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


class StudentNameAndIdSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Student
        fields = ('user', 'st_id')    


# Staff Serializers
class StaffSerializer(serializers.ModelSerializer):
    school = SchoolSerializer()
    subjects = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()

    class Meta:
        model = Staff
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['img'] = get_image(data, 'staff')

        return data

    def get_department(self, obj):
        if obj.department:
            return obj.department.name
        return None
    
    def get_subjects(self, obj):
        return [_subject.name for _subject in obj.subjects.all()]
    

class SpecificStaffSerializer(serializers.ModelSerializer):
    school = SchoolSerializer
    user = UserSerializer()
    subjects = SubjectsSerializer(many=True)
    department = 'DepartmentNameSerializer'

    class Meta:
        model = Staff
        fields = ('staff_id', 'contact', 'img', 'gender', 'user', 'subjects', 'department', 'role', 'dob', 'date_created')

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
    department = serializers.SerializerMethodField()

    class Meta:
        model = Staff
        fields = ('staff_id', 'contact', 'alt_contact', 'img', 'gender', 'user', 'subjects', 'department', 'role', 'dob', 'nationality', 'pob', 'region', 'religion', 'email', 'address', 'date_enrolled')

    def get_user(self, obj):
        return f"{obj.title} {obj.user.get_full_name()}"
    
    def get_department(self, obj):
        if obj.department:
            return obj.department.name
        return None
    
    def get_subjects(self, obj):
        return [_subject.name for _subject in obj.subjects.all()]
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['img'] = get_image(data, 'staff')
       
        return data


class StaffSerializerTwo(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    subjects = serializers.SerializerMethodField()

    class Meta:
        model = Staff
        fields = ('staff_id', 'contact', 'img', 'gender', 'user', 'subjects', 'role', 'email', 'alt_contact')

    def get_subjects(self, obj):
        return [_subject.name for _subject in obj.subjects.all()]
        
    def get_user(self, obj):
        return f"{obj.title} {obj.user.get_full_name()}"
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['img'] = get_image(data, 'staff')
       
        return data
    
    
class StaffSerializerThree(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Staff
        fields = ('staff_id', 'img', 'user')

    def get_user(self, obj):
        return f"{obj.title} {obj.user.get_full_name()}"
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['img'] = get_image(data, 'staff')
       
        return data
    
    
class SpecificStaffWithoutImageSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    subjects = SubjectsSerializer(many=True)
    department = 'DepartmentNameSerializer'

    class Meta:
        model = Staff
        fields = ('staff_id', 'contact', 'gender', 'user', 'subjects', 'department', 'role', 'date_created')
        

# Department Serializers
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
    subjects = SubjectsSerializer(many=True)

    class Meta:
        model = Department
        fields = ('name', 'subjects')
        
        
class DepartmentNameSubjectsTeachersDataSerializer(serializers.ModelSerializer):
    subjects = SubjectsSerializer(many=True)
    teachers = StaffSerializerTwo(many=True)

    class Meta:
        model = Department
        fields = ('subjects', 'teachers', 'name')
    
    
# Head Serializers
class HeadSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    school = SchoolSerializer()

    class Meta:
        model = Head
        fields = "__all__"

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


class SpecificHeadSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    level = EducationalLevelSerializer()

    class Meta:
        model = Head
        fields = ('head_id', 'contact', 'img', 'gender', 'user', 'role', 'dob', 'level', 'date_created')

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


# Classe Serializers
class ClasseSerializer(serializers.ModelSerializer):
    students = SpecificStudentSerializer(many=True)
    program = ProgramNameSerializer()
    head_teacher = SpecificStaffWithoutImageSerializer()
    academic_years = AcademicYearSerializer(many=True)
    students_level = EducationalLevelSerializer()

    class Meta:
        model = Classe
        fields = "__all__"


class ClasseWithSubjectsSerializer(serializers.ModelSerializer):
    students = SpecificStudentSerializer(many=True)
    subjects = SubjectsSerializer(many=True)
    program = ProgramNameSerializer()
    head_teacher = SpecificStaffSerializer()
    academic_years = AcademicYearSerializer(many=True)

    class Meta:
        model = Classe
        fields = "__all__"

class ClassesSerializerOne(serializers.ModelSerializer):
    students = StudentSerializerOne(many=True)
    subjects = serializers.SerializerMethodField()
    program = serializers.SerializerMethodField()
    head_teacher = StaffSerializerThree()

    class Meta:
        model = Classe
        fields = ('name', 'students', 'students_year', 'head_teacher', 'program', 'subjects')
   
    def get_subjects(self, obj):
        return [_subject.name for _subject in obj.subjects.all()]
    
    def get_program(self, obj):
        return obj.program.name

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
        
        
class ClasseWithoutStudentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Classe
        fields = ('name', 'students_year')


# Subject Assignment Serializers
class SubjectAssignmentSerializer(serializers.ModelSerializer):
    students_class = ClasseSerializer()
    subjects = SubjectsSerializer(many=True)
    assigned_by = SpecificStaffWithoutImageSerializer()
    teacher = SpecificStaffSerializer()

    class Meta:
        model = SubjectAssignment
        fields = ('students_class', 'subjects', 'teacher', 'academic_term', 'date_created', 'assigned_by')


class SubjectAssignmentWithoutStudentsSerializer(serializers.ModelSerializer):
    students_class = ClasseWithoutStudentsSerializer()
    subjects = SubjectsSerializer(many=True)
    assigned_by = SpecificStaffWithoutImageSerializer()
    teacher = SpecificStaffSerializer()

    class Meta:
        model = SubjectAssignment
        fields = ('students_class', 'subjects', 'teacher', 'academic_term', 'date_created', 'assigned_by')
    
    
class TeacherSubjectAssignmentSerializer(serializers.ModelSerializer):
    students_class = serializers.SerializerMethodField()
    subjects = serializers.SerializerMethodField()

    class Meta:
        model = SubjectAssignment
        fields = ('students_class', 'subjects')

    def get_subjects(self, obj):
        return [subject.name for subject in obj.subjects.all()]
    
    def get_students_class(self, obj):
        st_class = {
            'name': obj.students_class.name,
        }
        class_students = []
        students = obj.students_class.students.all()
        for _student in students:
            student_data = {
                'name': _student.user.get_full_name(),
                'st_id': _student.st_id,
                'gender': _student.gender,
                'img': _student.img,
            }
            student_data['img'] = get_image(student_data, 'student')
            class_students.append(student_data)
        st_class['students'] = class_students
        
        return st_class
    
# Exams Serializers
class ExamsSerializer(serializers.ModelSerializer):
    student = SpecificStudentWithoutImageSerializer()
    subject = SubjectsSerializer()
    academic_year = AcademicYearSerializer()
    teacher = SpecificStaffWithoutImageSerializer()

    class Meta:
        model = Exam
        fields = "__all__"
        
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


# Assessment Serializers
class AssessmentSerializer(serializers.ModelSerializer):
    student = SpecificStudentWithoutImageSerializer()
    subject = SubjectsSerializer()
    academic_year = AcademicYearSerializer()
    teacher = SpecificStaffWithoutImageSerializer()

    class Meta:
        model = Assessment
        fields = "__all__"
        
class AssessmentSerializerWithoutStudentTeacher(serializers.ModelSerializer):
    subject = SubjectsSerializer()

    class Meta:
        model = Assessment
        fields = ('subject', 'academic_term', 'score', 'assessment_date', 'percentage', 'title', 'total_score', 'description', 'comment')


# Teacher 
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


# HOD
class HodSubjectAssignmentSerializer(serializers.ModelSerializer):
    subjects = serializers.SerializerMethodField()
    teacher = serializers.SerializerMethodField()
    students_class = serializers.SerializerMethodField()

    class Meta:
        model = SubjectAssignment
        fields = ('subjects', 'teacher', 'students_class')
        
    def get_subjects(self, obj):
        return [subject.name for subject in obj.subjects.all()]
    
    def get_teacher(self, obj):
        return {
            'name': f"{obj.teacher.user.first_name} {obj.teacher.user.last_name}",
            'staff_id': obj.teacher.staff_id,
        }
    
    def get_students_class(self, obj):
        return obj.students_class.name


# Students Attendance
class StudentAttendanceStudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Student
        fields = ('user', 'st_id')

class StudentsAttendanceSerializer(serializers.ModelSerializer):
    students_class = ClasseWithoutStudentsSerializer()
    students_present = StudentAttendanceStudentSerializer(many=True)
    students_absent = StudentAttendanceStudentSerializer(many=True)

    class Meta:
        model = StudentAttendance
        fields = ('date', 'students_class', 'students_present', 'students_absent')

# Student Notification Serializer
class StudentNotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Student
        fields = ('st_id', 'img', 'user')

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
                data['img'] = f"https://cassandra-o5ft.onrender.com/static/images/staff_img.jpg"

        return data
    
    
# Staff Notification Serializer
class StaffNotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Staff
        fields = ('staff_id', 'img', 'user', 'role')

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
                data['img'] = f"https://cassandra-o5ft.onrender.com/static/images/staff_img.jpg"

        return data


# Head Notification Serializer
class HeadNotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Head
        fields = ('head_id', 'img', 'user', 'role')

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
                data['img'] = f"https://cassandra-o5ft.onrender.com/static/images/staff_img.jpg"

        return data


class NotificationSerializer(serializers.ModelSerializer):
    from_head = HeadNotificationSerializer()
    from_staff = StaffNotificationSerializer()
    from_student = StudentNotificationSerializer()
    to_staff = StaffNotificationSerializer(many=True)
    to_student = StudentNotificationSerializer(many=True)

    class Meta:
        model = Notification
        fields = "__all__"
        
        
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
class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = '__all__'
        
class KnustProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnustProgram
        fields = '__all__'
        
class UGProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = UGProgram
        fields = '__all__'
        
class UCCProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = UCCProgram
        fields = '__all__'
        
        
        
