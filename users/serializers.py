from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20)
    password = serializers.CharField(max_length=20)

    def validate(self, attrs):
        if attrs["username"] and attrs["password"]:
            user = authenticate(username=attrs["username"], password=attrs["password"])

            if user:
                attrs["user"] = user
                return attrs
            else:
                raise serializers.ValidationError("Niepoprawne dane logowania")

        else:
            raise serializers.ValidationError("Podaj nazwę użytkownika i hasło")


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20)
    password = serializers.CharField(max_length=20)

    def validate(self, attrs):

        if attrs["username"] and attrs["password"]:
            if User.objects.filter(username=attrs["username"]).exists():
                raise serializers.ValidationError({'message':'Użytkownik o podanej nazwie już istnieje'})
            return attrs

        else:
            raise serializers.ValidationError({'message':'Podaj nazwę użytkownika i hasło'})

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"]
        )
        return user