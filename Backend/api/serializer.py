from rest_framework import serializers
from api.models import *
from django.contrib.auth.models import User
import os
from django.conf import settings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'last_login', 'email']


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if settings.DEBUG:
            data['sch_logo'] = f"http://localhost:8000{data['sch_logo']}"

        return data


class SpecificSchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ('name', 'date_created')


class GradingSystemSerializer(serializers.ModelSerializer):
    school = SpecificSchoolSerializer()
    class Meta:
        model = GradingSystem
        fields = '__all__'


class EducationalLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationalLevel
        fields = '__all__'


class AcademicYearDivisionSerializer(serializers.ModelSerializer):

    class Meta:
        model = AcademicYearDivision
        fields = '__all__'
        
        
class AcademicYearSerializer(serializers.ModelSerializer):
    period_division = AcademicYearDivisionSerializer()
    
    class Meta:
        model = AcademicYear
        fields = '__all__'

        
# Course Serializers
class SubjectsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        fields = '__all__'


class ProgramSerializer(serializers.ModelSerializer):
    subjects = SubjectsSerializer(many=True)

    class Meta:
        model = Program
        fields = '__all__'


class SpecificProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ('name', 'date_created')


#  Student Serializers
class StudentSerializer(serializers.ModelSerializer):
    school = SchoolSerializer()
    user = UserSerializer()
    level = EducationalLevelSerializer()
    st_class = 'ClassSerializer'
    program = SpecificProgramSerializer()

    class Meta:
        model = Student
        fields = '__all__'

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
                data['img'] = f"https://cassandra-o5ft.onrender.com/static/images/students_img.jpg"

        return data


class SpecificStudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    level = EducationalLevelSerializer()
    program = SpecificProgramSerializer()

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
                data['img'] = f"https://cassandra-o5ft.onrender.com/static/images/students_img.jpg"

        return data


class SpecificStudentWithoutImageSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    level = EducationalLevelSerializer()
    program = SpecificProgramSerializer()

    class Meta:
        model = Student
        fields = ('user', 'st_id', 'gender', 'has_completed', 'current_year', 'program', 'level', 'date_created')
    

# Staff Serializers
class StaffSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    level = EducationalLevelSerializer()
    school = SchoolSerializer()
    subjects = SubjectsSerializer(many=True)

    class Meta:
        model = Staff
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
                data['img'] = f"https://cassandra-o5ft.onrender.com/static/images/staff_img.jpg"

        return data


class DepartmentNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('name', 'date_created')


class SpecificStaffSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    level = EducationalLevelSerializer()
    subjects = SubjectsSerializer(many=True)
    department = DepartmentNameSerializer()

    class Meta:
        model = Staff
        fields = ('staff_id', 'contact', 'img', 'gender', 'user', 'subjects', 'department', 'role', 'dob', 'level', 'date_created')

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

class SpecificStaffWithoutImageSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    subjects = SubjectsSerializer(many=True)
    department = DepartmentNameSerializer()
    level = EducationalLevelSerializer()

    class Meta:
        model = Staff
        fields = ('staff_id', 'contact', 'gender', 'user', 'subjects', 'department', 'role', 'level', 'date_created')
    

# Department Serializers
class DepartmentSerializer(serializers.ModelSerializer):
    teachers = SpecificStaffSerializer(many=True)
    hod = SpecificStaffSerializer()
    subjects = SubjectsSerializer(many=True)

    class Meta:
        model = Department
        fields = "__all__"


# Department Serializers
class SpecificDepartmentSerializer(serializers.ModelSerializer):
    subjects = SubjectsSerializer(many=True)

    class Meta:
        model = Department
        fields = ('name', 'subjects', 'date_created')
        

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
                data['img'] = f"https://cassandra-o5ft.onrender.com/static/images/staff_img.jpg"

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
                data['img'] = f"https://cassandra-o5ft.onrender.com/static/images/staff_img.jpg"

        return data


# Classe Serializers
class ClasseSerializer(serializers.ModelSerializer):
    students = SpecificStudentSerializer(many=True)
    program = SpecificProgramSerializer()
    head_teacher = SpecificStaffWithoutImageSerializer()
    academic_years = AcademicYearSerializer(many=True)
    students_level = EducationalLevelSerializer()

    class Meta:
        model = Classe
        fields = "__all__"


class ClasseWithSubjectsSerializer(serializers.ModelSerializer):
    students = SpecificStudentSerializer(many=True)
    subjects = SubjectsSerializer(many=True)
    program = SpecificProgramSerializer()
    head_teacher = SpecificStaffSerializer()
    academic_years = AcademicYearSerializer(many=True)

    class Meta:
        model = Classe
        fields = "__all__"


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
        fields = ('subject', 'student_year', 'academic_term', 'score', 'date_created')


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
        fields = ('subject', 'student_year', 'academic_term', 'score', 'date', 'percentage', 'title', 'total_score', 'description', 'comment')


class StudentAssessmentSerializer(serializers.ModelSerializer):
    subject = SubjectsSerializer()

    class Meta:
        model = Assessment
        fields = ('subject', 'score', 'date', 'percentage', 'title', 'total_score', 'description', 'comment')
        
        
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
        
        
        