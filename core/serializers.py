from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerialzier
from rest_framework import serializers

class UserCreateSerializer(BaseUserCreateSerialzier):
    class Meta(BaseUserCreateSerialzier.Meta):
        fields = ['id','username','password','email','first_name','last_name']


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields= ['id','username','email','first_name','last_name']