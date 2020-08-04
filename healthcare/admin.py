from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Patient)
admin.site.register(TestLocation)
admin.site.register(CovidScreening)