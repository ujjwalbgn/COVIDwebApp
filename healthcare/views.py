from django.shortcuts import render , redirect
from django.http import HttpResponse

from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User



from .models import Patient
from .forms import *

# Create your views here.

def registerPage(request):

    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')


            messages.success(request,'Account was created for ' + username)

            return redirect('login')

    context= {'form': form}
    return render(request, 'healthcare/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username = username,password = password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request,'Username or Password is incorrect')

    content= {}
    return render(request, 'healthcare/login.html', content)

def logoutUser(request):
    logout(request)
    return redirect('login')

def home(request):
    return render(request, 'healthcare/home.html')

def editPateint(request,pk):
    patient = Patient.objects.get(id = pk)
    form = PatientForm(instance = patient)
    context = {'form': form, 'pateint': patient}

    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('/')

    return render(request, 'healthcare/patientForm.html', context)
