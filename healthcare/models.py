from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Patient(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other'),('NA', 'I do not wish to say')]

    user = models.OneToOneField(User, null=True,blank=True, on_delete=models.CASCADE)
    first_Name = models.CharField(max_length= 200, null= True)
    last_Name = models.CharField(max_length= 200, null= True)
    phone = models.CharField(max_length= 200, null= True)
    email = models.CharField(max_length=200, null= True)
    address = models.CharField(max_length=500, null= True)
    date_created = models.DateField(auto_now_add = True)

    birth_date = models.DateField(blank= True, null= True)
    age = models.DecimalField(decimal_places=0, max_digits=50, null=True)
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, blank= True)
    height = models.CharField(max_length=10, default='0.00 ft')
    weight = models.CharField(max_length=10, default='0.00 lbs')
    allergies = models.CharField(max_length=200, null=True)
    emergency_contact_name = models.CharField(max_length=200, null=True)
    emergency_contact_phone = models.CharField( max_length=200, null=True)
    emergency_contact_address = models.CharField(max_length=200, null=True)
    insurance_provider = models.CharField(max_length=200, null=True)

    def __str__(self):
        if (self.first_Name and self.last_Name):
            display = (self.first_Name + " " + self.last_Name)
        else:
            display = str(self.date_created)

        return display

class TestLocation(models.Model):
    name = models.CharField(max_length=200, null=False)
    address = models.CharField(max_length=500, null=True)
    phone_number = models.CharField(max_length= 200, null= True)

    def __str__(self):
        return self.name


class CovidScreening(models.Model):
    BOOL_CHOICES = [('Y', 'Yes'), ('N', 'No')]
    OPT_CHOICES = [('Y', 'Yes'), ('N', 'No'),('NA', 'I do not know')]

    patient = models.OneToOneField(Patient, null=True,blank=True, on_delete=models.CASCADE)
    age = models.DecimalField(decimal_places=0, max_digits=50, null=True)
    fever_above_100_F = models.CharField(max_length=2, choices=BOOL_CHOICES,null=True)
    cough = models.CharField(max_length=2, choices=BOOL_CHOICES,null=True)
    shortness_of_breath_or_difficulty_breathing = models.CharField(max_length=2, choices=BOOL_CHOICES,null=True)
    sustained_loss_of_smell_or_taste = models.CharField(max_length=2, choices=BOOL_CHOICES,null=True)
    body_aches = models.CharField(max_length=2, choices=BOOL_CHOICES,null=True)
    vomiting_or_diarrhoea = models.CharField(max_length=2, choices=BOOL_CHOICES, null=True)
    have_you_been_in_contact_with_COVID19_patient = models.CharField(max_length=2, choices=OPT_CHOICES, null=True)
    have_you_been_to_any_COVID_affected_regions = models.CharField(max_length=2, choices=OPT_CHOICES, null=True)

    def __str__(self):
        if (self.patient.first_Name and self.patient.last_Name):
            display = (self.patient.first_Name + " " + self.patient.last_Name)
        else:
            display = str(self.id)
        return display


class Medication(models.Model):
    name =  models.CharField(max_length= 200, null= True)
    description =  models.TextField()

    def __str__(self):
        return self.name

class Treatment(models.Model):
    name = models.CharField(max_length= 200, null= True)
    description = models.TextField()

    def __str__(self):
        return self.name

class AssignMed(models.Model):
      patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
      medication = models.ForeignKey(Medication,on_delete=models.CASCADE)

      class Meta:
          ordering = ['medication']

      def __str__(self):
          return self.medication.name


class AssignTreatment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE)

    class Meta:
        ordering = ['treatment']

    def __str__(self):
        return self.treatment.name

