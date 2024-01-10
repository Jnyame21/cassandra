import os
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from pathlib import Path
from django.utils import timezone


# Create your models here.
BASE_DIR = Path(__file__).resolve().parent.parent


def get_school_folder(school_name: str):
    name = school_name.replace(".", "_").replace(" ", "_").replace("'", "").lower()
    return name


def students_file_path(instance, filename):
    # Construct the folder path based on the user's username
    # user_folder = instance.user.username
    # Combine the folder path and filename
    return os.path.join(BASE_DIR, 'staticfiles', f"{get_school_folder(instance.school.name)}", 'students', 'img', filename)


def staff_file_path(instance, filename):
    # Construct the folder path based on the user's username
    # user_folder = instance.user.username
    # Combine the folder path and filename
    return os.path.join(BASE_DIR, 'staticfiles', f"{get_school_folder(instance.school.name)}", 'staff', 'img', filename)


def head_file_path(instance, filename):
    # Construct the folder path based on the user's username
    user_folder = instance.user.username
    # Combine the folder path and filename
    return os.path.join(BASE_DIR, 'staticfiles', f"{get_school_folder(instance.school.name)}" , 'head', user_folder, filename)


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
    name = models.CharField(max_length=100, verbose_name="School Name", blank=False, unique=True, null=False)
    code = models.CharField(max_length=10, verbose_name="School Code", blank=True, null=True)
    semesters = models.BooleanField(verbose_name="Semester System", default=True, blank=False, null=False)
    address = models.CharField(max_length=100, verbose_name="School Address", blank=False, default="not set")
    short_name = models.CharField(max_length=50, verbose_name="School Short Name", blank=True, null=True)
    contact = models.CharField(max_length=20, verbose_name="Phone Number", blank=True, null=True)
    email = models.EmailField(max_length=100, verbose_name="Email", blank=True, null=True)
    delete_staff = models.BooleanField(verbose_name="Admin To Delete Staff", default=True, blank=False, null=False)
    delete_class = models.BooleanField(verbose_name="Admin To Delete Class", default=True, blank=False, null=False)

    def __str__(self):
        return self.name


class AcademicYear(models.Model):
    name = models.CharField(max_length=20, verbose_name="Name", blank=False, unique=True)
    start_date = models.DateField(verbose_name='Start Date')
    end_date = models.DateField(verbose_name='End Date')
    school = models.ForeignKey(School, verbose_name="School", on_delete=models.SET_NULL, null=True)
    sem_1_end_date = models.DateField(verbose_name="First Semester End Date", blank=False, null=True)
    sem_2_start_date = models.DateField(verbose_name="Second Semester Start Date", blank=False, null=True)
    sem_2_end_date = models.DateField(verbose_name="Second Semester End Date", blank=False, null=True)
    sem_3_start_date = models.DateField(verbose_name="Third Semester Start Date", blank=True, null=True)
    sem_3_end_date = models.DateField(verbose_name="Third Semester End Date", blank=True, null=True)

    def __str__(self):
        return f"{self.school} {self.name}"


class Program(models.Model):
    name = models.CharField(max_length=100, verbose_name='Program Name', unique=True)
    subjects = models.ManyToManyField('Subject', verbose_name='Subjects', blank=True)
    schools = models.ManyToManyField(School, verbose_name="Schools", blank=True)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=100, verbose_name='Subject Name', blank=False, unique=True)
    schools = models.ManyToManyField(School, verbose_name="Schools", blank=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    school = models.ForeignKey(School, verbose_name="School", blank=False, on_delete=models.SET_NULL, null=True)
    program = models.ForeignKey(Program, verbose_name='Program', on_delete=models.SET_NULL, null=True)
    st_class = models.ForeignKey('Classe', verbose_name='Class', null=True, on_delete=models.SET_NULL)
    current_year = models.IntegerField(verbose_name='Current Year', default=1)
    date_enrolled = models.DateField(verbose_name='Enrollment Date', blank=False)
    has_completed = models.BooleanField(verbose_name='Has Completed', default=False)
    st_id = models.CharField(max_length=50, verbose_name="Student ID.", blank=False, null=True)
    index_no = models.CharField(max_length=20, verbose_name="Index No.", default='not assigned yet')
    img = models.ImageField(verbose_name='Profile Image', upload_to=students_file_path, blank=True, null=True, max_length=255)

    gender = models.CharField(max_length=10, verbose_name="Gender")
    dob = models.DateField(verbose_name='Date Of Birth')
    contact = models.CharField(verbose_name='Phone No', max_length=20, default='not set')
    alt_contact = models.CharField(verbose_name='Alternate Phone No', max_length=15, default='not set', blank=True, null=True)
    address = models.CharField(verbose_name='Address', max_length=100, default='not set')
    religion = models.CharField(verbose_name='Religion', max_length=50, default='not set')
    pob = models.CharField(verbose_name='Home City/Town', max_length=50, default='not set')
    region = models.CharField(verbose_name='Region', max_length=50, default='not set')
    nationality = models.CharField(verbose_name='Nationality', max_length=50, default='GHANA')
    guardian = models.CharField(max_length=100, verbose_name='Guardian Name', default='not set')
    guardian_gender = models.CharField(max_length=100, verbose_name='Guardian Gender')
    guardian_email = models.CharField(max_length=100, verbose_name='Guardian Email', default='not set')
    guardian_occupation = models.CharField(max_length=50, verbose_name='Occupation of guardian', default='not set')
    guardian_nationality = models.CharField(max_length=50, verbose_name='Nationality of Guardian', default='GHANA')
    guardian_contact = models.CharField(max_length=10, verbose_name='Phone no. of guardian', default='not set')
    guardian_address = models.CharField(max_length=100, verbose_name='Address of guardian', default='not set')

    def __str__(self):
        return f"{self.school} {self.user.first_name} {self.user.last_name}"

    class Meta:
        unique_together = ('st_id', 'school')


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    school = models.ForeignKey(School, verbose_name="School", blank=False, on_delete=models.SET_NULL, null=True)
    img = models.ImageField(verbose_name="Profile Image", upload_to=staff_file_path, blank=True, null=True, max_length=255)
    staff_id = models.CharField(max_length=50, verbose_name='Staff ID', blank=False)
    role = models.CharField(max_length=50, verbose_name='Staff Role', blank=False, default='teacher')
    subjects = models.ManyToManyField('Subject', verbose_name='Subject(s) taught', blank=True)
    department = models.ForeignKey('Department', related_name='staff_department', verbose_name='Department', blank=True, on_delete=models.SET_NULL, null=True)
    date_enrolled = models.DateField(verbose_name='Enrollment Date', blank=True, null=True)
    gender = models.CharField(max_length=10, verbose_name="Gender", default='not set')
    dob = models.DateField(verbose_name='Date Of Birth')
    contact = models.CharField(verbose_name='Phone No', max_length=20, default='not set')
    address = models.CharField(verbose_name='Address', max_length=100, default='not set')
    pob = models.CharField(verbose_name='Home City/Town', max_length=50, default='not set')
    region = models.CharField(verbose_name='Region', max_length=50, default='not set')
    nationality = models.CharField(verbose_name='Nationality', max_length=50, default='not set')

    def __str__(self):
        return f"{self.school} {self.user.first_name} {self.user.last_name}"

    class Meta:
        unique_together = ('staff_id', 'school', 'dob', 'contact', 'address')


class Head(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    school = models.ForeignKey(School, verbose_name="School", blank=False, on_delete=models.SET_NULL, null=True)
    img = models.ImageField(verbose_name="Profile Image", upload_to=head_file_path, blank=True, null=True, max_length=255)
    head_id = models.CharField(max_length=50, verbose_name='Head ID', blank=False)
    role = models.CharField(max_length=50, verbose_name='Head Role', blank=True, null=True)
    date_enrolled = models.DateField(verbose_name='Enrollment Date', blank=True)
    gender = models.CharField(max_length=10, verbose_name="Gender")
    dob = models.DateField(verbose_name='Date Of Birth', blank=False)
    contact = models.CharField(verbose_name='Phone No', max_length=20)
    address = models.CharField(verbose_name='Address', max_length=100)
    pob = models.CharField(verbose_name='Home City/Town', max_length=50)
    region = models.CharField(verbose_name='Region', max_length=50)
    nationality = models.CharField(verbose_name='Nationality', max_length=50)

    def __str__(self):
        return f"{self.school} {self.user.first_name} {self.user.last_name}"

    class Meta:
        unique_together = ('head_id', 'school', 'dob', 'contact', 'address')


class Department(models.Model):
    name = models.CharField(max_length=100, verbose_name='Department Name', blank=False)
    teachers = models.ManyToManyField(Staff, related_name='department_teachers', verbose_name='Teachers', blank=True)
    hod = models.ForeignKey(Staff, verbose_name='HOD', related_name='department_hod', on_delete=models.SET_NULL, null=True, blank=True)
    subjects = models.ManyToManyField(Subject, verbose_name='Subjects')
    school = models.ForeignKey(School, verbose_name="School", blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.school} {self.name}"


class Classe(models.Model):
    school = models.ForeignKey(School, verbose_name="School", blank=False, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50, verbose_name='Class Name')
    students_year = models.IntegerField(verbose_name='Students Year', default=1)
    students = models.ManyToManyField(Student, verbose_name='Students', blank=True)
    program = models.ForeignKey(Program, verbose_name='Students Program', on_delete=models.SET_NULL, null=True)
    completion_date = models.DateField(verbose_name='Completion Date', null=True, blank=True)
    subjects = models.ManyToManyField('Subject', verbose_name='Subjects', blank=True)
    academic_years = models.ManyToManyField(AcademicYear, verbose_name='Academic Years')
    date_enrolled = models.DateField(verbose_name='Enrollment Date', blank=False, null=True)
    created_at = models.DateTimeField(verbose_name="Created At", default=timezone.now())
    is_active = models.BooleanField(verbose_name='Class is Active', default=True)

    def __str__(self):
        return f"{self.school} {self.name}"

    class Meta:
        unique_together = ('name', 'students_year', 'program', 'school')


class SubjectAssignment(models.Model):
    school = models.ForeignKey(School, verbose_name="School", blank=False, on_delete=models.SET_NULL, null=True)
    hod = models.ForeignKey(Staff, related_name='hod', verbose_name="Assigned By", on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, verbose_name='Subject')
    teacher = models.ForeignKey(Staff, on_delete=models.SET_NULL, verbose_name='Taught by', null=True)
    students_class = models.ForeignKey(Classe, on_delete=models.SET_NULL, verbose_name='Students Class', null=True)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.SET_NULL, verbose_name='Academic Year', null=True)
    academic_term = models.IntegerField(verbose_name='Academic Term', default=1)

    def __str__(self):
        return f'{self.subject} taught by {self.teacher} to {self.students_class} for the {self.academic_year} academic year term {self.academic_term} in {self.school}'

    class Meta:
        unique_together = ('subject', 'teacher', 'students_class', 'academic_year', 'academic_term')


class Result(models.Model):
    school = models.ForeignKey(School, verbose_name="School", blank=False, on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey(Student, verbose_name='Student', on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subject, verbose_name='Subject', on_delete=models.SET_NULL, null=True)
    academic_year = models.ForeignKey(AcademicYear, verbose_name='Academic Year', on_delete=models.SET_NULL, null=True)
    academic_term = models.IntegerField(verbose_name='Term', blank=False)
    student_year = models.IntegerField(verbose_name='Student Year', blank=True, null=True)
    score = models.DecimalField(verbose_name="Student's Score", max_digits=5, decimal_places=2)
    teacher = models.ForeignKey(Staff, verbose_name="Uploaded By", on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f"{self.student} {self.subject} result for the {self.academic_year} academic year term {self.academic_term} in {self.school}"

    class Meta:
        unique_together = ('student', 'subject', 'academic_year', 'academic_term', 'teacher')


class StaffNotification(models.Model):
    content = models.CharField(max_length=500, verbose_name='Message', blank=False)
    sent_by_hod = models.ForeignKey(Staff, verbose_name='HOD', on_delete=models.SET_NULL, null=True)
    sent_by_head = models.ForeignKey(Head, verbose_name='HEAD', on_delete=models.SET_NULL, null=True)
    send_to = models.ManyToManyField(Staff, related_name='send_to', verbose_name='Sent To')
    date_time = models.DateTimeField(verbose_name='Timestamp', auto_now_add=True)

    def __str__(self):
        return self.content



