from logging import raiseExceptions
from threading import activeCount
from django.shortcuts import render
from rest_framework import generics
from sympy import Add
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK
from django.http import JsonResponse

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
import json
from django.contrib.auth import authenticate

# Create your views here.

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@api_view(['POST',])
@permission_classes((AllowAny,))
def login_view(request):

    #POST API for login
    data = json.loads(request.body)
    email = data.get('email')
    password = data.get('password')
    if email is None:
        return JsonResponse({
            "errors": {
                "detail": "Please enter email"
            }
        }, status=400)
    elif password is None:
        return JsonResponse({
            "errors": {
                "detail": "Please enter password"
            }
        }, status=400)

    # authentication user
    user = authenticate(email=email, password=password)
    if user is not None:
        #login(request, user)
        #return JsonResponse({"success": "User has been logged in"})
        #user_id = get_user_model().objects.get(email=email)
        data = get_tokens_for_user(user)
        return Response(data, status=HTTP_200_OK)
        #return JsonResponse({user})
    return JsonResponse(
        {"errors": "Invalid credentials"},
        status=400,
    )

class AadharViewSet(generics.GenericAPIView):
    http_methods=['get', 'post',]

    serializer_class = AadharSerializer
    queryset = Aadhar.objects.all()

    def get(self, request):
        accounts = Aadhar.objects.all()
        serializer = AadharSerializer(accounts, many=True)
        return Response(serializer.data)

    def post(self, request):
        print(request.data)
        if request.data['aadhar_num'].isnumeric():
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            account = serializer.save()
            return Response(status=HTTP_200_OK, data=serializer.data)
        return Response(status=HTTP_400_BAD_REQUEST, data="Bad request: Aadhar should be numeric")

class RetrieveAadharView(generics.RetrieveAPIView):

    serializer_class = AadharSerializer
    queryset = Aadhar.objects.all()

    def patch(self, request, pk):
        account=Aadhar.objects.get(aadhar_num=pk)
        serializer = AadharSerializer(account, data=request.data, partial=True) # set partial=True to update a data partially
        if serializer.is_valid():
            serializer.save()
            return Response(status=HTTP_200_OK, data=serializer.data)
        return Response(status=HTTP_400_BAD_REQUEST, data="Bad request: Incorrect Parameters")
        
    # def get(self, request, pk):
    #     account=Aadhar.objects.get(aadhar_num=pk)
    #     serializer=AadharSerializer(account)
    #     return Response(serializer.data)

class InactiveAadharView(generics.ListAPIView):
    http_methods=['get']

    serializer_class = AadharSerializer
    queryset = Aadhar.objects.filter(is_active=False)

class AddressAccountViewSet(generics.RetrieveAPIView):

    serializer_class = AddressSerializer
    queryset = Address.objects.all()

    def get(self, request, pk):
        account=Aadhar.objects.get(aadhar_num=pk)
        address_queryset=Address.objects.filter(person=account)
        serializer=AddressSerializer(address_queryset, many=True)
        return Response(serializer.data)

class AddressViewSet(generics.GenericAPIView):

    serializer_class = AddressSerializer
    queryset = Address.objects.all()

    def get(self, request):
        address_queryset = Address.objects.all()
        serializer=AddressSerializer(address_queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_200_OK)
        #return Response(status=HTTP_400_BAD_REQUEST, data="Bad request: Incorrect Parameters")
        
class QualificationAccountViewSet(generics.RetrieveAPIView):

    serializer_class = QualificationSerializer
    queryset = Qualification.objects.all()

    def get(self, request, pk):
        account=Aadhar.objects.get(aadhar_num=pk)
        queryset=Qualification.objects.filter(person=account)
        serializer=QualificationSerializer(queryset, many=True)
        return Response(serializer.data)

class QualificationViewSet(generics.GenericAPIView):

    serializer_class = QualificationSerializer
    queryset = Qualification.objects.all()

    def get(self, request):
        queryset = Qualification.objects.all()
        serializer=QualificationSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):

        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_200_OK)
        #return Response(status=HTTP_400_BAD_REQUEST, data="Bad request: Incorrect Parameters")
        
class BankLinkedAccountViewSet(generics.GenericAPIView):
    serializer_class = BankSerializer
    queryset = Bank.objects.all()

    def get(self, request, pk):
        account=Aadhar.objects.get(aadhar_num=pk)
        queryset=Bank.objects.filter(person=account)
        serializer=BankSerializer(queryset, many=True)

        print(serializer.data, type(serializer.data))

        return Response(serializer.data)

class BankViewSet(generics.GenericAPIView):
    serializer_class = BankSerializer
    queryset = Bank.objects.all()

    def get(self, request):
        queryset = Bank.objects.all()
        serializer=BankSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.data['account_num'].isnumeric():
            serializer=self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(status=HTTP_400_BAD_REQUEST, data="Bad request: Incorrect Parameters")

class JobExperienceAccountViewSet(generics.RetrieveAPIView):

    serializer_class = JobExperienceSerializer
    queryset = JobExperience.objects.all()

    def get(self, request, pk):
        account=Aadhar.objects.get(aadhar_num=pk)
        queryset=JobExperience.objects.filter(person=account)
        serializer=JobExperienceSerializer(queryset, many=True)
        return Response(serializer.data)

class JobExperienceViewSet(generics.GenericAPIView):

    serializer_class = JobExperienceSerializer
    queryset = JobExperience.objects.all()

    def get(self, request):
        queryset = JobExperience.objects.all()
        serializer=JobExperienceSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_200_OK)

class PersonalDetailsAccountViewSet(generics.GenericAPIView):
    serializer_class=PersonalDetailsSerializer
    queryset=PersonalDetails.objects.all()

    def get(self, request, pk):
        account=Aadhar.objects.get(aadhar_num=pk)
        details=PersonalDetails.objects.filter(person=account).first()
        serializer=PersonalDetailsSerializer(details, many=False)

        email_queryset=details.get_emails()
        contacts_queryset=details.get_contacts()

        emails_serializer=EmailSerializer(email_queryset, many=True)
        contacts_serialized=ContactSerializer(contacts_queryset, many=True)

        # print(serializer.data)
        # print(emails_serializer.data)
        # print(contacts_serialized.data)
        # print(email_queryset)

        emails=[]
        contacts=[]
        for each in email_queryset:
            emails.append(each.email)
            print(each.email)
        for each in contacts_queryset:
            contacts.append(each.contact)

        print(emails, contacts)

        x=serializer.data

        x['email']=emails
        x['contact']=contacts

        print(x)

        return Response(x)

class PersonalDetailsViewSet(generics.GenericAPIView):
    serializer_class = PersonalDetailsSerializer
    # serializer_class_email=EmailSerializer
    # serializer_class_contact=ContactSerializer
    queryset = PersonalDetails.objects.all()  

    def post(self, request):
        account=Aadhar.objects.get(aadhar_num=request.data['person'])
        if not PersonalDetails.objects.filter(person=account).first():
            emails=request.data.pop('email')
            contacts=request.data.pop('contact')

            serializer=self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            details=serializer.save()

            for each in emails:
                Email.objects.create(person=details, email=each)

            for each in contacts:
                Contact.objects.create(person=details, contact=each)

            return Response(serializer.data, status=HTTP_200_OK)
        return Response(data="Bad request: Details already exist for user", status=HTTP_400_BAD_REQUEST)