from django.shortcuts import render
from  django_filters.rest_framework import DjangoFilterBackend

from . import permissions
from . import models as account_models
from . import serializers as account_serializer
from . import constants as account_constants
from . import filters

from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, viewsets
from rest_framework.settings import api_settings
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

# Create your views here.


class AdminViewSet(viewsets.ModelViewSet):
    """
    view for managing admin accounts
    
    can only be accessed by admin,
    admin will be given username and password created in django admin
    admin can login using that credentials and add his data

    Attribs:
        queryset             : This attribute sets the queryset of Account
                               objects that will be used for this view.
        serializer_class     : This attribute sets the serializer class
                               that will be used for this view.
        permission_classes   : This attribute sets the permission
                               classes that will be used for this view
    
    Methods:                 : get,patch,delete            
    """
    
    http_method_names = ['get', 'patch', 'delete']
    permission_classes = [permissions.IsAdmin,IsAuthenticated]
    serializer_class = account_serializer.AdminSerializer
    queryset = account_models.Account.objects.filter(
        user_type=account_constants.UserType.ADMIN)
    
    def destroy(self, request, *args, **kwargs):
        """
        to deactivate an account when delete request is encountered
        """
        
        account = self.get_object()
        account.is_active = False
        account.save()
        return Response(data='account deactivated')


class LoginView(ObtainAuthToken):
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

    serializer_class = account_serializer.LoginSerializer

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


class CreateTeacherView(viewsets.ModelViewSet):
    """
    This view managing teacher model
    This view handles post and get request
    """

    permission_classes = [permissions.IsAdmin,IsAuthenticated]
    serializer_class = account_serializer.TeacherSerializer
    queryset = account_models.Teacher.objects.all()
    filterset_class = filters.TeacherFilter


class CreateStudentView(viewsets.ModelViewSet):
    """
    This view is used for create/list student
    it can be only accessed by teacher of that class or admin
    """

    http_method_names = ['get', 'patch', 'delete']
    permission_classes = [permissions.IsStaff,IsAuthenticated]
    serializer_class = account_serializer.StudentSerializer
    queryset = account_models.Student.objects.all()
    filterset_class = filters.StudentFilterSet
