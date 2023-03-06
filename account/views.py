from django.shortcuts import render
from .permissions import IsAdmin, IsStaff
from .models import Account, Teacher, Student
from .serializers import (
    AccountCreateSerializer,
    AuthTokenSerializer,
    TeacherSerializer,
    StudentSerializer,
)
from django.contrib.auth.models import User
from . import constants as account_constants
from rest_framework import generics, permissions, status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.settings import api_settings
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from academics.models import Classroom


# Create your views here.


class SignUpView(generics.CreateAPIView):
    """
    api for sign up

    Attribs:
        queryset             : This attribute sets the queryset of Account
                               objects that will be used for this view.
        serializer_class     : This attribute sets the serializer class
                               that will be used for this view.
        permission_classes   : This attribute sets the permission
                               classes that will be used for this view
    """

    # this api creates a admin account by an admin
    # UserCreationPermission - checker whether the value provided in
    # user_type field is of ADMIN
    queryset = Account.objects.all
    serializer_class = AccountCreateSerializer
    permission_classes = [
        IsAdmin,
    ]


class ObtainAuthTokenView(ObtainAuthToken):
    """Handle creating user authentication tokens
            used to return token and id when the data
            from the serializer is validated.

            Used for login


    Attribs:
        serializer_class     : This attribute sets the serializer class
                               that will be used for this view.
        serializer           : Instance of  AuthTokenSerializer class
        user                 : This variable contains the User object
                               that was authenticated using the credentials
                               sent in the request.
        token                : stores the token generated for the authenticated
                               user.
        created              :this variable is a boolean that indicates whether
                              the token was newly created (True) or
                              retrieved from the database (False).

    Methods:
        post                 : handles the http POST request

    """

    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        """Handle HTTP POST request"""
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {"token": token.key, "id": user.id}  # Include the id field in the response
        )


class CreateTeacherView(generics.CreateAPIView):
    # this api creates a teacher account by an admin
    serializer_class = TeacherSerializer
    permission_classes = [
        IsAdmin,
    ]


class CreateStudentView(generics.CreateAPIView):
    permission_classes = [
        IsStaff,
    ]
    serializer_class = StudentSerializer
