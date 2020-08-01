from django.shortcuts import render , redirect
from django.http import HttpResponse

from .models import Patient
from .forms import *
# Create your views here.


def home(request):
    return render(request, 'healthcare/home.html')

def editPateint(request,pk):
    patient = Patient.objects.get(pk)
    form = PatientForm(instance = patient)
    context = {'form': form}

    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('/')

    return render(request, 'healthcare/patientForm.html', context)
