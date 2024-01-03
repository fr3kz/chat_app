from django.urls import path
from .views import Show_lobby,Create_lobby,Join_to_lobby,Send_message,Get_messages,Leave_lobby

urlpatterns = [
    path('', Show_lobby.as_view(), name='index'),
    path('create/', Create_lobby.as_view(), name='create_lobby'),
    path('join/<int:id>/', Join_to_lobby.as_view(), name='join_lobby'),
    path('send/<int:id>/', Send_message.as_view(), name='send_message'),
    path('receive/<int:id>/', Get_messages.as_view(), name='receive_message'),
    path('leave/<int:id>/', Leave_lobby.as_view(), name='leave_lobby')

]