from django.shortcuts import render
from .permissions import IsAdmin
from .models import Account ,Teacher
from .serializers import AccountCreateSerializer,AuthTokenSerializer \
                        ,TeacherSerializer
from django.contrib.auth.models import User
from . import constants as account_constants
from rest_framework import generics,permissions,status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.settings import api_settings
from rest_framework.authtoken.views import ObtainAuthToken 
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


# Create your views here.

class SignUpView(generics.CreateAPIView):
    # this api creates a admin account by an admin
    # UserCreationPermission - checker whether the value provided in
    # user_type field is of ADMIN
    queryset           = Account.objects.all
    serializer_class   = AccountCreateSerializer
    permission_classes = [IsAdmin, permissions.IsAuthenticated]

class ObtainAuthTokenView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    serializer_class = AuthTokenSerializer
    def post(self, request, *args, **kwargs):
        """Handle HTTP POST request"""
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'id': user.id  # Include the id field in the response
        })


class CreateTeacherView(generics.CreateAPIView):
    #this api creates a teacher account by an admin
    serializer_class   = TeacherSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]


    def post(self, request, *args, **kwargs):
        # Extract teacher data from request body
        username = request.data.get('username')
        email = request.data.get('email')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        password = request.data.get('password')
        user_type = request.data.get('user_type')
        user_type = int(user_type)
        if user_type == account_constants.TEACHER:
            # Check if account already exists
            try:
                account = Account.objects.get(user__username=username)
            except Account.DoesNotExist:
                # Create a new User object
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=password
                )
                # Create a new Account object with the User object as its user field
                account = Account.objects.create(user=user,user_type=user_type)
    
            # Create a new Teacher object with the Account object as its user field
            teacher = Teacher.objects.create(user=account)
    
            # Serialize the new Teacher object and return it in the response
            serializer = TeacherSerializer(teacher)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"error":"usertype is not teacher"},status=status.HTTP_406_NOT_ACCEPTABLE)
    

class HelloAPIView(generics.GenericAPIView):
    """Test API view  this api is used for testing purposes"""
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        account = request.user.account
        print(account.user_type)
        content = {'message': 'Hello, World!'}
        return Response(content)