from django.urls import path
from .models import *
from .views import *
from rest_framework.routers import DefaultRouter

urlpatterns=[
    path('aadhar/', AadharViewSet.as_view()),
    path('aadhar/<int:pk>', RetrieveAadharView.as_view()),
    path('aadhar-inactive/', InactiveAadharView.as_view()),
    path('aadhar/address/<int:pk>', AddressAccountViewSet.as_view()),
    path('aadhar/address/', AddressViewSet.as_view()),
    path('aadhar/qualification/<int:pk>', QualificationAccountViewSet.as_view()),
    path('aadhar/qualification/', QualificationViewSet.as_view()),
    path('aadhar/bank/<int:pk>', BankLinkedAccountViewSet.as_view()),
    path('aadhar/bank/', BankViewSet.as_view()),
    path('aadhar/jobexperience/<int:pk>', JobExperienceAccountViewSet.as_view()),
    path('aadhar/jobexperience/', JobExperienceViewSet.as_view()),
    path('aadhar/personaldetails/<int:pk>', PersonalDetailsAccountViewSet.as_view()),
    path('aadhar/personaldetails/', PersonalDetailsViewSet.as_view()),
]
