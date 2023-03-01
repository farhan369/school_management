from rest_framework.permissions import BasePermission
from . import constants as account_constants
from rest_framework.response import Response

class UserTypePermission(BasePermission):
    """ this class is used to create a custom permission 
        such that only admins are allowed to create
        account for students and teaches
    """

    def has_permission(self, request, view):
        account   = request.user.account
        user_type = account.user_type
        user_type = int(user_type)
        return user_type == account_constants.ADMIN
    

class AdminCreationPermission(BasePermission):
    #checks whether the request is to make a admin account
    def has_permission(self, request, view):
        
        user_type = request.data.get('user_type')
        user_type = int(user_type)
    
        return user_type == account_constants.ADMIN 
        

class TeacherCreationPermission(BasePermission):
    #checks whether the new creating user is Teacher
    def has_permission(self, request, view):
        
        user_type = request.data.get('user_type')
        user_type = int(user_type)
    
        return user_type == account_constants.TEACHER 
    
class StudentCreationPermission(BasePermission):
    #checks whether the new creating user is Student
    def has_permission(self, request, view):
        
        user_type = request.data.get('user_type')
        user_type = int(user_type)
    
        return user_type == account_constants.STUDENT 
             
        


