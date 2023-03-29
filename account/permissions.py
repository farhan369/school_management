from . import constants as account_constants

from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import BasePermission

from academics.models import Classroom

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.exceptions import BadRequest


class IsAdmin(BasePermission):
    """
    this class is used to create a custom permission
    such that only admins are given access
    Attributes:
        account   : to store instance of Account
        user_type : to store users_type of Account Instance
    """

    def has_permission(self, request, view):
        """This function checks if user of type ADMIN"""
        try:
            user_type = request.user.user_type
            if user_type == account_constants.UserType.ADMIN:
                return True
            else:
                return False
        except:
            raise ValidationError("not a valid user")


class IsStaff(BasePermission):
    """
    this class is used to create a custom permission such that
    classteacher or admin assigned to a class are given access
    Attributes:
        account   : to store instance of Account
        user_type : to store users_type of Account Instance
    """

    def has_permission(self, request, view):
        """check if user type is teacher or student"""
        
        user_type = request.user.user_type
        access_users = [
            account_constants.UserType.ADMIN,
            account_constants.UserType.TEACHER
            ]
        if user_type in access_users:
            return True
        else:
            return False


class IsStudent(BasePermission):
    """
    this class is used to create a custom permission
    such that only students are given access
    Attributes:
    account   : to store instance of Account
    user_type : to store users_type of Account Instance
    """

    def has_permission(self, request, view):
        """check if user type is student"""
        
        try:
            user_type = request.user.user_type
            if user_type == account_constants.STUDENT:
                return True
            else:
                return False
        except Exception as e:
            raise ValidationError('not a valid user')
        

class IsTeacher(BasePermission):
    """
    this class is used to create a custom permission
    such that only teacher are given access
    Attributes:
    account   : to store instance of Account
    user_type : to store users_type of Account Instance
    """

    def has_permission(self, request, view):
        """check if user type is teacher"""
        
        try:
            user_type = request.user.user_type
            if user_type == account_constants.TEACHER:
                return True
            else:
                return False
        except Exception as e:
            raise ValidationError('not a valid user')