
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


# Change Staff Role
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_staff_role(request):
    data = request.data
    staff = Staff.objects.select_related('school', 'current_role__level').get(user=request.user)
    school = staff.school
    if not AcademicYear.objects.filter(school=school, level=staff.current_role.level).exists():
        return Response(f"There are no academic year data for the level of your role '{staff.current_role.identifier.split('|')[1]} {staff.current_role.identifier.split('|')[0]}'. Contact your school administrator", status=400)
    
    role_identifier = data['newRoleIdentifier']
    new_role = StaffRole.objects.get(schools=school, identifier=role_identifier)
    staff.current_role = new_role
    staff.save()
    return Response(status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_student_level(request):
    student = Student.objects.select_related('current_level', 'current_program').prefetch_related('levels', 'programs').get(user=request.user)
    data = request.data
    new_current_level = student.levels.get(name=data['levelName'])
    new_current_program = student.programs.get(level=new_current_level)
    student.current_level = new_current_level
    student.current_program =  new_current_program
    student.save()
    
    return Response(status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reset_user_password(request):
    user = request.user
    user.set_password(request.data['password'])
    user.save()
    
    return Response(status=200)
    

# Staff Support
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def staff_support(request):
    problem = request.data['problem']
    staff = Staff.objects.select_related('user', 'school', 'current_role__level').get(user=request.user)
    subject = f"{staff.school.name} ({staff.current_role.level.name} {staff.current_role.name}) [ Name: {staff.title}. {staff.user.get_full_name()} ] [ Username: {staff.user.username} ]"
    try:
        send_mail(subject, problem, 'nyamejustice2000@gmail.com', ['nyamejustice2000@gmail.com'], fail_silently=False)
        return Response(status=200)

    except Exception:
        return Response(status=400)


# Students Support
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def students_support(request):
    problem = request.data['problem']
    student = Student.objects.select_related('user', 'school').get(user=request.user)
    subject = f"{student.school.name} (student) [ Name: {student.user.get_full_name()} ] [ Username: {student.user.username} ]"
    try:
        send_mail(subject, problem, 'nyamejustice2000@gmail.com', ['nyamejustice2000@gmail.com'], fail_silently=False)
        return Response(status=200)

    except Exception:
        return Response(status=400)
    
    
# goday email 'blacquetwist@gmail.com'

