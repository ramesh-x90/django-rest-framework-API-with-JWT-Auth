from patient.models import Patient
from rest_framework import serializers
from user.serializer import UserAccountRegSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password



class PatientRegSerializer(serializers.ModelSerializer):
    
    user = UserAccountRegSerializer()

    class Meta:
        model = Patient
        fields = ['user']

    
    def create(self, validated_data):

        userdata = validated_data.pop('user')

        user_model = get_user_model()

        userinstence = user_model.objects.create_user(**userdata)
        return Patient.objects.create(user= userinstence , **validated_data)

    # supper important to validate password . Without this passwords want automaticaly validate  
    def validate(self, attrs):

        try:
            # will throw when invalid will retutn None when valid
            userModel =get_user_model() 
            instance = userModel(**(attrs['user']))
            validate_password(password=attrs["user"].get('password') ,user=instance)
        except Exception as e:
            # user serializers.ValidationError (must)
            raise serializers.ValidationError(e)

        # finalt return data
        return attrs
        


        

