from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include 

from api.student import get_student_data, student_transcript
from api.teacher import get_teacher_data, teacher_assessments, teacher_exams, teacher_students_results, teacher_students_attendance
from api.views import UserAuthView, keep_server_running, root, user_help, get_user_data, change_staff_role
from api.superuser import *
from api.school_admin import *
from api.hod import *
from api.query import query


urlpatterns = [
    path('', root, name='root'),
    path('start_up', keep_server_running),

    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Token refresh
    path('support', user_help),  # Support/Help
    path('user/data', get_user_data),
    path('staff/change-role', change_staff_role),
    # path('notification', notification),
    
    # Superuser
    path('superuser/data', get_superuser_data),
    path('superuser/schools', superuser_schools),
    path('superuser/levels', superuser_levels),
    path('superuser/subjects', superuser_subjects),
    path('superuser/programs', superuser_programs),
    path('superuser/departments', superuser_departments),
    path('superuser/grading_system_ranges', superuser_grading_system_ranges),
    path('superuser/grading_systems', superuser_grading_systems),
    path('superuser/classes', superuser_classes),
    path('superuser/academic_years', superuser_academic_years),
    path('superuser/staff_roles', superuser_staff_roles),
    path('superuser/staff', superuser_staff),
    
    # Student
    path('login', UserAuthView.as_view(), name='token_obtain_pair'),  # Student token obtain
    path('student/data', get_student_data),   # Student data
    path('student/transcript', student_transcript),  # Student transcript
    
    # Teacher
    path('teacher/data', get_teacher_data),
    path('teacher/assessments', teacher_assessments),
    path('teacher/exams', teacher_exams),
    path('teacher/students-result', teacher_students_results),
    path('teacher/students/attendance', teacher_students_attendance),
    
    # HOD
    # path('hod/students_performance', hod_students_performance),
    path('hod/subject-assignment', hod_subject_assignment),

    # Head
    # path('head/data', get_head_data),
    # path('head/students_performance', head_students_performance),

    # School Administrator
    path('school-admin/data', school_admin_data),
    path('school-admin/academic_years', school_admin_academic_years),
    path('school-admin/students', school_admin_students),
    path('school-admin/staff', school_admin_staff),
    path('school-admin/subject-assignment', school_admin_subject_assignment),
    path('school-admin/released_results', release_results),
    path('query', query),
]

if settings.DEBUG:
    urlpatterns += path('silk/', include('silk.urls', namespace='silk')),
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)




