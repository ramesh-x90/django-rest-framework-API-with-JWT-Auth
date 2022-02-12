from django.db import models
from user.models import UserAccount
from django.contrib.auth.models import UserManager


def get_file_path(instence , filename):
    return f"doctor/licences/{instence.user.username}-{filename}"

class Doctor(models.Model):

    user = models.OneToOneField(UserAccount,on_delete=models.CASCADE)
    specification = models.CharField(max_length=200  )
    licences = models.FileField(upload_to=get_file_path )

    def __str__(self) -> str:
        return self.user.email