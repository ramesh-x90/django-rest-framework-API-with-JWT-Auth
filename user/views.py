import threading
from user.renderers import loginRenderer
from doctor.models import Doctor
from patient.models import Patient
from django.shortcuts import render
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework_simplejwt.exceptions import InvalidToken
from . import serializer 
from rest_framework.permissions import  IsAuthenticated , IsAdminUser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication 
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken , OutstandingToken
from django.middleware.csrf import get_token
from datetime import datetime
from hospitalManager.models import HospitalManager
from django.core.mail import send_mail
from django.conf import settings



class UserReg(APIView):

    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self,request):
        SERIALIZER = serializer.UserAccountRegSerializer(data=request.data)

        if SERIALIZER.is_valid(raise_exception=True):
            SERIALIZER.save()
            return Response(data=SERIALIZER.data)
        return Response(data={'error': 'invalid data'} , status=status.HTTP_400_BAD_REQUEST )




class LoginView(APIView):

    renderer_classes  = (loginRenderer,)

    def post(self,request):
        SERIALIZER = serializer.LoginSerializer(data=request.data) 
        if SERIALIZER.is_valid(raise_exception=True):
            user = auth.authenticate(email = SERIALIZER.validated_data.get('email') , password= SERIALIZER.validated_data.get('password'))
            accountType = "000"
            if  Patient.objects.filter(user = user):
                accountType = "001"
            elif Doctor.objects.filter(user = user):
                accountType = "002"
            elif HospitalManager.objects.filter(user = user):
                accountType = "003"
            if user:
                response = Response()
                if user.is_verified and user.is_active:                    
                    refresh = RefreshToken.for_user(user=user)
                    response.data = { 
                                        "username":user.username , 
                                        "id" : user.pk , 
                                        "email" : user.email,
                                        "refresh": str(refresh)  ,
                                        "access" : str(refresh.access_token),
                                        "accountType" : accountType
                                        }
                    
                    subject = 'You Care - Email Service'
                    message = f'Hi {user.username}, New Device Loged in to this Account'
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [user.email, ]
                    threading.Thread(target=send_mail, args=(subject,message,email_from,recipient_list,)).start()
                    return response
                response.status_code = 400
                response.data = {"error" : "Account is not active or verified contact admin"}
                return response
            raise AuthenticationFailed("User does not exist")


class TokenRefresh(APIView):
    renderer_classes  = (loginRenderer,)
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated , isTokenOwner]


    def post(self,request):

        SERIALIZER = serializer.RefreshTokenSerializer(data=request.data)

        if SERIALIZER.is_valid(raise_exception=True):
            response = Response()
            try:
                access = SERIALIZER.getAccessToken() 
            except Exception:
                raise InvalidToken("invalid refresh token")
            
            response.data = {'access':access}
            return response


class LogOut(APIView):
    renderer_classes  = (loginRenderer,)

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


    def post(self,request):

        SERIALIZER = serializer.LogOutSerializer(data=request.data)

        if SERIALIZER.is_valid(raise_exception=True):
            response = Response()
            try:
                SERIALIZER.isTokenMatch(request.user)
                SERIALIZER.save() 
            except Exception:
                raise InvalidToken("invalide refresh token")
            
            response.data = {'response':'logout successful'}
            return response

        # return Response(data={"header" : request.headers , "data" : request.data})

class ClearTokenBlackList(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAdminUser]


    def get(self,request):

        today = datetime.now()

        # a = BlacklistedToken.objects.all()
        a = OutstandingToken.objects.all()
        count = len(a)
        deletedCount = 0

        for record in a:
            # if record.expires_at.date() < today.date():
            if record.expires_at.date() >= today.date():
                deletedCount +=1
                record.delete()
                
        del a
        del today

        return Response(data= {'deleted' : f"{deletedCount} out of {count}" })

