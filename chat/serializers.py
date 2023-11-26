from chat.models import Lobby,Message
from rest_framework import serializers

from users.models import User


class LobbySerializer(serializers.ModelSerializer):


    class Meta:
        model = Lobby
        fields = '__all__'


    def validate(self, data):
        if data['title'] == '':
            raise serializers.ValidationError("Title cannot be empty")
        
        data['user'] = data
        return data


    def create(self, validated_data):
        user =  User.objects.get(id=1)
        lobby = Lobby.objects.create(title=validated_data['title'])
        lobby.users.add(user)
        lobby.save()

        return lobby


class MessageSerializer(serializers.Serializer):
    class Meta:
        fields = '__all__'
        model = Message