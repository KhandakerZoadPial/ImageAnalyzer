from django.db import models
from django.contrib.auth.models import User






class Verify(models.Model):
    whom = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)


class Plan(models.Model):
    name = models.TextField(blank=True)
    type_of_plan = models.IntegerField(default=0) #0=NoPlan, 1=Yearly, 2=other
    number_of_run_left = models.IntegerField(default=10)
    expires_on = models.DateField(blank=True, null=True, auto_now_add=True)


class UserProfile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, null=True, blank=True)
    plan_info = models.OneToOneField(Plan, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)