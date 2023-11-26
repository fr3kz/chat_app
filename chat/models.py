from django.db import models

# Create your models here.
class Lobby(models.Model):
    title = models.CharField(max_length=100)
    users = models.ManyToManyField('users.User', related_name='lobby_users', blank=True)


class Message(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    lobby = models.ForeignKey('chat.Lobby', on_delete=models.CASCADE)
    message = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message