from dataclasses import field
from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model=User
        fields=['username', 'password', 'is_manager']

    def validate_password(self, value: str) -> str:
        return make_password(value)

class AadharSerializer(serializers.ModelSerializer):    

    class Meta:
        model=Aadhar
        fields=["aadhar_num", "is_active"]


class AddressSerializer(serializers.ModelSerializer):
    person=serializers.PrimaryKeyRelatedField(many=False, queryset=Aadhar.objects.all())

    class Meta:
        model=Address
        fields='__all__'

    # def create(self, validated_data):
    #     account=validated_data.pop('account')
        
class QualificationSerializer(serializers.ModelSerializer):
    person=serializers.PrimaryKeyRelatedField(many=False, queryset=Aadhar.objects.all())

    class Meta:
        model=Qualification
        fields='__all__'

class BankSerializer(serializers.ModelSerializer):
    person=serializers.PrimaryKeyRelatedField(many=False, queryset=Aadhar.objects.all())

    class Meta:
        model=Bank
        fields='__all__'

class JobExperienceSerializer(serializers.ModelSerializer):
    person=serializers.PrimaryKeyRelatedField(many=False, queryset=Aadhar.objects.all())

    class Meta:
        model=JobExperience
        fields='__all__'

class PersonalDetailsSerializer(serializers.ModelSerializer):
    person=serializers.PrimaryKeyRelatedField(many=False, queryset=Aadhar.objects.all())

    class Meta:
        model=PersonalDetails
        fields='__all__'
        #fields=['person', 'first_name', 'last_name', 'dob', 'b_group']

# class EmailSerializer(serializers.ModelSerializer):
#     person=serializers.PrimaryKeyRelatedField(many=False, queryset=PersonalDetails.objects.all())

#     class Meta:
#         model=Email
#         fields='__all__'

# class ContactSerializer(serializers.ModelSerializer):
#     person=serializers.PrimaryKeyRelatedField(many=False, queryset=PersonalDetails.objects.all())

#     class Meta:
#         model=Contact
#         fields='__all__'