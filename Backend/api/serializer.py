from rest_framework import serializers
from api.models import *
from django.contrib.auth.models import User
import os
from django.conf import settings
from api.utils import *
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
        fields = ['name']


class AcademicYearSerializer(serializers.ModelSerializer):
    # school = SchoolSerializer()

    class Meta:
        model = AcademicYear
        fields = '__all__'


# Course Serializers
class SubjectsSerializer(serializers.ModelSerializer):
    # schools = SchoolSerializer(many=True)

    class Meta:
        model = Subject
        fields = '__all__'


class ProgramSerializer(serializers.ModelSerializer):
    subjects = SubjectsSerializer(many=True)
    # schools = SchoolSerializer(many=True)

    class Meta:
        model = Program
        fields = '__all__'


class SpecificProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ['name']


#  Student Serializers
class StudentSerializer(serializers.ModelSerializer):
    school = SchoolSerializer()
    user = UserSerializer()
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
                data['img'] = f"https://eduaap.onrender.com/static/images/students_img.jpg"

        return data


class SpecificStudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    program = SpecificProgramSerializer()

    class Meta:
        model = Student
        fields = ('user', 'img', 'st_id', 'gender', 'has_completed', 'current_year', 'program', 'dob')

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
                data['img'] = f"https://eduaap.onrender.com/static/images/students_img.jpg"

        return data


# Staff Serializers
class StaffSerializer(serializers.ModelSerializer):
    user = UserSerializer()
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
                data['img'] = f"https://eduaap.onrender.com/static/images/staff_img.jpg"

        return data


class DepartmentNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['name']


class SpecificStaffSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    subjects = SubjectsSerializer(many=True)
    department = DepartmentNameSerializer()

    class Meta:
        model = Staff
        fields = ('staff_id', 'contact', 'img', 'gender', 'user', 'subjects', 'department', 'role', 'dob')

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
                data['img'] = f"https://eduaap.onrender.com/static/images/staff_img.jpg"

        return data


# Department Serializers
class DepartmentSerializer(serializers.ModelSerializer):
    teachers = SpecificStaffSerializer(many=True)
    hod = SpecificStaffSerializer()
    subjects = SubjectsSerializer(many=True)

    class Meta:
        model = Department
        fields = "__all__"


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
                data['img'] = f"https://eduaap.onrender.com/static/images/staff_img.jpg"

        return data


class SpecificHeadSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Head
        fields = ('head_id', 'contact', 'img', 'gender', 'user', 'role', 'dob')

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
                data['img'] = f"https://eduaap.onrender.com/static/images/staff_img.jpg"

        return data


# Classe Serializers
class ClasseSerializer(serializers.ModelSerializer):
    students = SpecificStudentSerializer(many=True)
    program = SpecificProgramSerializer()
    academic_years = AcademicYearSerializer(many=True)

    class Meta:
        model = Classe
        fields = "__all__"


class ClasseWithSubjectsSerializer(serializers.ModelSerializer):
    students = SpecificStudentSerializer(many=True)
    subjects = SubjectsSerializer(many=True)
    program = SpecificProgramSerializer()
    academic_years = AcademicYearSerializer(many=True)

    class Meta:
        model = Classe
        fields = "__all__"


class ClasseWithoutStudentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Classe
        fields = ('name', 'students_year')


# Course Assignment Serializers
class SubjectAssignmentSerializer(serializers.ModelSerializer):
    students_class = ClasseSerializer()
    subject = SubjectsSerializer()
    teacher = SpecificStaffSerializer()

    class Meta:
        model = SubjectAssignment
        fields = ('students_class', 'subject', 'teacher')


class SubjectAssignmentWithoutStudentsSerializer(serializers.ModelSerializer):
    students_class = ClasseWithoutStudentsSerializer()
    subject = SubjectsSerializer()
    teacher = SpecificStaffSerializer()

    class Meta:
        model = SubjectAssignment
        fields = ('students_class', 'subject', 'teacher')

        
# Results Serializers
class ResultsSerializer(serializers.ModelSerializer):
    student = SpecificStudentSerializer()
    subject = SubjectsSerializer()
    academic_year = AcademicYearSerializer()
    teacher = SpecificStaffSerializer()

    class Meta:
        model = Result
        fields = "__all__"


class StudentResultsSerializer(serializers.ModelSerializer):
    subject = SubjectsSerializer()

    class Meta:
        model = Result
        fields = ('subject', 'score')


# Students Attendance
class StudentsAttendanceSerializer(serializers.ModelSerializer):
    students_class = ClasseWithoutStudentsSerializer()
    subject = SubjectsSerializer()
    teacher = SpecificStaffSerializer()
    students_present = SpecificStudentSerializer(many=True)
    students_absent = SpecificStudentSerializer(many=True)

    class Meta:
        model = StudentAttendance
        fields = '__all__'


# Staff Message Serializer
class NotificationStaff(serializers.ModelSerializer):
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
                data['img'] = f"https://eduaap.onrender.com/static/images/staff_img.jpg"

        return data


class NotificationHead(serializers.ModelSerializer):
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
                data['img'] = f"https://eduaap.onrender.com/static/images/staff_img.jpg"

        return data


class StaffNotificationSerializer(serializers.ModelSerializer):
    sent_by_hod = NotificationStaff()
    sent_by_head = NotificationHead()
    send_to = NotificationStaff(many=True)

    class Meta:
        model = StaffNotification
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


