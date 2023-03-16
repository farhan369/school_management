from django.shortcuts import render
from  django_filters.rest_framework import DjangoFilterBackend

from . import permissions
from . import models as account_models
from . import serializers as account_serializer
from . import filters

from rest_framework import generics
from rest_framework.settings import api_settings
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

# Create your views here.


class SignUpView(generics.CreateAPIView):
    """
    api for sign up
    can only be accessed by admin

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
    queryset = account_models.Account.objects.all
    serializer_class = account_serializer.AccountCreateSerializer
    permission_classes = [permissions.IsAdmin]


class ObtainAuthTokenView(ObtainAuthToken):
    """
    Handle creating user authentication tokens
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

    serializer_class = account_serializer.AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        """Handle HTTP POST request"""
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
             # Include the id field in the response
            {"token": token.key, "id": user.id} 
        )


class CreateTeacherView(generics.ListCreateAPIView):
    """
    This api creates a teacher account by an admin
    it also return list of teachers
    """
    serializer_class = account_serializer.TeacherSerializer
    permission_classes = [permissions.IsAdmin]
    queryset = account_models.Teacher.objects.all()
    filterset_class = filters.TeacherFilter


class CreateStudentView(generics.ListCreateAPIView):
    """
    This api is used for create/list student
    it can be only accessed by teacher of that class or admin
    """
    permission_classes = [permissions.IsStaff]
    serializer_class = account_serializer.StudentSerializer
    queryset = account_models.Student.objects.all()
    filterset_class = filters.StudentFilterSet

