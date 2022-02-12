

from doctor.models import Doctor
import json
from doctor.serializer import DoctorRegSerializer
from user.serializer import UserAccountRegSerializer
from django.shortcuts import render
from rest_framework.request import Request

# Create your views here.

from django.shortcuts import render
from rest_framework.views import APIView 
from rest_framework.authentication import SessionAuthentication , TokenAuthentication 
from rest_framework.permissions import IsAuthenticated 
from rest_framework_simplejwt.authentication import JWTAuthentication 
from rest_framework.response import Response 
from rest_framework import status  
from rest_framework.parsers import MultiPartParser , FormParser 
class DocRegView(APIView):

    # authentication_classes = [TokenAuthentication ]
    # permission_classes = [IsAuthenticated ]

    parser_classes = (MultiPartParser, FormParser )

    def post(self,request : Request , format = None):
        USER_ACC_SERIALIZER = UserAccountRegSerializer(data=request.data)
        DOCTOR_SERIALIZER = DoctorRegSerializer(data=request.data)
        if USER_ACC_SERIALIZER.is_valid(raise_exception=True) and  DOCTOR_SERIALIZER.is_valid(raise_exception=True):
            
            userInstence = USER_ACC_SERIALIZER.create(USER_ACC_SERIALIZER.validated_data)
            Doctor(user=userInstence ,**DOCTOR_SERIALIZER.validated_data ).save()
            return Response(data=[ USER_ACC_SERIALIZER.data , DOCTOR_SERIALIZER.data  ])
        return Response(data={'error': 'invalid data'} , status=status.HTTP_400_BAD_REQUEST )
