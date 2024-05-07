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

    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Token refresh
    path('support', user_help),  # Support/Help
    path('user/data', get_user_data),
    path('notification', notification),
    
    # Student
    path('login', UserAuthView.as_view(), name='token_obtain_pair'),  # Student token obtain
    path('st/data', get_student_data),   # Student data
    path('st/transcript', student_transcript),  # Student transcript
    
    # Staff
    path('teacher/subject_assignments/', get_teacher_subject_assignments),
    path('teacher/results/upload/', teacher_student_results),
    path('hod/data', get_hod_data),
    path('hod/students_performance', hod_students_performance),
    path('teacher/students/attendance', teacher_students_attendance),

    # Head
    path('head/data', get_head_data),
    path('head/students_performance', head_students_performance),

    # Admin
    path('sch-admin/data', get_sch_admin_data),
    path('sch-admin/students', admin_students),
    path('sch-admin/staff', admin_staff),
    path('sch-admin/head', admin_head),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# 202260301
# 202260302
# 202250603
# 202260304
# 202260305
# 202260306
# 202260307
# 202260308
# 202260309
# 202260310
# 202260311
# 202260312
# 202260313
# 202260314
# 202260315
# 202260316
# 202260317
# 202260318
# 202260319
# 202260320
# 202260321
# 202260322
# 202260323
# 202260324
# 202260325
# 202260326
# 202260327
# 202260328
# 202260329
# 202260330
# 202260331
# 202260332
# 202260333
# 202260334
# 202260335
# 202260336
# 202260337
# 202260338
# 202260339
# 202260340
# 202260341
# 202260342
# 202260343
# 202260344
# 202260345
# 202260346
# 202260347
# 202260348
# 202260349
# 202260350
# 202260351
# 202260352
# 202260353
# 202260353
# 202260354
# 202260355
# 202260356
# 202260357
# 202260358
# 202260359
# 202260360
# 202260361







