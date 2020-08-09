from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Patient)
admin.site.register(TestLocation)
admin.site.register(CovidScreening)
admin.site.register(Medication)
admin.site.register(AssignMed)
admin.site.register(AssignTreatment)
admin.site.register(Appointment)
admin.site.register(PeriodicReporting)

