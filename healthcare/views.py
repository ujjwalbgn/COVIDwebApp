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

from .decorators import unauthenticated_user, allowed_users, staff_only


from .models import *
from .forms import *


# Create your views here.
@unauthenticated_user
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

@unauthenticated_user
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
            if row[1] == "Dallas":
                dallas_confirmed = row[4]
                dallas_death = row[5]
            if row[1] == "Collin":
                collin_confirmed = row[4]
                collin_death = row[5]
            if row[1] == "Johnson":
                johnson_confirmed = row[4]
                johnson_death = row[5]
            if row[1] == "Denton":
                denton_confirmed = row[4]
                denton_death = row[5]
            if row[1] == "Parker":
                parker_confirmed = row[4]
                parker_death = row[5]
            if row[1] == "Johnson":
                johnson_confirmed = row[4]
                johnson_death = row[5]


    if request.user.is_authenticated:
        current_user = request.user
        try:
            patient = Patient.objects.get(user = current_user)
        except ObjectDoesNotExist:
            patient = None

        context = {'user': current_user, 'patient': patient,'date':tarrant_date,
                   'tarrant_confirmed':tarrant_confirmed,'tarrant_death':tarrant_death,
                   'dallas_confirmed':dallas_confirmed,'dallas_death':dallas_death,
                   'denton_confirmed':denton_confirmed,'denton_death':denton_death,
                   'parker_confirmed':parker_confirmed,'parker_death':parker_death,
                   'johnson_confirmed': johnson_confirmed, 'johnson_death':johnson_death,
                   'collin_confirmed':collin_confirmed, 'collin_death':collin_death,
                   }
    else:
        context= {'tarrant_date':tarrant_date, 'tarrant_confirmed':tarrant_confirmed,'tarrant_death':tarrant_death,
                  'dallas_confirmed':dallas_confirmed,'dallas_death':dallas_death,
                  'denton_confirmed':denton_confirmed,'denton_death':denton_death,
                  'parker_confirmed':parker_confirmed,'parker_death':parker_death,
                  'johnson_confirmed': johnson_confirmed, 'johnson_death':johnson_death,
                  'collin_confirmed':collin_confirmed, 'collin_death':collin_death}

    return render(request, 'healthcare/home.html', context )

# @allowed_users(allowed_roles=['staff'])
@staff_only
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

@staff_only
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

@staff_only
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


def covidEmergencyChech(request):
    if request.user.is_authenticated:
        current_user = request.user
        try:
            patient = Patient.objects.get(user=current_user)
        except ObjectDoesNotExist:
            # print("Unable to find patient ID")
            patient = None
        context = { 'patient': patient}
    else:
        context = {}
    return render(request, 'healthcare/covidEmergencyChech.html', context)


def covidScreening(request):

    form = CovidScreeningForm()
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
    if request.method == 'POST':
        form = CovidScreeningForm(request.POST)
        if form.is_valid():

            closeContactWithCovid19Patient = form.cleaned_data['have_you_been_in_contact_with_COVID19_patient']
            counter = 0
            if (closeContactWithCovid19Patient == 'Yes'):
                messages.info(request, 'According to the data you provided, we recommend COVID testing')
                return redirect('testLocation')
            for field in form.fields:
                userInput = form.cleaned_data[field]
                if(userInput == 'Yes'):
                    counter = counter + 1
            if(counter >= 2):
                messages.info(request, 'According to the data you provided, we recommend COVID testing')
                return redirect('testLocation')
            else:
                # messages.info(request, 'You are under low risk. ')
                return render(request, 'healthcare/noCovid.html', context)


    return render(request, 'healthcare/covidScreening.html', context)

@staff_only
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

@staff_only
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

@staff_only
def DeletePatient(request, pk):
    patient = Patient.objects.get(id=pk)
    context = {'patient' : patient}
    if request.method == "POST":
        patient.delete()
        return redirect('listPatient')
    return render(request, "healthcare/deletePatient.html", context)

def call911(request):
    return render(request, "healthcare/call911.html")

def Covidnegative(request):
    return render(request, "healthcare/noCovid.html")

@login_required(login_url='login')
# @allowed_users(allowed_roles=['patient'])
def ScheduleAppointment(request):
    form = ScheduleAppointmentForm()
    appointments = Appointment.objects.all()

    current_user = request.user
    try:
        patient = Patient.objects.get(user=current_user)
    except ObjectDoesNotExist:
        patient = None

    if request.method == 'POST':
        form = ScheduleAppointmentForm(request.POST)
        if form.is_valid():
            stock = form.save(commit=False)
            stock.patient = patient
            stock.save()
            messages.success(request, 'Request for appointment approval has been submitted successfully')
            return redirect('scheduleAppointment')


    context = {'form': form, 'appointments': appointments,'patient':patient,
               }
    return render(request, 'healthcare/ScheduleAppointment.html', context)

@staff_only
def DeleteMedication(request, pk):
    medication = Medication.objects.get(id=pk)
    context = {'medication' : medication}
    if request.method == "POST":
        medication.delete()
        return redirect('medication')
    return render(request, "healthcare/deleteMedication.html", context)

@staff_only
def DeleteTreatment(request, pk):
    treatment = Treatment.objects.get(id=pk)
    context = {'treatment' : treatment}
    if request.method == "POST":
        treatment.delete()
        return redirect('treatment')
    return render(request, "healthcare/deleteTreatment.html", context)

@login_required(login_url='login')
def ReportSymptoms(request):
    form = PeriodicReportingForm()

    if request.user.is_authenticated:
        current_user = request.user
        try:
            patient = Patient.objects.get(user=current_user)
        except ObjectDoesNotExist:
            print("Unable to find patient ID")
            patient = None
    context = {'form': form, 'patient': patient}


    if request.method == 'POST':
        counter = 0
        form = PeriodicReportingForm(request.POST)
        if form.is_valid():
            for field in form.fields:
                userInput = form.cleaned_data[field]
                if(userInput == 'Yes'):
                    counter = counter + 1
            if(counter >= 2):
                stock = form.save(commit=False)
                stock.patient = patient
                stock.flag = 'Yes'
                stock.save()
                messages.info(request, 'Your information is recorded. According to the data you provided, we recommend contacting Healthcare Professionals')
                return redirect('home')
            else:
                stock = form.save(commit=False)
                stock.patient = patient
                stock.flag = 'No'
                stock.save()
                messages.info(request, 'Your information is recorded. ')
                return redirect('home')

        else:
            messages.warning(request, 'Your previous report is being reviewed. '
                                      'Please submit new report later.')


    return render(request, 'healthcare/symptomsReporting.html', context)


@login_required(login_url='login')
def ContactTracingView(request):
    form = ContactTracingForm()

    if request.user.is_authenticated:
        current_user = request.user
        try:
            patient = Patient.objects.get(user=current_user)
        except ObjectDoesNotExist:
            print("Unable to find patient ID")
            patient = None

    if request.method == 'POST':
        form = ContactTracingForm(request.POST)
        if form.is_valid():
            stock = form.save(commit=False)
            stock.patient = patient
            stock.save()

            messages.success(request, 'Thank you for submitting Contact Tracing Form. We appreciate you support during this Pandemic')
            return redirect('home')
        else:
            messages.warning(request, 'Something wnt wrong')

    context = {'form': form, 'patient': patient}
    return render(request, 'healthcare/symptomsReporting.html', context)

@staff_only
def listAllCovidTracing(request):

    contactrracings = ContactTracing.objects.all()
    context = {'contacts': contactrracings}
    return render(request, 'healthcare/listContactTracing.html', context)


@staff_only
def viewCovidTracing(request, pk):

    contactrracing = ContactTracing.objects.get(id = pk)
    form = ContactTracingForm(instance=contactrracing)
    context = {'form': form}
    return render(request, 'healthcare/viewContactTracing.html', context)

@staff_only
def deleteCovidTracing(request, pk):
    contact = ContactTracing.objects.get(id=pk)
    context = {'contact': contact}
    if request.method == "POST":
        contact.delete()
        return redirect('listCovidTracing')
    return render(request, "healthcare/deleteCovidTracing.html", context)

@staff_only
def reviewReportings(request):
    reportings = PeriodicReporting.objects.all()

    context = {'reportings': reportings}

    return render(request, 'healthcare/listReportings.html', context)


@staff_only
def viewReportReviewStatus(request, pk):
    form = PeriodicReportingForm()
    reportings = PeriodicReporting.objects.get(id=pk)
    context = {'reportings': reportings, 'form': form}
    return render(request, 'healthcare/viewReportings.html', context)

@staff_only
def deleteSymptomsReport(request, pk):
    reportings = PeriodicReporting.objects.get(id=pk)
    context = {'reportings': reportings}
    if request.method == "POST":
        reportings.delete()
        return redirect('reviewreportings')
    return render(request, "healthcare/deleteSymptomsReport.html", context)


@staff_only
def deleteAppointment(request, pk):
    appointments = Appointment.objects.get(id=pk)
    context = {'appointments': appointments}

    if request.method == "POST":
        appointments.delete()
        return redirect('scheduleAppointment')
    return render(request, "healthcare/deleteAppointment.html", context)