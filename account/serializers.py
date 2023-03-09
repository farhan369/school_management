from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Account, Teacher, Student
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from . import constants as account_constants
from rest_framework.response import Response
from rest_framework import status
from academics.serializers import ClassroomSerializer
from academics.models import Classroom


class AccountCreateSerializer(serializers.ModelSerializer):
    """
    This class  serialize Account object
    """
    # This serializer is used to create an admin user

    username = serializers.CharField(source="user.username")
    email = serializers.EmailField(source="user.email")
    password = serializers.CharField(source="user.password", write_only=True)
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")

    class Meta:
        # this class define the model and the variables that need to be
        # serialized in order
        model = Account
        fields = (
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "user_type",
        )

    """     
    def validate_email(self, value):
        # this function is to check whether another account exist with
        # given email
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email address must be unique')
        return value
        """

    # To create Account object in DataBase before creating account 
    # We need to create user account so create method is overridden
    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user_type = validated_data["user_type"]

        if user_type == account_constants.ADMIN:
            user = User.objects.create_user(**user_data, is_active=True)
            account = Account.objects.create(user=user, **validated_data)
            return account
        return Response(
            {"error": "user is not of type ADMIN"}, status=status.HTTP_401_UNAUTHORIZED
        )


class TeacherSerializer(serializers.ModelSerializer):
    """
    Serilizer used to serialize Teacher Object
    """

    """
    class to store values for user fields.

    Attribs:   
        Teacher Object attrubtes : [username,email,first_name,last_name
                                   ,last_name ,user_type]
        account                  : to store instance of Account
        user                     : to store instance of User that is created
        teacher                  : to store instance of Teacher that is created
"""
    username = serializers.CharField(source="user.user.username")
    email = serializers.EmailField(source="user.user.email")
    password = serializers.CharField(source="user.user.password", write_only=True)
    first_name = serializers.CharField(source="user.user.first_name")
    last_name = serializers.CharField(source="user.user.last_name")
    user_type = serializers.IntegerField(source="user.user_type")


    class Meta:
        model = Teacher
        fields = (
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "user_type",
        )

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        # To store user data to user object
        user_type = user_data["user_type"]
        user = User.objects.create_user(**user_data["user"])
        account = Account.objects.create(user=user, user_type=user_type)
        teacher = Teacher.objects.create(user=account)
        return teacher


class StudentSerializer(serializers.ModelSerializer):
    """
    Serilizer used to create Student Object
    """

    username = serializers.CharField(source="user.user.username")
    email = serializers.EmailField(source="user.user.email")
    password = serializers.CharField(source="user.user.password", write_only=True)
    first_name = serializers.CharField(source="user.user.first_name")
    last_name = serializers.CharField(source="user.user.last_name")
    class_room = serializers.IntegerField(write_only=True)
    user_type = serializers.IntegerField(source="user.user_type")

    class Meta:
        model = Student
        fields = (
            "username",
            "email",
            "classroom",
            "password",
            "first_name",
            "last_name",
            "user_type",
            "class_room",
        )

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user_type = user_data["user_type"]

        if user_type == account_constants.STUDENT:
            try:
                """
                This try except block check if the classroom
                exists
                """
                classroom = Classroom.objects.get(id=validated_data["class_room"])
                account = self.context["request"].user.account
                request_user_type = account.user_type
                request_user_type = int(request_user_type)
                # Checks whether the teacher is assigned to the given class
                if request_user_type == account_constants.TEACHER:
                    print('3')
                    class_teacher_id = classroom.teacher.user.user.id
                    if class_teacher_id != self.context["request"].user.id:
                        return Response(
                            {"error": "teacher is not assigned to this class"},
                            status=status.HTTP_406_NOT_ACCEPTABLE,
                        )

            except Exception as e:
                return Response(
                    {"error": str(e), "app_data": "classroom doesn't exist"},
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )
            user = User.objects.create_user(**user_data["user"])
            account = Account.objects.create(user=user, user_type=user_type)
            class_room = Classroom.objects.get(id=validated_data["class_room"])
            student = Student.objects.create(user=account)
            student.classroom.set([class_room])
            return student
        else:
            return print("user is not student")



class AuthTokenSerializer(serializers.Serializer):
    """
    This is a serializer for the Django Rest Framework authentication
    token.The authentication token provides a way to authenticate users using
    an API key.


    inputs :
        username of user
        password of user

    process :
        validate username and password

    output :
        token
    """

    username = serializers.CharField()
    password = serializers.CharField()
    id = serializers.IntegerField(read_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            # checks if username and password enetered
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )

            if not user:
                # if user object is not created the credentials were incorrect
                msg = "Unable to authenticate with provided credentials"
                raise serializers.ValidationError(msg, code="authentication")

        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code="authorization")

        try:
            # we are retrieving the account object associated with user
            # using  'user.account' synntax
            account = user.account
        except Account.DoesNotExist:
            msg = "User account not found"
            raise serializers.ValidationError(msg, code="authentication")

        # using the one to one field of model 'user' to set atributes of
        # Account model
        attrs["user"] = account.user

        # Create or update the user's token
        token, _ = Token.objects.get_or_create(user=user)
        attrs["token"] = token.key
        attrs["id"] = account.user.id
        return attrs
