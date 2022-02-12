from django.db import models
from user.models import UserAccount
from django.contrib.auth.models import UserManager




class HospitalManager(models.Model):

    user = models.OneToOneField(UserAccount,on_delete=models.CASCADE)
    hospitalName = models.CharField(max_length=200  )
    Organization_Email_Address  = models.EmailField(max_length=200 , unique= True )
    Organization_Address = models.CharField(max_length= 300  , unique= True)

    def __str__(self) -> str:
        return self.Organization_Email_Address