from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect


from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User

from django.core.exceptions import ObjectDoesNotExist
import requests, csv



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
    url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"
    response = requests.get(url)
    if response.status_code != 200:
        print('Failed to get data:', response.status_code)
    else:
        wrapper = csv.reader(response.text.strip().split('\n'))
        for row in wrapper:
            if row[1] == "Tarrant":
                tarrant_date = row[0]
                tarrant_confirmed = row[4]
                tarrant_death = row[5]


    if request.user.is_authenticated:
        current_user = request.user
        try:
            patient = Patient.objects.get(user = current_user)
        except ObjectDoesNotExist:
            patient = None

        context = {'user': current_user, 'patient': patient,'tarrant_date':tarrant_date,
                   'tarrant_confirmed':tarrant_confirmed,'tarrant_death':tarrant_death,
                   }
    else:
        context= {'tarrant_date':tarrant_date, 'tarrant_confirmed':tarrant_confirmed,'tarrant_death':tarrant_death,
                   }
    #     context = {'user': current_user, 'patient': patient,}
    # else:
    #     context = {}
    return render(request, 'healthcare/home.html', context )

def listPatient(request):
    patients = Patient.objects.all()

    context = {'patients': patients}

    return render(request, 'healthcare/listPatient.html', context)

def editPatient(request,pk):
    patient = Patient.objects.get(id = pk)
    patientMeds = patient.assignmed_set.all()
    patientTreatments = patient.assigntreatment_set.all()

    assignMedForm = AssignMedForm()
    assignTreatmentForm = AssignTreatmentForm()

    form = PatientForm(instance = patient)
    context = {'form': form, 'patient': patient, 'patientMeds':patientMeds, 'patientTreatments': patientTreatments,
                'assignMedForm':assignMedForm,'assignTreatmentForm':assignTreatmentForm }

    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request,'Patient profile updated')
            return HttpResponseRedirect(request.path_info)

    return render(request, 'healthcare/patientForm.html', context)


def assignMed(request):
    if request.method == 'POST':
        form = AssignMedForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Medication has been added to patient profile')
            return redirect('listPatient')
            # todo need to figure out routing
        else:
            messages.warning(request, 'Something went wrong!')

def assignTreatment(request):
    if request.method == 'POST':
        form = AssignTreatmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Treatment has been added to patient profile')
            return redirect('listPatient')
            # todo need to figure out routing
        else:
            messages.warning(request, 'Something went wrong!')


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
    medications = Medication.objects.all()

    if request.method == 'POST':
        form = MedicationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('medication')

    context = {'form': form, 'medications': medications}
    return render(request, 'healthcare/editMedication.html', context)

def editTreatement(request):
    form = TreatmentForm()
    treatments = Treatment.objects.all()

    if request.method == 'POST':
        form = TreatmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('treatment')

    context = {'form': form, 'treatments': treatments}
    return render(request, 'healthcare/editTreatment.htm', context)

def DeletePatient(request, pk):
    patient = Patient.objects.get(id=pk)
    context = {'patient' : patient}
    if request.method == "POST":
         patient.delete()
         return redirect('listPatient')
    return render(request, "healthcare/deletePatient.html", context)