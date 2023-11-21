from django.contrib.auth import login
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import LoginSerializer, RegisterSerializer

# Create your views here.
class Login(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():

            user = serializer.validated_data["user"]
            login(request, user)
            context  = {
                'message': 'Zalogowano pomyślnie',
                'user': user.username
            }
            return Response(context, status=status.HTTP_200_OK)
        else:
            context  = {'message': serializer.errors}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


class Register(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response({"message": "Zarejestrowano pomyślnie"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": RegisterSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)



class Get_CSRF(APIView):
    def get(self, request):

        context = {
            'message': 'Pobrano token CSRF',
            'csrftoken': request.COOKIES['csrftoken']
        }
        return Response(context, status=status.HTTP_200_OK)