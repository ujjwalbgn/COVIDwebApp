from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Patient(models.Model):
    user = models.OneToOneField(User, null=True,blank=True, on_delete=models.CASCADE)
    first_Name = models.CharField(max_length= 200, null= True)
    last_Name = models.CharField(max_length= 200, null= True)
    phone = models.CharField(max_length= 200, null= True)
    email = models.CharField(max_length=200, null= True)
    date_created = models.DateField(auto_now_add = True)

    birth_date = models.CharField(max_length=10, null=True)
    age = models.DecimalField(decimal_places=0, max_digits=50, null=True)
    gender = models.CharField(max_length=10, default='')
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