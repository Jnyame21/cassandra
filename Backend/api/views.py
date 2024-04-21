# Django
import json
import os
import random

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db import IntegrityError, transaction
from django.db.utils import IntegrityError as IntergrityError_unique_constraint
from django.core.files.storage import default_storage
from django.core.exceptions import SuspiciousOperation
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

# Django Restframework
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated

# Other
from api.models import *
from api.serializer import *
from datetime import datetime, date
import io
from pprint import pprint
import pytz
from dateutil import parser
from api.utils import *


def root(request):
    # user = User.objects.get(username='Eone739')
    # user.set_password('Eone739')
    # user.save()
        
    
    return HttpResponse("<h1>Yeah process successfull</h1>")
    # return HttpResponse("<h1>EduAAP</h1>")


# LOGIN
class UserAuthSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        user_data = UserSerializer(user).data
        try:
            staff = user.staff
            staff_data = SpecificStaffSerializer(staff).data
            if staff_data['contact'] and staff_data['contact'] != 'not set':
                token['reset'] = False
            else:
                token['reset'] = True

            return token

        except User.staff.RelatedObjectDoesNotExist:
            try:
                student = user.student
                if user_data['last_login']:
                    token['last_login'] = 'yes'

                return token

            except User.student.RelatedObjectDoesNotExist:
                try:
                    head = user.head
                    head_data = SpecificHeadSerializer(head).data
                    if head_data['contact'] != 'not set':
                        token['reset'] = False
                    else:
                        token['reset'] = True

                    return token

                except User.head.RelatedObjectDoesNotExist:
                    return token


class UserAuthView(TokenObtainPairView):
    serializer_class = UserAuthSerializer


# User Data
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_user_data(request):
    user = request.user
    user_info = UserSerializer(user).data

    if request.method == 'POST':
        data = request.data

        if len(data['contact']) != 10:
            return Response({'ms': 'The contact must be a 10 digit number'}, status=201)

        elif data['contact'][0] != '0' or data['altContact'] and data['altContact'] != 'null' and data['altContact'][0] != '0':
            return Response({'ms': 'The phone numbers must start with a 0'}, status=201)

        elif data['altContact'] and data['altContact'] != 'null' and len(data['altContact']) != 10:
            return Response({'ms': 'The second phone number must be a 10 digit number'}, status=201)

        try:
            staff = user.staff
            with transaction.atomic():
                user.set_password(data['password'])
                user.email = data['email'] if data['email'] and data['email'] != 'null' else 'not set'
                user.save()
                staff.contact = data['contact']
                staff.alt_contact = data['altContact'] if data['altContact'] and data['altContact'] != 'null' else 'not set'
                staff.save()

            return Response(status=200)

        except User.staff.RelatedObjectDoesNotExist:
            try:
                head = user.head
                with transaction.atomic():
                    user.set_password(data['password'])
                    user.email = data['email'].strip() if data['email'] and data['email'] != 'null' else 'not set'
                    user.save()
                    head.contact = data['contact']
                    head.alt_contact = data['altContact'] if data['altContact'] and data['altContact'] != 'null' else 'not set'
                    head.save()

                return Response(status=200)

            except User.head.RelatedObjectDoesNotExist:
                return Response(status=401)

    else:
        user_data = {
            'username': user_info['username'],
            'first_name': user_info['first_name'],
            'last_name': user_info['last_name']
        }
        if user_info['email']:
            user_data['email'] = user_info['email']
        else:
            user_data['email'] = 'null'

        try:
            staff = user.staff
            # Get current academic year
            get_current_academic_year(staff, user_data)

            staff_data = StaffSerializer(staff).data
            user_data['last_login'] = format_relative_date_time(staff_data['user']['last_login'], False, True)
            user_data['role'] = 'staff'
            user_data['img'] = staff_data['img']
            user_data['school'] = staff_data['school']
            user_data['staff_id'] = staff_data['staff_id']
            try:
                department = Department.objects.get(teachers=staff)
                user_data['department'] = DepartmentNameSerializer(department).data['name']
                if department.hod == staff:
                    user_data['staff_role'] = 'hod'
                    staff.role = 'hod'
                    staff.save()
                else:
                    user_data['staff_role'] = 'teacher'

            except Department.DoesNotExist:
                user_data['staff_role'] = staff_data['role']

            user_data['subjects'] = staff_data['subjects']
            user_data['gender'] = staff_data['gender']
            user_data['dob'] = staff_data['dob']
            user_data['address'] = staff_data['address']
            user_data['contact'] = staff_data['contact']
            user_data['ms'] = 'Login successful'
            user_data['pob'] = staff_data['pob']
            user_data['region'] = staff_data['region']
            user_data['nationality'] = staff_data['nationality']

            return Response(user_data)

        except User.staff.RelatedObjectDoesNotExist:
            try:
                student = user.student

                # Get current academic year
                get_current_academic_year(student, user_data)

                student_data = StudentSerializer(student).data
                user_data['last_login'] = format_relative_date_time(student_data['user']['last_login'], False, True)
                user_data['role'] = 'student'

                user_data['img'] = student_data['img']
                user_data['ms'] = 'Login successful'
                user_data['program'] = student_data['program']['name']
                user_data['school'] = student_data['school']
                user_data['st_id'] = student_data['st_id']

                if student_data['index_no']:
                    user_data['index_no'] = student_data['index_no']
                else:
                    user_data['index_no'] = 'not assigned yet'

                try:
                    clas = Classe.objects.get(school=student.school, students=student)
                    class_name = ClasseWithoutStudentsSerializer(clas).data
                    user_data['st_class'] = class_name['name']
                    
                    if student_data['has_completed'] or student.current_year == 4:
                        user_data['current_yr'] = 'COMPLETED'
                    else:
                        user_data['current_yr'] = student_data['current_year']

                except Classe.DoesNotExist:
                    pass

                user_data['contact'] = student_data['contact']
                user_data['dob'] = student_data['dob']
                user_data['gender'] = student_data['gender']
                user_data['pob'] = student_data['pob']
                user_data['region'] = student_data['region']
                user_data['address'] = student_data['address']
                user_data['religion'] = student_data['religion']
                user_data['nationality'] = student_data['nationality']
                user_data['guardian'] = student_data['guardian']
                user_data['guardian_gender'] = student_data['guardian_gender']
                user_data['guardian_occupation'] = student_data['guardian_occupation']
                user_data['guardian_nationality'] = student_data['guardian_nationality']

                if student_data['guardian_email']:
                    user_data['guardian_email'] = student_data['guardian_email']
                else:
                    user_data['guardian_email'] = 'null'

                user_data['guardian_contact'] = student_data['guardian_contact']
                user_data['guardian_address'] = student_data['guardian_address']

                return Response(user_data)

            except User.student.RelatedObjectDoesNotExist:
                head = user.head
                # Get current academic year
                get_current_academic_year(head, user_data)

                head_data = HeadSerializer(head).data
                user_data['last_login'] = format_relative_date_time(head_data['user']['last_login'], False, True)
                user_data['role'] = 'head'

                user_data['img'] = head_data['img']
                user_data['school'] = head_data['school']
                user_data['head_id'] = head_data['head_id']
                user_data['head_role'] = head_data['role']
                user_data['gender'] = head_data['gender']
                user_data['dob'] = head_data['dob']
                user_data['address'] = head_data['address']
                user_data['contact'] = head_data['contact']
                user_data['ms'] = 'Login successful'
                user_data['pob'] = head_data['pob']
                user_data['region'] = head_data['region']
                user_data['nationality'] = head_data['nationality']

                return Response(user_data)


# Messages
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def staff_notification(request):
    if request.method == 'POST' and request.data['type'] == 'send':
        try:
            sender = request.user.staff
            staff_ids = json.loads(request.POST.get('staff_ids'))
            if staff_ids and len(staff_ids) > 0:
                staff_message_instance = StaffNotification.objects.create(
                    content=request.data['message'],
                    sent_by_hod=sender
                )
                for staff_id in staff_ids:
                    send_to = Staff.objects.get(school=sender.school, staff_id=staff_id)
                    staff_message_instance.send_to.add(send_to)

                staff_message_instance.save()

                messages = get_staff_messages(request.user)

                return Response(messages)
            else:
                return Response(status=401)

        except User.staff.RelatedObjectDoesNotExist:
            sender = request.user.head
            staff_ids = json.loads(request.POST.get('staff_ids'))
            if staff_ids and len(staff_ids) > 0:
                head_message_instance = StaffNotification.objects.create(
                    content=request.data['message'],
                    sent_by_head=sender
                )
                for stf_id in staff_ids:
                    send_to = Staff.objects.get(school=sender.school, staff_id=stf_id)
                    head_message_instance.send_to.add(send_to)

                head_message_instance.save()

                messages = get_staff_messages(request.user)

                return Response(messages)
            else:
                return Response(status=401)

    elif request.method == 'POST' and request.data['type'] == 'delete':
        message_id = int(request.data['id'])
        try:
            hod = request.user.staff
            hod_messages = get_object_or_404(StaffNotification, sent_by_hod=hod, id=message_id)
            if hod_messages:
                hod_messages.delete()

            messages = get_staff_messages(request.user)

            return Response(messages)

        except User.staff.RelatedObjectDoesNotExist:
            head = request.user.head
            head_messages = get_object_or_404(StaffNotification, sent_by_head=head, id=message_id)
            if head_messages:
                head_messages.delete()

            messages = get_staff_messages(request.user)

            return Response(messages)

    else:
        try:
            head = request.user.head
            head_staff_data = []
            staff = SpecificStaffSerializer(Staff.objects.filter(school=head.school), many=True).data
            for stf in staff:
                head_staff_data.append({
                    'name': f"{stf['user']['first_name']} {stf['user']['last_name']}",
                    'staff_id': stf['staff_id']
                })

            messages = get_staff_messages(request.user)

            return Response({'messages': messages, 'head_staff_data': head_staff_data})

        except User.head.RelatedObjectDoesNotExist:
            messages = get_staff_messages(request.user)

            return Response(messages)


# OTHER
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_help(request):
    problem = request.data['problem']
    subject = f"School System"
    try:
        student = request.user.student
        st = StudentSerializer(student).data
        subject = f"{st['school']['name']} (student) [ Name: {st['user']['first_name']} {st['user']['last_name']} Username: {st['user']['username']} ]"
    except User.student.RelatedObjectDoesNotExist:
        try:
            staff = request.user.staff
            stf = StaffSerializer(staff).data
            subject = f"{stf['school']['name']} ({stf['role']}) [ Name: {stf['user']['first_name']} {stf['user']['last_name']} Username: {stf['user']['username']} ]"
        except User.staff.RelatedObjectDoesNotExist:
            head = request.user.head
            hd = HeadSerializer(head).data
            subject = f"{hd['school']['name']} ({hd['role']}) [ Name: {hd['user']['first_name']} {hd['user']['last_name']} Username: {hd['user']['username']}]"

    try:
        send_mail(subject, problem, 'nyamejustice2000@gmail.com', ['nyamejustice2000@gmail.com'], fail_silently=False)
        return Response(status=200)

    except Exception as e:
        return Response(status=401)


# class StudentsView(ListAPIView):
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer
#

# class StaffView(ListAPIView):
#     queryset = Staff.objects.all()
#     serializer_class = StaffSerializer

#
# class ClasseView(ListAPIView):
#     queryset = Classe.objects.all()
#     serializer_class = ClasseSerializer
#
#
# class SubjectAssignmentView(ListAPIView):
#     queryset = SubjectAssignment.objects.all()
#     serializer_class = SubjectAssignmentSerializer
#
#



