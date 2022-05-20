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

from .permissions import *

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
    username = data.get('username')
    password = data.get('password')
    if username is None:
        return JsonResponse({
            "errors": {
                "detail": "Please enter username"
            }
        }, status=400)
    elif password is None:
        return JsonResponse({
            "errors": {
                "detail": "Please enter password"
            }
        }, status=400)

    # authentication user
    user = authenticate(username=username, password=password)
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

class RegisterView(generics.GenericAPIView):
    permission_classes=[AllowAny]
    serializer_class = UserSerializer
    http_methods=['post']

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            #"user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
        })

class AadharViewSet(generics.GenericAPIView):
    http_methods=['get', 'post',]

    serializer_class = AadharSerializer
    queryset = Aadhar.objects.all()
    permission_classes=[AllowPermission,]

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
    permission_classes=[AllowPermission,]

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
    def delete(self, request, pk):
        account=Aadhar.objects.filter(aadhar_num=pk).first()
        if account:
            account.delete()
            return Response(data="Deletion Successful")
        return Response(data="Aadhar does not exist")

class InactiveAadharView(generics.ListAPIView):
    http_methods=['get',]
    permission_classes=[AllowPermission,]

    serializer_class = AadharSerializer
    queryset = Aadhar.objects.filter(is_active=False)


class AddressAccountViewSet(generics.RetrieveAPIView):

    serializer_class = AddressSerializer
    queryset = Address.objects.all()
    permission_classes=[AllowPermission,]

    def get(self, request, pk):
        account=Aadhar.objects.get(aadhar_num=pk)
        address_queryset=Address.objects.filter(person=account)
        serializer=AddressSerializer(address_queryset, many=True)
        return Response(serializer.data)

    def delete(self, request, pk):
        account=Aadhar.objects.filter(aadhar_num=pk).first()
        if account:
            queryset=Address.objects.filter(person=account)
            if queryset:
                for obj in queryset:
                    obj.delete()
                return Response(data="Deletion successful")
            return Response(data="Data does not exist")
        return Response(data="Aadhar does not exist")

class AddressViewSet(generics.GenericAPIView):

    serializer_class = AddressSerializer
    queryset = Address.objects.all()
    permission_classes=[AllowPermission,]

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
    permission_classes=[AllowPermission]

    def get(self, request, pk):
        account=Aadhar.objects.filter(aadhar_num=pk).first()
        if account:
            queryset=Qualification.objects.filter(person=account)
            serializer=QualificationSerializer(queryset, many=True)
            return Response(serializer.data)
        return Response(data="Aadhar does not exist")

    def delete(self, request, pk):
        account=Aadhar.objects.filter(aadhar_num=pk).first()
        if account:
            queryset=Qualification.objects.filter(person=account)
            if queryset:
                for obj in queryset:
                    obj.delete()
                return Response(data="Deletion successful")
            return Response(data="Data does not exist")
        return Response(data="Aadhar does not exist")


class QualificationViewSet(generics.GenericAPIView):

    serializer_class = QualificationSerializer
    queryset = Qualification.objects.all()
    permission_classes=[AllowPermission]

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
    permission_classes=[AllowPermission]

    def get(self, request, pk):
        account=Aadhar.objects.filter(aadhar_num=pk).first()
        if account:
            queryset=Bank.objects.filter(person=account)
            if queryset:
                serializer=BankSerializer(queryset, many=True)
                return Response(serializer.data)
            return Response(data="Details do not Exist")
        return Response(data="Aadhar does not exist")

    def delete(self, request, pk):
        account=Aadhar.objects.filter(aadhar_num=pk).first()
        if account:
            queryset=Bank.objects.filter(person=account)
            if queryset:
                for obj in queryset:
                    obj.delete()
                return Response(data="Deletion successful")
            return Response(data="Data does not exist")
        return Response(data="Aadhar does not exist")


class BankViewSet(generics.GenericAPIView):
    serializer_class = BankSerializer
    queryset = Bank.objects.all()
    permission_classes=[AllowPermission]

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
    permission_classes=[AllowPermission]

    def get(self, request, pk):
        account=Aadhar.objects.filter(aadhar_num=pk).first()
        if account:
            queryset=JobExperience.objects.filter(person=account)
            if queryset:
                serializer=JobExperienceSerializer(queryset, many=True)
                return Response(serializer.data)
            return Response(data="Data does not exist")
        return Response(data="Aadhar no. does not exist")

    def delete(self, request, pk):
        account=Aadhar.objects.get(aadhar_num=pk)
        queryset=JobExperience.objects.filter(person=account)
        if queryset:
            for obj in queryset:
                obj.delete()
            return Response(data="Deletion successful")
        return Response(data="Data does not exist")

class JobExperienceViewSet(generics.GenericAPIView):

    serializer_class = JobExperienceSerializer
    queryset = JobExperience.objects.all()
    permission_classes=[AllowPermission]

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
    permission_classes=[AllowPermission]

    def get(self, request, pk):

        account=Aadhar.objects.filter(aadhar_num=pk).first()
        if account:
            details=PersonalDetails.objects.filter(person=account).first()
            if details:
                serializer=PersonalDetailsSerializer(details, many=False)

                email_queryset=details.get_emails()
                contacts_queryset=details.get_contacts()

                emails=[]
                contacts=[]
                for each in email_queryset:
                    emails.append(each.email)
                for each in contacts_queryset:
                    contacts.append(each.contact)


                x=serializer.data

                x['email']=emails
                x['contact']=contacts

                return Response(x)
            return Response(data="Data does not exist")
        return Response(data="Aadhar no. does not exist")

    def delete(self, request, pk):
        obj=PersonalDetails.objects.filter(person=pk).first()
        if obj:
            obj.delete()
            return Response(data="Deletion successful")
        return Response(data="Data does not exist")

class PersonalDetailsViewSet(generics.GenericAPIView):
    permission_classes=[AllowPermission]

    serializer_class = PersonalDetailsSerializer
    # serializer_class_email=EmailSerializer
    # serializer_class_contact=ContactSerializer
    queryset = PersonalDetails.objects.all()  

    def post(self, request):
        account=Aadhar.objects.get(aadhar_num=request.data['person'])
        if not PersonalDetails.objects.filter(person=account).first():
            try:
                emails=request.data.pop('email')
                contacts=request.data.pop('contact')
            except KeyError:
                return Response(status=HTTP_200_OK, data="Email and contact details are required")

            serializer=self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            details=serializer.save()

            for each in emails:
                Email.objects.create(person=details, email=each)

            for each in contacts:
                Contact.objects.create(person=details, contact=each)

            return Response(status=HTTP_200_OK, data="Personal Details successfully added")
        return Response(data="Bad request: Details already exist for user", status=HTTP_400_BAD_REQUEST)

    def patch(self, request):
        account=Aadhar.objects.get(aadhar_num=request.data['person'])
        object=PersonalDetails.objects.filter(person=account).first()
        if not object:
            return Response(data="Bad request: Details do not exist", status=HTTP_400_BAD_REQUEST)

        emails=None
        try:
            emails=request.data.pop('email')
        except KeyError:
            pass

        print(emails)

        contacts=None
        try:
            contacts=request.data.pop('contact')
        except KeyError:
            pass

        serializer=self.get_serializer(object, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        details=serializer.save()

        if emails:
            for each in emails:
                if not Email.objects.filter(person=details, email=each).first():
                    Email.objects.create(person=details, email=each)

        if contacts:
            for each in contacts:
                if not Contact.objects.filter(person=details, conatct=each).first():
                    Contact.objects.create(person=details, contact=each)

        return Response(status=HTTP_200_OK, data="Personal Details successfully added")