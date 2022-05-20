from datetime import datetime
from email import message
from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator, RegexValidator
from django.utils.translation import gettext_lazy as _
from sympy import true
from datetime import date
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from .managers import *

# Create your models here.

class User(AbstractUser, PermissionsMixin):
    is_manager = models.BooleanField(_("manager status"), default=False)

    #objects = UserManager()

class Aadhar(models.Model):
    aadhar_num=models.CharField(validators=[MaxLengthValidator(12), MinLengthValidator(12)], primary_key="True", max_length=12)
    is_active=models.BooleanField(default=True)

    def __str__(self) -> str:
        return str(self.aadhar_num)
    
class Address(models.Model):
    person=models.ForeignKey(Aadhar, on_delete=models.CASCADE)
    street=models.CharField(max_length=50, blank=True)
    city=models.CharField(max_length=30, blank=True)
    state=models.CharField(max_length=30, blank=True)
    postal_code=models.CharField(validators=[MaxLengthValidator(6), MinLengthValidator(6)], max_length=6)

class Qualification(models.Model):
    person=models.ForeignKey(Aadhar, on_delete=models.CASCADE)
    institute=models.CharField(max_length=100, blank=True)
    percentage=models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100.0)], blank=True)
    year=models.PositiveSmallIntegerField(validators=[MaxValueValidator(date.today().year), MinValueValidator(1950)], blank=True)

class Bank(models.Model):
    person=models.ForeignKey(Aadhar, on_delete=models.CASCADE)
    account_num=models.CharField(max_length=16, validators=[MinLengthValidator(8), MaxLengthValidator(16)])
    bank_name=models.CharField(max_length=30, blank=True)
    ifsc=models.CharField(max_length=10, validators=[MinLengthValidator(10), MaxLengthValidator(10)], blank=True)

class PersonalDetails(models.Model):
    b_group_type=(
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('O+','O+'),
        ('O-', 'O-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-')
    )
    
    person=models.OneToOneField(Aadhar, on_delete=models.CASCADE)
    first_name = models.CharField( max_length=40, blank=True)
    last_name = models.CharField(max_length=40, blank=True)
    dob=models.DateField(null=True)
    b_group=models.CharField(choices=b_group_type, max_length=3)

    def get_emails(self):
        return self.email_set.all()

    def get_contacts(self):
        return self.contact_set.all()

class Email(models.Model):
    person=models.ForeignKey(PersonalDetails, on_delete=models.CASCADE)
    email=models.EmailField()

class Contact(models.Model):
    person=models.ForeignKey(PersonalDetails, on_delete=models.CASCADE)
    contact=models.CharField(validators=[MaxLengthValidator(10), MinLengthValidator(10)], blank=True, max_length=10)

    def __str__(self) -> str:
        return str(self.contact)

class JobExperience(models.Model):
    person=models.ForeignKey(Aadhar, on_delete=models.CASCADE)
    company=models.CharField(max_length=50, blank=True)
    job_role=models.CharField(max_length=30, blank=True)
    year=models.PositiveSmallIntegerField(blank=True)

    def __str__(self) -> str:
        return str(self.company)