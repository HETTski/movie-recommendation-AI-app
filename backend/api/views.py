from django.shortcuts import render
#from django.contrib.auth.models import User
from .models import CustomUser
from rest_framework import generics
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

# Create your views here.
class CreateUserView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.raw('SELECT * FROM users')
    serializer_class = UserSerializer
    permission_classes = [AllowAny]