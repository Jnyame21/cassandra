import os
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from pathlib import Path
from Backend.development import *
from django.utils import timezone


# Create your models here.
BASE_DIR = Path(__file__).resolve().parent.parent


def get_school_folder(school_name: str):
    name = school_name.replace(".", "_").replace(" ", "_").replace("'", "").lower()
    return name


def students_file_path(instance, filename):
    # Construct the folder path based on the user's username
    user_folder = instance.user.username
    return f"{get_school_folder(instance.school.name)}/students/{user_folder}/{filename}"
    # if DEBUG:
    #     return f"{get_school_folder(instance.school.name)}/students/{user_folder}/{filename}"
    # else:
    #     return f"{get_school_folder(instance.school.name)}/students/{user_folder}/{filename}"


def staff_file_path(instance, filename):
    # Construct the folder path based on the user's username
    user_folder = instance.user.username
    return f"{get_school_folder(instance.school.name)}/staff/{user_folder}/{filename}"
    # if DEBUG:
    #     return f"{get_school_folder(instance.school.name)}/staff/{user_folder}/{filename}"
    # else:
    #     return f"{get_school_folder(instance.school.name)}/staff/{user_folder}/{filename}"


def school_image_path(instance, filename):
    return f"{get_school_folder(instance.name)}/images/{filename}"
    # if DEBUG:
    #     return f"{get_school_folder(instance.name)}/images/{filename}"
    # else:
    #     return f"{get_school_folder(instance.name)}/images/{filename}"


def school_file_path(instance, filename):
    return f"{get_school_folder(instance.name)}/files/{filename}"
    # if DEBUG:
    #     return f"{get_school_folder(instance.name)}/files/{filename}"
    # else:
    #     return f"{get_school_folder(instance.name)}/files/{filename}"


def head_file_path(instance, filename):
    # Construct the folder path based on the user's username
    user_folder = instance.user.username
    if DEBUG:
        return f"{get_school_folder(instance.school.name)}/head/{user_folder}/{filename}"
    else:
        return f"{get_school_folder(instance.school.name)}/head/{user_folder}/{filename}"


class File(models.Model):
    filename = models.CharField(max_length=50, verbose_name='File Name', blank=False, default='')
    path = models.FileField(upload_to=f"{os.path.join(BASE_DIR, 'staticfiles', 'files')}")

    def __str__(self):
        return self.filename


@receiver(pre_delete, sender=File)
def delete_file(sender, instance, **kwargs):
    # Remove the file from the media folder
    if instance.path:
        if os.path.isfile(instance.path.path):
            os.remove(instance.path.path)


class School(models.Model):
    name = models.CharField(max_length=100, verbose_name="School Name", blank=False, unique=False, null=False)
    identifier = models.CharField(max_length=100, verbose_name="School Identifier", blank=False, unique=False, null=False, default="", db_index=True)
    code = models.CharField(max_length=10, verbose_name="School Code", blank=True, null=True, default="")
    logo = models.ImageField(verbose_name='School Logo', upload_to=school_image_path, blank=True, null=True, max_length=255)
    address = models.CharField(max_length=500, verbose_name="School Address", blank=False, default="")
    region = models.CharField(max_length=500, verbose_name="Region the school is located", blank=False, default="")
    city_town = models.CharField(max_length=500, verbose_name="The city/town the school is located", blank=False, default="")
    postal_address = models.CharField(max_length=200, verbose_name="School's Postal Address", blank=False, default="")
    short_name = models.CharField(max_length=50, verbose_name="School Short Name", blank=True, null=True, default="")
    contact = models.CharField(max_length=20, verbose_name="Phone Number", blank=False, null=False, default="")
    alt_contact = models.CharField(max_length=20, verbose_name="Second Phone Number", blank=True, null=True, default="")
    staff_id = models.BooleanField(verbose_name="Does the school give staff ID numbers?", default=False)
    email = models.EmailField(max_length=100, verbose_name="Email", blank=True, null=True, default="")
    date_created = models.DateField(verbose_name='Date Created', max_length=20, default=timezone.now)

    def __str__(self):
        return self.identifier


class GradingSystemRange(models.Model):
    label = models.CharField(max_length=10, verbose_name="Label", blank=False, null=True)
    upper_limit = models.DecimalField(verbose_name="Upper Limit", max_digits=5, decimal_places=2)
    lower_limit = models.DecimalField(verbose_name="Lower Limit", max_digits=5, decimal_places=2, db_index=True)
    remark = models.CharField(max_length=50, verbose_name="Remark", blank=False, null=True)
    identifier = models.CharField(max_length=100, verbose_name="Grading sytem range identifier", blank=False, null=False, default="", db_index=True)
    
    def __str__(self) -> str:
        return self.identifier
    
    
class GradingSystem(models.Model):
    schools = models.ManyToManyField(School, verbose_name="Schools", blank=True)
    level = models.ForeignKey('EducationalLevel', verbose_name="Level with this grading system", on_delete=models.SET_NULL, null=True) 
    ranges = models.ManyToManyField(GradingSystemRange, verbose_name="Grading System Ranges", blank=True)
    

class EducationalLevel(models.Model):
    schools = models.ManyToManyField(School, verbose_name="Schools", blank=True)
    name = models.CharField(max_length=50, verbose_name="Level name", blank=False, null=True)
    identifier = models.CharField(max_length=100, verbose_name="Level identifier", blank=False, null=False, default="", db_index=True)
    years_to_complete = models.IntegerField(verbose_name="Years to complete this level", default=0)
    has_departments = models.BooleanField(verbose_name="Does the level has departments?", default=False)
    has_programs = models.BooleanField(verbose_name="Does the level has programs?", default=False)
    students_id = models.BooleanField(verbose_name="Does the level give student ID numbers?", default=False, db_index=True)
    students_index_no = models.BooleanField(verbose_name="Does the level give student Index numbers?", default=False)
    
    def __str__(self) -> str:
        return self.identifier


class AcademicYear(models.Model):
    school = models.ForeignKey(School, verbose_name="School", blank=False, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=20, verbose_name="Name", blank=False, db_index=True)
    level = models.ForeignKey(EducationalLevel, verbose_name="Level", on_delete=models.SET_NULL, null=True)
    start_date = models.DateField(verbose_name='Start Date')
    end_date = models.DateField(verbose_name='End Date')
    term_1_end_date = models.DateField(verbose_name="Term 1 End Date", blank=False, null=True)
    term_2_start_date = models.DateField(verbose_name="Term 2 Start Date", blank=False, null=True)
    term_2_end_date = models.DateField(verbose_name="Term 2 End Date", blank=False, null=True)
    term_3_start_date = models.DateField(verbose_name="Term 3 Start Date", blank=True, null=True)
    term_3_end_date = models.DateField(verbose_name="Term 3 End Date", blank=True, null=True)
    period_division = models.CharField(max_length=20, verbose_name="Period Division Name", blank=False, default='TERM')
    no_divisions = models.IntegerField(verbose_name="Number of Divisions", default=3)
    students_graduation_date = models.DateField(verbose_name='Date students will graduated', blank=True, null=True)
    date_created = models.DateField(verbose_name="Date Created", default=timezone.now)

    def __str__(self):
        return f"{self.school} {self.level} {self.name}"
    
    
class Program(models.Model):
    name = models.CharField(max_length=100, verbose_name='Program Name')
    schools = models.ManyToManyField(School, verbose_name="Schools", blank=True)
    identifier = models.CharField(max_length=100, verbose_name="Program identifier", blank=False, null=False, default="", db_index=True)
    subjects = models.ManyToManyField('Subject', verbose_name='Subjects', blank=True)
    level = models.ForeignKey(EducationalLevel, verbose_name="Level", blank=True, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.identifier


class Subject(models.Model):
    schools = models.ManyToManyField(School, verbose_name="Schools", blank=True)
    name = models.CharField(max_length=100, verbose_name='Subject Name', blank=False, unique=True)
    identifier = models.CharField(max_length=100, verbose_name="Subject identifier", blank=False, null=False, default="", db_index=True)
    level = models.ForeignKey(EducationalLevel, verbose_name="Level", blank=True, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.identifier      


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    school = models.ForeignKey(School, verbose_name="School", blank=False, on_delete=models.SET_NULL, null=True)
    current_level = models.ForeignKey(EducationalLevel, related_name='current_level', verbose_name="Current Level", blank=False, on_delete=models.SET_NULL, null=True)
    levels = models.ManyToManyField(EducationalLevel, related_name='levels', verbose_name="Levels", blank=True)
    programs = models.ManyToManyField(Program, related_name='programs', verbose_name='Programs', blank=True)
    current_program = models.ForeignKey(Program, related_name='current_program', verbose_name='Current Program', on_delete=models.SET_NULL, null=True, blank=True)
    st_class = models.ForeignKey('Classe', related_name='st_class', verbose_name='Class', null=True, on_delete=models.SET_NULL, blank=True)
    current_year = models.IntegerField(verbose_name='Current Year', default=1, db_index=True)
    date_enrolled = models.DateField(verbose_name='Enrollment Date', blank=False, default=timezone.now)
    st_id = models.CharField(max_length=50, verbose_name="Student ID.", blank=False, null=True, db_index=True)
    index_no = models.CharField(max_length=20, verbose_name="Index No.", default='none')
    img = models.ImageField(verbose_name='Profile Image', upload_to=students_file_path, blank=True, null=True, max_length=255)
    academic_years = models.ManyToManyField(AcademicYear, related_name='academic_years', verbose_name='Academic Years', blank=True)
    repeated_academic_years = models.ManyToManyField(AcademicYear, related_name='repeated_academic_years', verbose_name='Repeated Academic Years', blank=True)
    gender = models.CharField(max_length=10, verbose_name="Gender")
    dob = models.DateField(verbose_name='Date Of Birth')
    contact = models.CharField(verbose_name='Phone No', max_length=15, default='')
    address = models.CharField(verbose_name='Address', max_length=100, default='')
    religion = models.CharField(verbose_name='Religion', max_length=50, default='')
    pob = models.CharField(verbose_name='Home City/Town', max_length=50, default='')
    region = models.CharField(verbose_name='Region', max_length=100, default='')
    religion = models.CharField(verbose_name='Religion', max_length=100, default='')
    nationality = models.CharField(verbose_name='Nationality', max_length=50, default='')
    email = models.EmailField( max_length=254, blank=True, null=True, verbose_name="Email Address", default='')
    guardian = models.CharField(max_length=100, verbose_name='Guardian Name', default='')
    guardian_gender = models.CharField(max_length=100, verbose_name='Guardian Gender', default='')
    guardian_email = models.CharField(max_length=100, verbose_name='Guardian Email', default='')
    guardian_occupation = models.CharField(max_length=50, verbose_name='Occupation of guardian', default='')
    guardian_nationality = models.CharField(max_length=50, verbose_name='Nationality of Guardian', default='')
    guardian_contact = models.CharField(max_length=15, verbose_name='Phone no. of guardian', default='')
    guardian_address = models.CharField(max_length=100, verbose_name='Address of guardian', default='')
    date_created = models.DateField(verbose_name='Date Created', default=timezone.now)

    def __str__(self):
        return f"{self.school} {self.user.first_name} {self.user.last_name}"

    class Meta:
        unique_together = ('st_id', 'school')


class StaffRole(models.Model):
    schools = models.ManyToManyField(School, verbose_name="Schools", blank=True)
    name = models.CharField(max_length=100, verbose_name='Role Name', blank=False)
    identifier = models.CharField(max_length=100, verbose_name="Staff Role identifier", blank=False, null=False, default="", db_index=True)
    level = models.ForeignKey(EducationalLevel, verbose_name="Level", blank=False, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.identifier}"
    
    
class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    school = models.ForeignKey(School, verbose_name="School", blank=False, on_delete=models.SET_NULL, null=True)
    img = models.ImageField(verbose_name="Profile Image", upload_to=staff_file_path, blank=True, null=True, max_length=255)
    staff_id = models.CharField(max_length=50, verbose_name='Staff ID', blank=False, null=True, db_index=True)
    signature = models.ImageField(verbose_name="Staff signature", upload_to=staff_file_path, blank=True, null=True, max_length=255)
    roles = models.ManyToManyField(StaffRole, related_name='staff_roles', verbose_name='Roles', blank=False)
    current_role = models.ForeignKey(StaffRole, verbose_name='Role', blank=False, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=50, verbose_name='staff title', blank=True, default='')
    subjects = models.ManyToManyField('Subject', verbose_name='Subject(s) taught', blank=True)
    departments = models.ManyToManyField('Department', verbose_name='Staff departments', blank=True)
    date_enrolled = models.DateField(verbose_name='Enrollment Date', blank=True, null=True)
    gender = models.CharField(max_length=10, verbose_name="Gender")
    dob = models.DateField(verbose_name='Date Of Birth')
    contact = models.CharField(verbose_name='Phone No', max_length=20, default='')
    alt_contact = models.CharField(verbose_name='Alternate Phone No', max_length=15, default='')
    address = models.CharField(verbose_name='Address', max_length=100, default='')
    pob = models.CharField(verbose_name='Home City/Town', max_length=50, default='')
    religion = models.CharField(verbose_name='Religion', max_length=100, default='')
    email = models.EmailField( max_length=254, blank=True, null=True, verbose_name="Email Address", default='')
    region = models.CharField(verbose_name='Region', max_length=50, default='')
    nationality = models.CharField(verbose_name='Nationality', max_length=50, default='')
    is_active = models.BooleanField(verbose_name='Staff is Active', default=True, db_index=True)
    date_created = models.DateField(verbose_name='Date Created', max_length=20, default=timezone.now)

    def __str__(self):
        return f"{self.school} {self.user.first_name} {self.user.last_name}" if self.user else f"{self.school} {self.user}"

    class Meta:
        unique_together = ('staff_id', 'school')


class Department(models.Model):
    school = models.ForeignKey(School, verbose_name="School", blank=False, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100, verbose_name='Department Name', blank=False)
    identifier = models.CharField(max_length=100, verbose_name="Department identifier", blank=False, null=False, default="", db_index=True)
    teachers = models.ManyToManyField(Staff, related_name='department_teachers', verbose_name='Teachers', blank=True)
    hod = models.ForeignKey(Staff, verbose_name='HOD', related_name='department_hod', on_delete=models.SET_NULL, null=True, blank=True)
    subjects = models.ManyToManyField(Subject, verbose_name='Subjects', blank=True)
    level = models.ForeignKey(EducationalLevel, verbose_name="Level", blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.identifier}"


class Classe(models.Model):
    school = models.ForeignKey(School, verbose_name="School", blank=False, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50, verbose_name='Class Name')
    identifier = models.CharField(max_length=100, verbose_name="Class identifier", blank=False, null=False, default="")
    level = models.ForeignKey(EducationalLevel, verbose_name="Level", blank=False, on_delete=models.SET_NULL, null=True)
    students_year = models.IntegerField(verbose_name='Students Year', default=1, db_index=True)
    students = models.ManyToManyField(Student, verbose_name='Students', blank=True)
    program = models.ForeignKey(Program, verbose_name='Students Program', on_delete=models.SET_NULL, null=True, blank=True)
    head_teacher = models.ForeignKey(Staff, verbose_name='Head Teacher', on_delete=models.SET_NULL, null=True, blank=True)
    subjects = models.ManyToManyField('Subject', verbose_name='Subjects', blank=True)
    linked_class = models.ForeignKey('self', verbose_name='Linked to class', blank=True, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.identifier}"

    class Meta:
        unique_together = ('name', 'students_year', 'program', 'level', 'school')


class GraduatedClasse(models.Model):
    school = models.ForeignKey(School, verbose_name="School", blank=False, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50, verbose_name='Class Name')
    level = models.ForeignKey(EducationalLevel, verbose_name="Level", blank=False, on_delete=models.SET_NULL, null=True)
    students = models.ManyToManyField(Student, verbose_name='Students', blank=True)
    class_graduated_from = models.ForeignKey(Classe, verbose_name='Class Graduated From', on_delete=models.SET_NULL, null=True)
    graduated_academic_year = models.ForeignKey(AcademicYear, verbose_name='Graduation Academic Year', null=True, on_delete=models.SET_NULL, blank=True)

    def __str__(self):
        return f"{self.school} {self.name}"

    class Meta:
        unique_together = ('name', 'school')
        
        
class LinkedClasse(models.Model):
    school = models.ForeignKey(School, verbose_name="School", blank=False, on_delete=models.SET_NULL, null=True)
    level = models.ForeignKey(EducationalLevel, verbose_name="Level", blank=False, on_delete=models.SET_NULL, null=True)
    from_class = models.ForeignKey(Classe, related_name='from_class', verbose_name='From Class Name', on_delete=models.SET_NULL, null=True)
    to_class = models.ForeignKey(Classe, related_name='to_class', verbose_name='To Class Name', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.level} From {self.from_class} To {self.to_class}"
    
    class Meta:
        unique_together = ('level', 'from_class', 'school')


class SubjectAssignment(models.Model):
    school = models.ForeignKey(School, verbose_name="School", blank=False, on_delete=models.SET_NULL, null=True)
    level = models.ForeignKey(EducationalLevel, verbose_name="Level", blank=False, on_delete=models.SET_NULL, null=True)
    assigned_by = models.ForeignKey(Staff, related_name='assigned_by', verbose_name="Assigned By", on_delete=models.SET_NULL, null=True, blank=True)
    subjects = models.ManyToManyField(Subject, verbose_name='Subject(s)', blank=True)
    teacher = models.ForeignKey(Staff, on_delete=models.SET_NULL, verbose_name='Taught by', null=True)
    students_class = models.ForeignKey(Classe, on_delete=models.SET_NULL, verbose_name='Students Class', null=True)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.SET_NULL, verbose_name='Academic Year', null=True)
    academic_term = models.IntegerField(verbose_name='Academic Term', default=1, db_index=True)
    date_created = models.DateField(verbose_name='Date Created', max_length=20, default=timezone.now)

    def __str__(self):
        return f'{self.school} {self.teacher} to {self.students_class} for the {self.academic_year} academic year term {self.academic_term} in {self.level}'

    class Meta:
        unique_together = ('teacher', 'students_class', 'academic_year', 'academic_term')


class Assessment(models.Model):
    school = models.ForeignKey(School, verbose_name="School", blank=False, on_delete=models.SET_NULL, null=True)
    level = models.ForeignKey(EducationalLevel, verbose_name="School", blank=False, on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey(Student, verbose_name='Student', on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.ForeignKey(Subject, verbose_name='Subject', on_delete=models.SET_NULL, null=True, blank=False)
    student_class = models.ForeignKey(Classe, verbose_name='Student Class', on_delete=models.SET_NULL, null=True, blank=False)
    academic_year = models.ForeignKey(AcademicYear, verbose_name='Academic Year', on_delete=models.SET_NULL, null=True, blank=False)
    teacher = models.ForeignKey(Staff, verbose_name="Uploaded By", on_delete=models.SET_NULL, null=True, blank=True)
    academic_term = models.IntegerField(verbose_name='Term', blank=False, null=False, db_index=True)
    score = models.DecimalField(verbose_name="Student's Score", max_digits=6, decimal_places=2, blank=True, null=True, db_index=True)
    total_score = models.DecimalField(verbose_name="Total Assessment Score", max_digits=6, decimal_places=2, blank=False, null=False)
    percentage = models.DecimalField(verbose_name="Assessment Percentage", max_digits=5, decimal_places=2)
    title = models.CharField(verbose_name="Title Of Assessment", max_length=50, blank=False, null=False, db_index=True)
    description = models.CharField(verbose_name="Assessment description", max_length=100, blank=True)
    comment = models.CharField(verbose_name="Comment", max_length=100, blank=True)
    assessment_date = models.DateField(verbose_name='Date the assessment was conducted')
    created_at = models.DateField(verbose_name='Date Created', auto_now_add=True, null=True)
    updated_at = models.DateField(verbose_name='Date Created', auto_now=True, null=True)
    
    def __str__(self):
        return f"{self.school} {self.level} {self.student} {self.title}"

    class Meta:
        unique_together = ('student', 'subject', 'academic_year', 'academic_term', 'teacher', 'title')
        
        
class Exam(models.Model):
    school = models.ForeignKey(School, verbose_name="School", blank=False, on_delete=models.SET_NULL, null=True)
    level = models.ForeignKey(EducationalLevel, verbose_name="School", blank=False, on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey(Student, verbose_name='Student', on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subject, verbose_name='Subject', on_delete=models.SET_NULL, null=True)
    student_class = models.ForeignKey(Classe, verbose_name='Student Class', on_delete=models.SET_NULL, null=True)
    academic_year = models.ForeignKey(AcademicYear, verbose_name='Academic Year', on_delete=models.SET_NULL, null=True)
    academic_term = models.IntegerField(verbose_name='Term', blank=False, db_index=True)
    score = models.DecimalField(verbose_name="Student's Score", max_digits=5, decimal_places=2, db_index=True)
    teacher = models.ForeignKey(Staff, verbose_name="Uploaded By", on_delete=models.SET_NULL, null=True)
    total_score = models.DecimalField(verbose_name="Total Exams Score", max_digits=6, decimal_places=2)
    percentage = models.DecimalField(verbose_name="Exam Percentage", max_digits=5, decimal_places=2)
    date_created = models.DateField(verbose_name='Date Created', max_length=20, default=timezone.now)
    
    def __str__(self):
        return f"{self.school} {self.student} {self.subject} exam for the {self.academic_year} academic year term {self.academic_term} in {self.level}"

    class Meta:
        unique_together = ('student', 'subject', 'academic_year', 'academic_term', 'teacher')


class StudentResult(models.Model):
    school = models.ForeignKey(School, verbose_name="School", blank=False, on_delete=models.SET_NULL, null=True)
    level = models.ForeignKey(EducationalLevel, verbose_name="School", blank=False, on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey(Student, verbose_name='Student', on_delete=models.SET_NULL, null=True)
    teacher = models.ForeignKey(Staff, verbose_name="Uploaded By", on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subject, verbose_name='Subject', on_delete=models.SET_NULL, null=True)
    student_class = models.ForeignKey(Classe, verbose_name='Student Class', on_delete=models.SET_NULL, null=True)
    academic_year = models.ForeignKey(AcademicYear, verbose_name='Academic Year', on_delete=models.SET_NULL, null=True)
    academic_term = models.IntegerField(verbose_name='Term', blank=False, db_index=True)
    exam_percentage = models.DecimalField(verbose_name="Percentage Of Exams", max_digits=5, decimal_places=2, blank=False, null=True)
    exam_score = models.DecimalField(verbose_name="Students's Exam Score", max_digits=5, decimal_places=2, blank=False, null=True)
    total_assessment_percentage = models.DecimalField(verbose_name="Percentage Of Assessments", max_digits=5, decimal_places=2, blank=False, null=True)
    total_assessment_score = models.DecimalField(verbose_name="Total Students's Assessment Score", max_digits=5, decimal_places=2, blank=False, null=True)
    result = models.DecimalField(verbose_name="Result", max_digits=5, decimal_places=2, blank=False, null=True, db_index=True)
    grade = models.CharField(max_length=10, verbose_name="Student's Grade", blank=False, null=True)
    position = models.CharField(max_length=50, verbose_name="Student's Position", blank=True)
    remark = models.CharField(max_length=20, verbose_name="Remark", blank=False, null=True)
    created_at = models.DateField(verbose_name='Date Created', max_length=20, default=timezone.now)
    updated_at = models.DateField(verbose_name='Date Created', auto_now=True, null=True)
    
    def __str__(self):
        return f"{self.school} {self.student} {self.subject} result for the {self.academic_year} academic year term {self.academic_term} in {self.level}"

    class Meta:
        unique_together = ('student', 'subject', 'academic_year', 'academic_term', 'teacher')
        

class StudentAttendance(models.Model):
    school = models.ForeignKey(School, verbose_name="School", blank=False, on_delete=models.SET_NULL, null=True)
    level = models.ForeignKey(EducationalLevel, verbose_name="School", blank=False, on_delete=models.SET_NULL, null=True)
    students_present = models.ManyToManyField(Student, related_name='students_present', verbose_name='Students Present', blank=True)
    students_absent = models.ManyToManyField(Student, related_name='students_absent', verbose_name='Students Absent', blank=True)
    academic_year = models.ForeignKey(AcademicYear, verbose_name='Academic Year', on_delete=models.SET_NULL, null=True)
    academic_term = models.IntegerField(verbose_name='Term', blank=False, db_index=True)
    students_class = models.ForeignKey('Classe', verbose_name='Students Class', on_delete=models.SET_NULL, null=True)
    date = models.DateField(verbose_name="Attendance Date", default=timezone.now)
    teacher = models.ForeignKey(Staff, verbose_name="Uploaded By", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.school} attendance by {self.teacher} for the {self.academic_year} academic year term {self.academic_term} in {self.level}"

    class Meta:
        unique_together = ('level', 'academic_year', 'academic_term', 'teacher', 'date', 'students_class')


class ReleasedResult(models.Model):
    school = models.ForeignKey(School, verbose_name="School", blank=False, on_delete=models.SET_NULL, null=True)
    level = models.ForeignKey(EducationalLevel, verbose_name="School", blank=False, on_delete=models.SET_NULL, null=True)
    academic_year = models.ForeignKey(AcademicYear, verbose_name='Academic Year', on_delete=models.SET_NULL, null=True)
    academic_term = models.IntegerField(verbose_name='Term', blank=False, db_index=True)
    students_class = models.ForeignKey('Classe', verbose_name='Students Class', on_delete=models.SET_NULL, null=True)
    date = models.DateField(verbose_name="Results Released Date", default=timezone.now, db_index=True)
    released_by = models.ForeignKey(Staff, verbose_name="Released By", on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ('level', 'academic_year', 'academic_term', 'released_by', 'students_class')
        
        
# class Notification(models.Model):
#     content = models.CharField(max_length=500, verbose_name='Message', blank=False)
#     from_head = models.ForeignKey(Head, related_name='from_head', verbose_name='From Head', on_delete=models.SET_NULL, null=True, blank=True)
#     from_staff = models.ForeignKey(Staff, related_name='from_staff', verbose_name='From Staff', on_delete=models.SET_NULL, null=True, blank=True)
#     from_student = models.ForeignKey(Student, related_name='from_student', verbose_name='From Student', on_delete=models.SET_NULL, null=True, blank=True)
#     to_staff = models.ManyToManyField(Staff, related_name='to_staff', verbose_name='To Staff')
#     to_student = models.ManyToManyField(Student, related_name='to_student', verbose_name='To Student')
#     date_time = models.DateTimeField(verbose_name='At', auto_now_add=True)

#     def __str__(self):
#         return self.content


# class KnustProgram(models.Model):
#     name = models.CharField(max_length=500, verbose_name='Program Name', blank=False)
#     degree = models.CharField(max_length=500, verbose_name='Degree', blank=False)
#     cut_off_point = models.CharField(max_length=500, verbose_name='Cut-off point', null=True, blank=True)

#     def __str__(self):
#         return self.name   
    
    
# class UGProgram(models.Model):
#     name = models.CharField(max_length=500, verbose_name='Program Name', blank=False)
#     degree = models.CharField(max_length=500, verbose_name='Degree', blank=False)
#     cut_off_point_choice_1 = models.CharField(max_length=500, verbose_name='First choice cut-off point', null=True, blank=True)
#     cut_off_point_choice_2 = models.CharField(max_length=500, verbose_name='Second choice cut-off point', null=True, blank=True)
#     subject_requirement = models.CharField(max_length=500, verbose_name='Subject requirement', null=True, blank=True)

#     def __str__(self):
#         return self.name  


# class UCCProgram(models.Model):
#     name = models.CharField(max_length=500, verbose_name='Program Name', blank=False)
#     degree = models.CharField(max_length=500, verbose_name='Degree', blank=False)
#     cut_off_point_male = models.CharField(max_length=500, verbose_name='Cut-off point for males', null=True, blank=True)
#     cut_off_point_female = models.CharField(max_length=500, verbose_name='Cut-off point for females', null=True, blank=True)

#     def __str__(self):
#         return self.name  
    

# class University(models.Model):
#     name = models.CharField(max_length=500, verbose_name='Name of University ', blank=False)
#     aka = models.CharField(max_length=500, verbose_name='Short Name', blank=False)

#     def __str__(self):
#         return self.name  


