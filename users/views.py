from django.contrib.auth import login
from django.middleware.csrf import get_token
from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import LoginSerializer, RegisterSerializer

# Create your views here.
class Login(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():

            user = serializer.validated_data["user"]
            login(request, user)
            context  = {
                'message': request.session.session_key,
                'user': user.username,
                'userid': user.id,
            }
            return Response(context, status=status.HTTP_200_OK)
        else:
            context  = {'message_error': serializer.errors}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


class Register(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response({"message": "Zarejestrowano pomyślnie"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": RegisterSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)



class Get_CSRF(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request):
        csrf_token = get_token(request)
        context = {
            'message': 'Pobrano token CSRF',
            'csrftoken': csrf_token
        }
        return Response(context, status=status.HTTP_200_OK)

