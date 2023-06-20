from rest_framework.serializers import ModelSerializer
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model


class BankSerializer(ModelSerializer):
    class Meta:
        model=Bank
        fields="__all__" 

class AccountSerializer(ModelSerializer):
    class Meta:
        model=Account
        fields="__all__" 

class UpdateBankSerializers(ModelSerializer):
    class Meta:
        model=Bank
        fields="__all__"
        
class UpdateAccountSerializers(ModelSerializer):
    class Meta:
        model=Account
        fields="__all__"


class MyTokenObtainPairSerializer(TokenObtainSerializer):
    token_class = RefreshToken

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        return data
    

User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email', 'first_name', 'last_name', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class TrancationSerializer(ModelSerializer):
    class Meta:
        model=Transaction
        fields="__all__"