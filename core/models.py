from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from django.contrib.auth.models import (
    BaseUserManager
)
from datetime import datetime

class UserManager(BaseUserManager):
    def create_user(self, email,  username, password=None,**extra_fields):

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('acivation_status', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError((
                'Super user must have is_staff'
            ))

        return self.create_user(email,username,password,**extra_fields)


class User(AbstractUser):
   

    profile_img=models.ImageField('image',null=True,blank=True,upload_to='profile',validators=[FileExtensionValidator(['png','jpg'])])
    acivation_status=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email
    
Type=(
    ('saving','saving'),
    ('current','current'),
)
    
AmmountType=(
    ('credit','credit'),
    ('debit','debit'),
)


class Bank(models.Model):
    name=models.CharField(max_length=100)
    branch=models.CharField(max_length=100)
    district=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    ifsc_code=models.CharField(max_length=100)


class Account(models.Model):
    bank=models.ForeignKey(Bank,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    birth_date=models.CharField(max_length=100)
    address=models.CharField(max_length=500)
    phone=models.CharField(max_length=15)
    pan_no=models.CharField(max_length=15)
    email=models.EmailField(max_length=254)
    acc_type=models.CharField(max_length=15,choices=Type)
    acc_number=models.CharField(max_length=16,blank=True,null=True)
    balance=models.CharField(max_length=100,default=0)
    is_verified=models.BooleanField(default=False)


class Transaction(models.Model):
    account=models.CharField(max_length=16)
    amount=models.CharField(max_length=1000)
    amount_type=models.CharField(max_length=15,choices=AmmountType)
    time=models.DateTimeField(default=datetime.now)
    


