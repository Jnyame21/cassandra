
# Django
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db import transaction
from django.core.mail import send_mail

# Django Restframework
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated

# Other
from api.models import *
from api.serializer import *
from email_validator import validate_email
from api.utils import get_current_academic_year
import json
import time

def root(request):
    return HttpResponse("<h1>Welcome to Cassandra, a school management system</h1>")
        

@api_view(['GET'])
def keep_server_running(request):
    return Response(status=200)


# LOGIN
class UserAuthSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        return token


class UserAuthView(TokenObtainPairView):
    serializer_class = UserAuthSerializer


# User Data
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_data(request):
    user = request.user
    user_data = {
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name
    }
    user_data['reset_password'] = True if user.password == user.username else False
    
    try:
        staff = Staff.objects.select_related('current_role__level', 'school').prefetch_related('roles', 'departments', 'subjects').get(user=user)
        if not staff.current_role:
            staff_role = staff.roles.all().first()
            if staff_role:
                staff.current_role = staff_role
                staff.save()
            else:
                return Response('You have no role in the school. Please contact your school administrator', status=401)
            
        staff_data = StaffSerializer(staff).data
        
        # Get the current academic year
        data = get_current_academic_year(staff.school, staff.current_role.level, user_data)
        if isinstance(data, str):
            return Response(data, status=401)
        
        user_data = data | staff_data
        user_data['role'] = 'staff'
        user_data['staff_role'] = staff.current_role.name.lower()
        
    except Staff.DoesNotExist:
        try:
            student = Student.objects.prefetch_related('levels').select_related('school', 'current_level', 'current_program', 'st_class').get(user=user)

            # Get current academic year
            data = get_current_academic_year(student.school, student.current_level, user_data)
            if isinstance(data, str):
                return Response(data, status=401)

            student_data = StudentSerializer(student).data
            user_data = user_data | student_data
            user_data['role'] = 'student'

        except Student.DoesNotExist:
            user_data['role'] = 'superuser'
        
    user_data['ms'] = 'LOGIN SUCCESSFUL'
    return Response(user_data, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_staff_role(request):
    data = request.data
    staff = Staff.objects.select_related('school', 'current_role__level').get(user=request.user)
    school = staff.school
    if not AcademicYear.objects.filter(school=school, level=staff.current_role.level).exists():
        return Response('There are no academic year data for the level of your role. Contact your school administrator', status=400)
    
    role_identifier = data['newRoleIdentifier']
    new_role = StaffRole.objects.get(schools=school, identifier=role_identifier)
    staff.current_role = new_role
    staff.save()
    return Response(status=200)
    
    
    
# # Notifications
# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
# def notification(request):
#     from_obj = None
#     from_obj_type = None
#     try:
#         from_obj = request.user.head
#         from_obj_type = 'head'
#     except User.head.RelatedObjectDoesNotExist:
#         try:
#             from_obj = request.user.staff
#             from_obj_type = 'staff'
#         except User.staff.RelatedObjectDoesNotExist:
#             try:
#                 from_obj = request.user.student
#                 from_obj_type = 'student'
#             except User.head.RelatedObjectDoesNotExist:
#                 return Response(status=401)
                
#     if request.method == 'POST':
#         data = request.data
#         if request.data['type'] == 'send':
#             receivers = json.loads(data['ids'])
#             to_obj = None
#             to_obj_type = None
#             with transaction.atomic():
#                 try:
#                     notification_obj = Notification.objects.create(
#                         content=data['content'],
#                         from_head=from_obj if from_obj_type == 'head' else None,
#                         from_staff=from_obj if from_obj_type == 'staff' else None,
#                         from_student=from_obj if from_obj_type == 'student' else None,
#                     )
#                     for receiver_id in receivers:
#                         try:
#                             to_obj = Staff.objects.get(school=from_obj.school, staff_id=receiver_id)
#                             to_obj_type = 'staff'
#                         except Exception as e:
#                             try:
#                                 to_obj = Student.objects.get(school=from_obj.school, st_id=receiver_id)
#                                 to_obj_type = 'student'
#                             except Exception as e:
#                                 transaction.set_rollback(True)
#                                 return Response(status=401)
                        
#                         if to_obj_type == 'staff':
#                             notification_obj.to_staff.add(to_obj)
#                         elif to_obj_type == 'student':
#                             notification_obj.to_student.add(to_obj)
                
#                     notification_obj.save()
                        
#                     return Response(status=200)

#                 except Exception as e:
#                     transaction.set_rollback(True)
#                     return Response(status=401)
                
#         elif data['type'] == 'getClassStudents':     
#             try:
#                 st_class = ClasseSerializer(Classe.objects.get(school=from_obj.school, name=data['className'])).data
#                 students = []
#                 for st in st_class['students']:
#                     students.append({'label': f"{st['user']['first_name']} {st['user']['last_name']}", 'st_id': st['st_id']})
                
#                 if from_obj_type == 'student': 
#                     students = [item for item in students if item['st_id'] != from_obj.st_id]
                    
#                 return Response(students)
            
#             except Exception as e:
#                 return Response(status=401)
            
#         elif data['type'] == 'delete':
#             notification_id = data['id']
#             try:
#                 notification_obj = Notification.objects.get(id=int(notification_id))
#                 notification_obj.delete()
#                 return Response(status=200)
            
#             except Exception as e:
#                 return Response(status=401)
    
#     elif request.method == 'GET':
#         notifications = []
#         notifications_sent = []
#         notifications_received = []
#         students_classes = []
#         staff = []
#         if from_obj_type == 'head':
#             notifications_sent = NotificationSerializer(Notification.objects.filter(from_head=from_obj), many=True).data
#             for item in notifications_sent:
#                 del notifications_sent[notifications_sent.index(item)]['from_head']
#         elif from_obj_type == 'staff':
#             notifications_sent = NotificationSerializer(Notification.objects.filter(from_staff=from_obj), many=True).data
#             for item in notifications_sent:
#                 del notifications_sent[notifications_sent.index(item)]['from_staff']
#             notifications_received = NotificationSerializer(Notification.objects.filter(to_staff=from_obj), many=True).data
#             for item in notifications_received:
#                 del notifications_received[notifications_received.index(item)]['to_staff']
#                 del notifications_received[notifications_received.index(item)]['to_student']
#         elif from_obj_type == 'student':
#             notifications_sent = NotificationSerializer(Notification.objects.filter(from_student=from_obj), many=True).data
#             for item in notifications_sent:
#                 del notifications_sent[notifications_sent.index(item)]['from_student']
#             notifications_received = NotificationSerializer(Notification.objects.filter(to_student=from_obj), many=True).data
#             for item in notifications_received:
#                 del notifications_received[notifications_received.index(item)]['to_staff']
#                 del notifications_received[notifications_received.index(item)]['to_student']
        
#         for item in notifications_sent:
#             notifications.append(item)
        
#         for item in notifications_received:
#             notifications.append(item)
        
#         notifications = sorted(notifications, key=lambda x: x['date_time'], reverse=True)
#         for item in notifications:
#             item['date_time'] = format_relative_date_time(item['date_time'], True, True)
        
#         if from_obj_type == 'staff':
#             all_staff = SpecificStaffSerializer(Staff.objects.filter(school=from_obj.school).exclude(staff_id=from_obj.staff_id), many=True).data
#         else:
#             all_staff = SpecificStaffSerializer(Staff.objects.filter(school=from_obj.school), many=True).data
#         all_classes = ClasseWithoutStudentsSerializer(Classe.objects.filter(school=from_obj.school), many=True).data
        
#         for item in all_staff:
#             staff.append({'label': f"{item['user']['first_name']} {item['user']['last_name']}", 'staff_id': item['staff_id']})
        
#         for item in all_classes:
#             students_classes.append({'label': f"{item['name']} FORM {item['students_year']}", 'value': item['name']})
            
#         return Response({'notifications': notifications, 'classes': students_classes, 'staff': staff}, status=200)


# OTHER
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_help(request):
    problem = request.data['problem']
    subject = ''
    try:
        student = Student.objects.select_related('user', 'school').get(user=request.user)
        subject = f"{student.school.name} (student) [ Name: {student.user.get_full_name()} ] [ Username: {student.user.username} ]"
    except Student.DoesNotExist:
        try:
            staff = Staff.objects.select_related('user', 'school', 'current_role__level').get(user=request.user)
            subject = f"{staff.school.name} ({staff.current_role.level.name} {staff.current_role.name}) [ Name: {staff.title}. {staff.user.get_full_name()} ] [ Username: {staff.user.username} ]"
        except Staff.DoesNotExist:
            return Response(status=400)
        
    try:
        send_mail(subject, problem, 'nyamejustice2000@gmail.com', ['nyamejustice2000@gmail.com'], fail_silently=False)
        return Response(status=200)

    except Exception:
        return Response(status=400)


# goday email 'blacquetwist@gmail.com'

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



