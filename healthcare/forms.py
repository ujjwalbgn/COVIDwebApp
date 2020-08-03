from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Patient
from django import forms

class DateInput(forms.DateInput):
    input_type = 'date'

class PatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'
        exclude= ['user']
        widgets = {'birth_date' : DateInput}



class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email','password1','password2']


# class testLocationForm(ModelForm):
#     class Meta:
#         model = testLocation
#         fields = [
#             'name',
#             'address',
#             'phone_number',
#             'email',
#             'website'
#         ]