from django.core.files import File
from api.models import *
from django.http import HttpResponse
from datetime import date
from django.utils import timezone
from api.serializer import *
import pandas as pd


# Other
def query(request):
    student = Student.objects.get(id=5)
    print(StudentSerializer(student))
    

    return HttpResponse('Operation success')







