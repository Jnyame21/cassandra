# Django
from django.db import IntegrityError, transaction
from django.core.files.storage import default_storage

# Document Manipulation
import pandas as pd
from openpyxl.styles import Font, Alignment, Protection
from openpyxl import Workbook, load_workbook

# Django Restframework
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from api.models import *
from api.serializer import *
from api.utils import *
import json
from collections import defaultdict
from datetime import datetime
import hashlib
import inflect
import math
from django.db.models import Prefetch
from decimal import Decimal
import time

# Other Roles
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_other_roles_data(request):
    other_roles = Staff.objects.select_related('school', 'current_role__level').get(user=request.user)
    school = other_roles.school
    # current_level = other_roles.current_role.level
    # current_term = int(request.GET.get('term'))
    # current_academic_year = AcademicYear.objects.get(id=int(request.GET.get('year')))
    staff = StaffSerializerTwo(Staff.objects.select_related('user').prefetch_related('departments', 'subjects', 'roles').filter(school=school), many=True).data
    
    return Response({
        'staff': staff,
    })
    
    