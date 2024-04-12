from django.core.files import File
from api.models import *
from django.http import HttpResponse
from datetime import date
from django.utils import timezone
from api.serializer import *
import pandas as pd


# Other
def query(request):
    student = Student.objects.get()

    return HttpResponse('Operation success')
# # Student Objects Creation
# def query(request):
#     program = pd.read_excel('students.xlsx', sheet_name='2023_business')
#     students_data = program.values.tolist()
#     program = Program.objects.get(name='BUSINESS')
#     clas = Classe.objects.get(name='2023-BUSINESS')
#     academic_year_1 = AcademicYear.objects.get(name='2023-2024')
#
#     for st in students_data:
#         username = f"{st[0][0]}{st[1].lower()}{students_data.index(st) +1}"
#         if isinstance(st[2], str):
#             email = st[2]
#         else:
#             email = 'not set'
#
#         user = User.objects.create_user(
#             username=username,
#             password=username,
#             email=email,
#             first_name=st[0],
#             last_name=st[1],
#         )
#
#         user.save()
#
#         st_user = User.objects.get(username=username)
#
#         student = Student.objects.create(
#             user=st_user,
#             program=program,
#             st_class=clas,
#             current_year=1,
#             date_enrolled='2023-12-04',
#             graduation='2026-09-04',
#             st_id=st[3],
#             img=f'{username}.jpg',
#             gender=st[4],
#             dob=st[5],
#             contact=f"0{st[6]}",
#             address=st[7],
#             pob=st[8],
#             region=st[9],
#             nationality=st[10],
#         )
#         student.academic_years.add(academic_year_1)
#         student.save()
#         st_obj = Student.objects.get(st_id=st[3])
#         clas.students.add(st_obj)
#
#     return HttpResponse('Operation success')


# # Staff Objects Creation
# def query(request):
#     departments = pd.read_excel('staff.xlsx', sheet_name='arts')
#     staff_data = departments.values.tolist()
#     department = Department.objects.get(name='ARTS')
#
#     for staff in staff_data:
#         subject = Subject.objects.get(name=staff[11])
#         username = f"{staff[0][0]}{staff[1].lower()}{staff_data.index(staff) +1}"
#
#         user = User.objects.create_user(
#             username=username,
#             password=username,
#             email=staff[2] if isinstance(staff[2], str) else "not set",
#             first_name=staff[0],
#             last_name=staff[1],
#         )
#
#         user.save()
#
#         staff_user = User.objects.get(username=username)
#
#         stf = Staff.objects.create(
#             user=staff_user,
#             date_enrolled='2022-12-04',
#             staff_id=staff[3],
#             department=department,
#             gender=staff[4],
#             dob=staff[5],
#             contact=f"0{staff[6]}",
#             address=staff[7],
#             pob=staff[8],
#             region=staff[9],
#             nationality=staff[10],
#         )
#         stf.subjects.add(subject)
#         with open('staticfiles/img/students_img.jpg', 'rb') as f:  # read the image and save it to the image field
#             stf.img.save('students_img.jpg', f, save=True)
#         stf.save()
#         staff_obj = Staff.objects.get(staff_id=staff[3])
#         department.teachers.add(staff_obj)
#         department.save()
#
#     hod = Staff.objects.get(staff_id='50235431')
#     hod.role = "hod"
#     hod.save()
#     department.hod = hod
#     department.save()
#
#     return HttpResponse('Operation success')


# Head Objects Creation
# def query(request):
#     df = pd.read_excel('heads.xlsx', sheet_name='head')
#     head_data = df.values.tolist()
#
#     for item in head_data:
#         username = f"{item[0][0]}{item[1].lower()}{head_data.index(item) +1}"
#
#         user = User.objects.create_user(
#             username=username,
#             password=username,
#             email=item[2] if isinstance(item[2], str) else "not set",
#             first_name=item[0],
#             last_name=item[1],
#         )
#
#         user.save()
#
#         head_user = User.objects.get(username=username)
#
#         head = Head.objects.create(
#             user=head_user,
#             date_enrolled='2022-12-04',
#             head_id=item[3],
#             gender=item[4],
#             dob=item[5],
#             contact=f"0{item[6]}",
#             address=item[7],
#             pob=item[8],
#             region=item[9],
#             nationality=item[10],
#         )
#         with open('staticfiles/img/sch-logo.png', 'rb') as f:  # read the image and save it to the image field
#             head.img.save('sch-logo.png', f, save=True)
#         head.save()
#
#     return HttpResponse('Operation success')




