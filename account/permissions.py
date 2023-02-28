from rest_framework.permissions import BasePermission
from . import constants as account_constants
from rest_framework.response import Response

class UserTypePermission(BasePermission):
    """ this class is used to create a custom permission 
        such that only admins are allowed to create
        account for students and teaches
    """

    def has_permission(self, request, view):
        user_type = request.user.user_type
        return user_type == account_constants.ADMIN 
    

class UserCreationPermission(BasePermission):
    #checks whether the request is to make a admin account
    def has_permission(self, request, view):
        
        user_type = request.data.get('user_type')
        user_type = int(user_type)
    
        if user_type == account_constants.ADMIN :
            return True
        


