from rest_framework.fields import CreateOnlyDefault
from hospitalManager.models import HospitalManager
from rest_framework import serializers
from rest_framework import fields
from user.models import UserAccount
from user.serializer import UserAccountRegSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password


class HSManagerRegSerializer(serializers.ModelSerializer):

    userAccountData = UserAccountRegSerializer()

    class Meta:
        model = HospitalManager
        fields = [ "userAccountData" , "hospitalName" , "Organization_Email_Address" , "Organization_Address" ]

    def create(self, validated_data):
        userdata = validated_data.pop('userAccountData')

        user_model = get_user_model()

        userinstence = user_model.objects.create_user(**userdata)

        return HospitalManager.objects.create(user = userinstence , **validated_data)
        

    # supper important to validate password . Without this passwords want automaticaly validate  
    def validate(self, attrs):

        try:
            # will throw when invalid will retutn None when valid
            instance = UserAccount(**(attrs['userAccountData']))
            validate_password(password=attrs['userAccountData'].get('password') ,user=instance)
        except Exception as e:
            # user serializers.ValidationError (must)
            raise serializers.ValidationError(e)

        # finalt return data
        return attrs
