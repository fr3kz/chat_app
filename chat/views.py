from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Lobby,Message
from .serializers import LobbySerializer,MessageSerializer


# Create your views here.
class Show_lobby(APIView):
    def get(self, request):
        lobby = Lobby.objects.all()

        serializer = LobbySerializer(lobby, many=True)

        contex = {
            'lobby': serializer.data,
        }

        return Response(contex,status=200)


class Create_lobby(APIView):
    def post(self, request):
        lobby = LobbySerializer(data=request.data)

        if lobby.is_valid():
            lobb = lobby.create(lobby.validated_data)
            context = {
                'message': lobby.data,
            }
            return Response(context,status=201)
        else:
            context = {
                'message': lobby.errors,
            }
            return Response(context,status=400)


class Join_to_lobby(APIView):
    def get(self, request, id):
        lobby = Lobby.objects.get(id=id)
        user = request.user
        lobby.users.add(user)
        lobby.save()
        context = {
            'message': 'Dołączono do lobby',
        }
        return Response(context,status=200)


class Send_message(APIView):
    def post(self, request):
        lobby = Lobby.objects.get(id=request.data['lobby_id'])
        user = request.user
        message = Message.objects.create(user=user, lobby=lobby, message=request.data['message'])
        message.save()

        context = {
            'message': 'Wysłano wiadomość',
        }
        return Response(context,status=200)

class Get_messages(APIView):
    def get(self, request, id):
        lobby = Lobby.objects.get(id=id)
        messages = Message.objects.filter(lobby=lobby)
        serializer = MessageSerializer(messages, many=True)

        context = {
            'messages': serializer.data,
        }
        return Response(context,status=200)