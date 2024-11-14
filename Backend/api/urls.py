from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt.views import TokenRefreshView
from api.students import *
from api.head import *
from api.teachers import *
from api.school_admin import *
from api.views import *
from api.query import *


urlpatterns = [
    path('', root, name='root'),
    path('start_up', keep_server_running),

    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Token refresh
    path('support', user_help),  # Support/Help
    path('user/data', get_user_data),
    path('notification', notification),
    
    # Student
    path('login', UserAuthView.as_view(), name='token_obtain_pair'),  # Student token obtain
    path('st/data', get_student_data),   # Student data
    path('st/transcript', student_transcript),  # Student transcript
    
    # Staff
    path('teacher/data', get_teacher_data),
    path('teacher/assessments', teacher_assessments),
    path('teacher/exams', teacher_exams),
    path('teacher/students-result', teacher_students_results),
    path('hod/data', hod_data),
    path('hod/students_performance', hod_students_performance),
    path('teacher/students/attendance', teacher_students_attendance),

    # Head
    path('head/data', get_head_data),
    path('head/students_performance', head_students_performance),

    # Admin
    path('school-admin/data', school_admin_data),
    path('school-admin/academic_years', school_admin_academic_years),
    path('school-admin/linked-class', school_admin_linked_class),
    path('school-admin/students', admin_students),
    path('school-admin/staff', admin_staff),
    
    path('query', query),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



