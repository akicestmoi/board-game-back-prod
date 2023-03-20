from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "username", "password")

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        validated_data["is_logged"] = True
        
        return super(SignupSerializer, self).create(validated_data)



class LoginSerializer(serializers.Serializer):

    username = serializers.CharField()
    
    class Meta:
        model = User
        fields = ("password")
    
    def create(self, validated_data):
        return User.objects.get_or_create(**validated_data)
    


class LogoutSerializer(serializers.Serializer):

    username = serializers.CharField()
