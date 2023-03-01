from django.shortcuts import render
from .permissions import UserTypePermission,AdminCreationPermission \
                        ,StudentCreationPermission,TeacherCreationPermission
from .models import Account as User
from .serializers import AccountCreateSerializer,AuthTokenSerializer
from rest_framework import generics,permissions
from django.views.decorators.csrf import csrf_exempt
from rest_framework.settings import api_settings
from rest_framework.authtoken.views import ObtainAuthToken 
from rest_framework.response import Response

# Create your views here.

class SignUpView(generics.CreateAPIView):
    # this api creates a admin account by an admin
    # UserCreationPermission - checker whether the value provided in
    # user_type field is of ADMIN
    queryset           = User.objects.all
    serializer_class   = AccountCreateSerializer
    permission_classes = [AdminCreationPermission]

class ObtainAuthTokenView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    serializer_class = AuthTokenSerializer


class CreateTeacherView(generics.CreateAPIView):
    #this api creates a teacher account by an admin
    queryset           = User.objects.all
    serializer_class   = AccountCreateSerializer
    permission_classes = [permissions.IsAuthenticated, UserTypePermission,TeacherCreationPermission]

class CreateStudentView(generics.CreateAPIView):
    #this api creates a student account by an admin
    queryset           = User.objects.all
    serializer_class   = AccountCreateSerializer
    permission_classes = [permissions.IsAuthenticated, UserTypePermission, StudentCreationPermission]
    

class HelloAPIView(generics.GenericAPIView):
    """Test API view  this api is used for testing purposes"""
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        account = request.user.account
        print(account.user_type)
        content = {'message': 'Hello, World!'}
        return Response(content)