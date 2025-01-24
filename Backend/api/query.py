from django.core.files import File
from api.models import *
from django.http import HttpResponse
from datetime import date
from django.utils import timezone
from django.db import connection
from api.serializer import *
import pandas as pd


# Other
def query(request):
    
    return HttpResponse("Operation successful")


