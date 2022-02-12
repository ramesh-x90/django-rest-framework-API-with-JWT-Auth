from hospitalManager.serializer import HSManagerRegSerializer
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from user.serializer import UserAccountRegSerializer
from .models import HospitalManager

# Create your views here.


class HSManagerReg(APIView):

    def post(self,request):
        SERIALIZER_USER = UserAccountRegSerializer(data=request.data)
        SERIALIZER_HM = HSManagerRegSerializer(data=request.data)

        if SERIALIZER_USER.is_valid(raise_exception=True) and SERIALIZER_HM.is_valid(raise_exception=True):
            userInstence = SERIALIZER_USER.create(SERIALIZER_USER.validated_data)
            HospitalManager(user = userInstence , **SERIALIZER_HM.validated_data)
            response = Response()
            response.status_code = 200
            response.data = {
                [SERIALIZER_USER.validated_data, SERIALIZER_HM.validated_data]
            }
            return response

