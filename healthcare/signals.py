
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from django.contrib.auth.models import Group

from .models import Patient

def customer_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='patient')
        instance.groups.add(group)

        Patient.objects.create(
            user=instance,
            first_Name=instance.first_name,
            last_Name=instance.last_name,
        )
        print('Profile created!')


post_save.connect(customer_profile, sender= User)