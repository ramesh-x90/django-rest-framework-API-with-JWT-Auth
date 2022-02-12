from django.db import models
from user.models import UserAccount
from django.contrib.auth.models import UserManager

# Create your models here.
# class PatientManager(UserManager):

#     def get_queryset(self):

#         return super().get_queryset().filter(is_patient = True)


class Patient(models.Model):

    # objects = PatientManager()
    # class Meta:
    #     proxy = True

    user = models.OneToOneField(UserAccount,on_delete=models.CASCADE)
    note = models.TextField(blank=True , null=True)


    def __str__(self) -> str:
        return self.user.email