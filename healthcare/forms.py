from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User
from .models import Patient

class PatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'
        exclude= ['user']


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email','password1','password2']