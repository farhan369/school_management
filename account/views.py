from django.shortcuts import render
from .permissions import UserTypePermission,UserCreationPermission
from .models import Account as User
from .serializers import AccountCreateSerializer
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

class SignUpView(generics.CreateAPIView):
    #this api creates a admin account by an admin
    queryset           = User.objects.all
    serializer_class   = AccountCreateSerializer
    permission_classes = [UserCreationPermission]

