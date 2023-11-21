from django.urls import path
from .views import Login, Register, Get_CSRF

urlpatterns = [
        path('login/', Login.as_view()),
        path('register/', Register.as_view()),
        path('csrf/', Get_CSRF.as_view(), name='get_csrf')
    ]