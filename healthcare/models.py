from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Patient(models.Model):
    user = models.OneToOneField(User, null=True,blank=True, on_delete=models.CASCADE)
    firstName = models.CharField(max_length= 200, null= True)
    lastName = models.CharField(max_length= 200, null= True)
    phone = models.CharField(max_length= 200, null= True)
    email = models.CharField(max_length=200, null= True)
    date_created = models.DateField(auto_now_add = True)


    #todo add patients medical history

    def __str__(self):
        return self.firstName + ' ' + self.lastName