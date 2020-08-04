from django.shortcuts import render , redirect
from django.http import HttpResponse

from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User

from django.core.exceptions import ObjectDoesNotExist



from .models import *
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
                messages.warning(request,'Username or Password is incorrect')

    content= {}
    return render(request, 'healthcare/login.html', content)

def logoutUser(request):
    logout(request)
    return redirect('login')

def home(request):
    if request.user.is_authenticated:
        current_user = request.user
        try:
            patient = Patient.objects.get(user = current_user)
        except ObjectDoesNotExist:
            patient = None

        context = {'user': current_user, 'patient': patient}
    else:
        context= {}
    return render(request, 'healthcare/home.html', context )




def editPateint(request,pk):
    patient = Patient.objects.get(id = pk)
    form = PatientForm(instance = patient)
    context = {'form': form, 'patient': patient}

    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('/')

    return render(request, 'healthcare/patientForm.html', context)


def testLocation(request):
    testLocations = TestLocation.objects.all()

    if request.user.is_authenticated:
        current_user = request.user
        try:
            patient = Patient.objects.get(user=current_user)
        except ObjectDoesNotExist:
            patient = None
        context = {'testLocations': testLocations, 'patient': patient}
    else:
        context = {'testLocations': testLocations}


    return render(request, 'healthcare/testLocationForm.html', context)



def covidScreening(request):

    form = CovidScreeningForm()
    if request.method == 'POST':
        form = CovidScreeningForm(request.POST)
        if form.is_valid():

            # todo save to existing patient

            closeContactWithCovid19Patient = form.cleaned_data['have_you_been_in_contact_with_COVID19_patient_or_one_who_had_close_contact_with_Covid19_patient']
            counter = 0
            if (closeContactWithCovid19Patient == 'Y'):
                messages.info(request, 'According to the data you provided, we recommend COVID testing')
                return redirect('testLocation')
            for field in form.fields:
                userInput = form.cleaned_data[field]
                if(userInput == 'Y'):
                    counter = counter + 1
            if(counter >= 2):
                messages.info(request, 'According to the data you provided, we recommend COVID testing')
                return redirect('testLocation')


    if request.user.is_authenticated:
        current_user = request.user
        try:
            patient = Patient.objects.get(user=current_user)
        except ObjectDoesNotExist:
            # print("Unable to find patient ID")
            patient = None
        context = {'form': form, 'patient': patient}
    else:
        context = {'form': form}
    return render(request, 'healthcare/covidScreening.html', context)


def editMedication(request):
    form = MedicationForm()
    context = {'form': form}
    if request.method == 'POST':
        form = CovidScreeningForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    return render(request, 'healthcare/editMedication.html', context)



