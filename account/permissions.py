from rest_framework.permissions import BasePermission
from . import constants as account_constants
from rest_framework.response import Response
from rest_framework import status
class IsAdmin(BasePermission):
    """ this class is used to create a custom permission 
        such that only admins are given access
    """

    def has_permission(self, request, view):
        account   = request.user.account
        user_type = account.user_type
        user_type = int(user_type)
        if user_type == account_constants.ADMIN:
            return True
        else:
            return Response({'error': "you are not an admin"}, 
                            status=status.HTTP_403_FORBIDDEN)
        
class IsStaff(BasePermission):
    """this class is used to create a custom permission such that 
       teacher or admin assigned to a class are given access
    Attributes:
                account   : to store instance of Account
                user_type : to store users_type of Account Instance



    """
    def has_permission(self, request, view):

        account   = request.user.account # access the account associated with user
        user_type = account.user_type
        user_type = int(user_type)
        if user_type == account_constants.TEACHER or user_type == account_constants.ADMIN:
            return True
        else:
            return Response({'error': "you are not a staff"}, 
                                status=status.HTTP_403_FORBIDDEN)
             
        


