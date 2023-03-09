from rest_framework.permissions import BasePermission
from . import constants as account_constants
from rest_framework.response import Response
from rest_framework import status
from academics.models import Classroom
from django.conf import settings
from rest_framework.authtoken.models import Token
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
        try:
            account = request.user.account
            user_type = account.user_type
            if user_type == account_constants.ADMIN:
                return True
            else:
                return False
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class IsStaff(BasePermission):
    """
    this class is used to create a custom permission such that
    classteacher or admin assigned to a class are given access
    Attributes:
        account   : to store instance of Account
        user_type : to store users_type of Account Instance
    """

    def has_permission(self, request, view):
        # access the account to get user_type associated with user
        user_type = request.user.account.user_type
        access_users = [account_constants.ADMIN, account_constants.TEACHER]
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
        try:
            account = request.user.account
            user_type = account.user_type
            if user_type == account_constants.STUDENT:
                return True
            else:
                return False
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)