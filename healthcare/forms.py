from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import *
from django import forms

class DateInput(forms.DateInput):
    input_type = 'date'

class PatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'
        exclude = ['user']
        widgets = {'birth_date' : DateInput}



class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email','password1','password2']


class CovidScreeningForm(ModelForm):
    class Meta:
        model = CovidScreening
        fields = '__all__'
        exclude = ['patient']

class MedicationForm(ModelForm):
    class Meta:
        model = Medication
        fields = '__all__'

class TreatmentForm(ModelForm):
    class Meta:
        model = Treatment
        fields = '__all__'

class AssignMedForm(ModelForm):
    class Meta:
        model = AssignMed
        fields = '__all__'

class AssignTreatmentForm(ModelForm):
    class Meta:
        model = AssignTreatment
        fields = '__all__'

class ScheduleAppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'
        widgets = {'pick_Date' : DateInput, 'Description': forms.Textarea(attrs={
            "placeholder": "(Optional) Please add any additional comments if needed."})}

class PeriodicReportingForm(ModelForm):
    class Meta:
        model = PeriodicReporting
        fields = '__all__'
        widgets = {'date': DateInput}

