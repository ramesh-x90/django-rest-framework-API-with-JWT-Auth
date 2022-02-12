from django.shortcuts import render
from rest_framework.views import APIView 
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response 
from .serializer import PatientRegSerializer
from rest_framework import status   

# Create your views here.
class PatientReg(APIView):

    def post(self,request):
        
        SERIALIZER = PatientRegSerializer(data=request.data)

        if SERIALIZER.is_valid(raise_exception=True):
            SERIALIZER.save()
            return Response(data=SERIALIZER.data)
        return Response(data={'error': 'invalid data'} , status=status.HTTP_400_BAD_REQUEST )