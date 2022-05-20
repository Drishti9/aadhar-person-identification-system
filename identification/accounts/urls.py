from django.urls import path
from .models import *
from .views import *
from rest_framework.routers import DefaultRouter

urlpatterns=[
    path('', AadharViewSet.as_view()),
    path('<int:pk>', RetrieveAadharView.as_view()),
    path('aadhar-inactive/', InactiveAadharView.as_view()),
    path('address/<int:pk>', AddressAccountViewSet.as_view()),
    path('address/', AddressViewSet.as_view()),
    path('qualification/<int:pk>', QualificationAccountViewSet.as_view()),
    path('qualification/', QualificationViewSet.as_view()),
    path('bank/<int:pk>', BankLinkedAccountViewSet.as_view()),
    path('bank/', BankViewSet.as_view()),
    path('jobexperience/<int:pk>', JobExperienceAccountViewSet.as_view()),
    path('jobexperience/', JobExperienceViewSet.as_view()),
    path('personaldetails/<int:pk>', PersonalDetailsAccountViewSet.as_view()),
    path('personaldetails/', PersonalDetailsViewSet.as_view()),
]
