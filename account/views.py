from django.shortcuts import render
from .permissions import IsAdmin,IsStaff
from .models import Account ,Teacher,Student
from .serializers import AccountCreateSerializer,AuthTokenSerializer \
                        ,TeacherSerializer,StudentSerializer
from django.contrib.auth.models import User
from . import constants as account_constants
from rest_framework import generics,permissions,status
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
    queryset           = Account.objects.all
    serializer_class   = AccountCreateSerializer
    permission_classes = [IsAdmin, ]




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
    """
class to store values for user fields.

Attribs:
    
    serializer_class         : This attribute sets the serializer class
                               that will be used for this view. 
    permission_classes       : This attribute sets the permission 
                               classes that will be used for this view
    Teacher Object attrubtes : [username,email,first_name,last_name,last_name 
                                ,user_type]
    account                  : to store instance of Account
    user                     : to store instance of User that is created
    teacher                  : to store instance of Teacher that is created
    serializer               : Instance of  TeacherSerilizer class

"""

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
    


class CreateStudentView(generics.CreateAPIView):
    """This api creates a student and assign class to him
        only admin and teacher assigned to that class can 
        do it


Attribs:
    
    serializer_class         : This attribute sets the serializer class
                               that will be used for this view. 
    permission_classes       : This attribute sets the permission 
                               classes that will be used for this view
    Student Object attrubtes : [username,email,first_name,last_name,last_name 
                                ,user_type,classroom]
    account                  : to store instance of Account
    user                     : to store instance of User that is created
    student                  : to store instance of Student that is created
    serializer               : Instance of  StudentSerializer class
    request_user_type        : to store the user_type of user requesting 
                               request

    """
    permission_classes = [IsStaff]
    serializer_class = StudentSerializer

    def post(self, request, *args, **kwargs):
        # Extract student data from request body
        username = request.data.get('username')
        email = request.data.get('email')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        password = request.data.get('password')
        user_type = request.data.get('user_type')
        user_type = int(user_type)
        class_id = request.data.get('classroom')
        
        # Checks if the user type is of student
        if user_type == account_constants.STUDENT:
            try:
                """This try except block check if the classroom 
                    exists
                """
                classroom = Classroom.objects.get(id = class_id)
                account   = request.user.account
                request_user_type = account.user_type
                request_user_type = int(request_user_type)
                # Checks whether the teacher is assigned to the given class
                if request_user_type == account_constants.TEACHER:
                    class_teacher_id = classroom.teacher.user.user.id
                    if class_teacher_id != request.user.id:
                        return Response({'error':'teacher is not assigned to this class'})
                    
                
            except Exception as e:
                return Response({'error':str(e),'user':"classroom doesn't exist"},status=status.HTTP_404_NOT_FOUND)


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
    
            # Create a new Student object with the Account object as its user field
            student = Student.objects.create(user=account,classroom = classroom)
    
            # Serialize the new Student object and return it in the response
            serializer = StudentSerializer(student)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"error":"usertype is not student"},status=status.HTTP_406_NOT_ACCEPTABLE)

class HelloAPIView(generics.GenericAPIView):
    """Test API view  this api is used for testing purposes"""
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        account = request.user.account
        print(account.user_type)
        content = {'message': 'Hello, World!'}
        return Response(content)