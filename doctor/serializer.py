from rest_framework import serializers
from .models import Doctor
from rest_framework.exceptions import AuthenticationFailed, ErrorDetail
from django.contrib.auth.password_validation import validate_password

class DoctorRegSerializer(serializers.ModelSerializer):


    class Meta:
        model = Doctor
        fields = ['specification' , 'licences']

    
    def validate(self, attrs):
        return attrs
    
    def create(self, validated_data):
        return Doctor.objects.create(**validated_data)