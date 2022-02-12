
from rest_framework.exceptions import AuthenticationFailed, ErrorDetail
from django.conf import settings
from rest_framework.fields import CharField
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError 
from rest_framework import serializers  
from django.contrib.auth import get_user_model
from .models import UserAccount 
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
import jwt
from rest_framework.exceptions import APIException



# aka model serializer
class UserAccountRegSerializer(serializers.ModelSerializer):

    # inner class to init things 
    class Meta:
        model = UserAccount
        fields = ['username' , 'password' , 'email' , 'phone_number' , 'birthdate' , 'profileImage']

        extra_kwargs = {
            'password' : {"write_only": True},
            'profileImage' : {"required": False},
            'profileImage' : {"write_only": True},

        }

    # override create method when saving serializer object
    def create(self, validated_data):
        ModelClass = self.Meta.model

        try:
            instance = ModelClass.objects.create_user(**validated_data)
            return instance
        except :
            raise ErrorDetail('can not create this user')
        

    # supper important to validate password . Without this passwords want automaticaly validate  
    def validate(self, attrs):

        try:
            # will throw when invalid will retutn None when valid
            instance = self.Meta.model(**attrs)
            validate_password(password=attrs.get('password') ,user=instance)
        except Exception as e:
            # user serializers.ValidationError (must)
            raise serializers.ValidationError(e)

        # finalt return data
        return attrs




class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=60 , required=True)
    password = serializers.CharField(max_length=60 , required=True)



class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField(max_length=500 , required=True)

    def validate(self, attrs):
        try:
            self.refreshToken = attrs['refresh']
        except Exception as e:
            raise Exception(e)
        return attrs

    def getAccessToken(self):
        
        refresh = RefreshToken(self.refreshToken)   
        return str(refresh.access_token)



class LogOutSerializer(serializers.Serializer):
    refresh = serializers.CharField(max_length=500 , required=True)

    def validate(self, attrs):
        try:
            self.refreshToken = attrs['refresh']
        except Exception as e:
            raise Exception(e)
        return attrs

    def save(self):

        if self.TokenMatched == False :
            raise AuthenticationFailed()

        try:
            RefreshToken(self.refreshToken).blacklist() 
        except InvalidToken :
            raise InvalidToken
    
    def isTokenMatch(self , user : UserAccount):

        self.TokenMatched = False


        payload = jwt.decode(self.refreshToken, settings.SECRET_KEY , settings.SIMPLE_JWT['ALGORITHM'])

        if not user:
            raise AuthenticationFailed()

        if user.pk !=  payload['user_id']:
            raise AuthenticationFailed()
      
        
        self.TokenMatched = True