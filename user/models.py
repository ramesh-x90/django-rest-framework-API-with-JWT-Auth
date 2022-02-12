from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser ,AbstractUser, PermissionsMixin
from django.contrib.auth.models import User
from rest_framework.fields import BooleanField
# Create your models here.

class UserManager(BaseUserManager):

    

    def create_user(self, email, username , phone_number , birthdate  ,password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have an username')
        if not phone_number:
            raise ValueError('Users must have an phone_number')
        if not birthdate:
            raise ValueError('Users must have an birthdate')

        user = self.model(
            email=self.normalize_email(email),
            username = username,
            phone_number=phone_number,
            birthdate=birthdate,

        )



        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_staffuser(self, email, username , phone_number , birthdate , password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            username,
            phone_number ,
            birthdate , 
            password=password,
        )
        user.is_staff = True
        
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username , phone_number , birthdate , password):
        """
        Creates and saves a superuser with the given email and password.
        """
        if not password:
            raise ValueError('Users must have an password')

        user = self.create_user(
            email,
            username,
            phone_number ,
            birthdate , 
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.is_verified = True
        user.save(using=self._db)
        return user

class UserAccount(AbstractBaseUser , PermissionsMixin):
    
    objects = UserManager()
    
    # def get_profile_image_path(self):
    #     return f"users/profileImages/{self.pk}/profileImage.png"

    username = models.CharField(max_length=30 , null=False , unique=True)
    email = models.EmailField(max_length=60 , unique=True , null=False )
    phone_number = models.PositiveIntegerField()
    birthdate = models.DateField(null=False)
    created_date = models.DateTimeField(auto_now_add=True )
    last_login = models.DateTimeField(auto_now=True)
    profileImage = models.ImageField( upload_to="users/profileImages/" , blank=True , null=True)

    is_verified = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # is_patient = models.BooleanField(default=False)
    # is_doctor = models.BooleanField(default=False)
    # is_hospitalmanager = models.BooleanField(default=False,verbose_name='hospitalmanager')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username' , 'phone_number' , 'birthdate']

    def __str__(self) -> str:
        return self.username

    def get_full_name(self):
    # The user is identified by their email address
        return self.email
    def get_short_name(self):
    # The user is identified by their email address
        return self.email

    def has_perm(self,perm, obj=None):
        return self.is_admin

    def has_module_perms(self,package_name):
        return True

    # @property
    # def is_staff(self):
    #     return True

    # @property
    # def is_admin(self):
    #     return self.is_admin


    # def CreateToken(self):
    #     pass


# 
# 
# ADMINS


class AdminManager(UserManager):
    def get_queryset(self) :
        return super().get_queryset().filter(is_admin = True)


class AdminAccount(UserAccount):

    objects = AdminManager()

    class Meta:
        proxy = True




# 
# 
# STAFF

class StaffManager(UserManager):
    def get_queryset(self) :
        return super().get_queryset().filter(is_staff = True)


class StaffAccount(UserAccount):

    objects = StaffManager()

    class Meta:
        proxy = True



# 
# 
# SUPERUSER

class SuperuserManager(UserManager):
    def get_queryset(self) :
        return super().get_queryset().filter(is_superuser = True)


class SuperuserAccount(UserAccount):

    objects = SuperuserManager()

    class Meta:
        proxy = True
