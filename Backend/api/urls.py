from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt.views import TokenRefreshView
from api.views import *
from api.query import *


urlpatterns = [
    
    path('', root, name='root'),
    path('file/', FileView.as_view()),
    path('refresh/data', refresh_data),
    
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Token refresh
    path('support', user_help),  # Support/Help
    
    # Student
    path('login', UserAuthView.as_view(), name='token_obtain_pair'),  # Student token obtain
    path('st/data', get_student_data),   # Student data
    path('st/transcript', student_transcript),  # Student transcript
    
    # Staff
    path('teacher/subject_assignments/', get_teacher_subject_assignments),
    path('teacher/results/upload/', teacher_student_results),
    path('hod/data', hod_data),
    path('staff/notification', staff_notification),
    path('hod/students_performance', hod_students_performance),

    # Head
    path('head/data', head_data),
    path('head/students_performance', head_students_performance),

    # Admin
    path('sch-admin/data', get_sch_admin_data),
    path('sch-admin/students', admin_students),
    path('sch-admin/staff', admin_staff),


    # Testing paths
    # path('query/', query),

]



