from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.auth import authenticate

from . import models as account_models
from . import constants as account_constants

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status

from academics.models import Classroom


class AdminSerializer(serializers.ModelSerializer):
    """
    This class  serialize Account object
    """

    password = serializers.CharField(write_only=True)


    class Meta:
        """ 
        this class define the model and 
        the variables that need to be serialized in order
        """
        
        model = account_models.Account
        fields = (
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "user_type",
        )

         
    # def validate_email(self, value):
    #     # this function is to check whether another account exist with
    #     # given email
    #     if User.objects.filter(email=value).exists():
    #         raise serializers.ValidationError('Email address must be unique')
    #     return value
        

    def update(self, instance, validated_data):
        """ overriden to check whether the instance is of request user"""
        
        user = self.context['request'].user
        if user != instance:
            raise serializers.ValidationError(
                "You can only update your own account.")
        print(validated_data)
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
            instance.save()

        return super().update(instance, validated_data)


class TeacherSerializer(serializers.ModelSerializer):
    """
    Serilizer used to serialize Teacher Object

    Attribs:   
        Teacher Object attribtes : [username,email,first_name,last_name
                                   ,last_name ,user_type,password]
    """

    password = serializers.CharField(write_only=True)
 

    class Meta:
        """
        A class that defines metadata for a Django ModelForm for Teacher.
        """

        model = account_models.Teacher
        fields = (
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "user_type",
        )
    
    def create(self, validated_data):
        """overriden to check whether user is of teacher"""
        user_type = validated_data["user_type"]
        if user_type == account_constants.UserType.TEACHER:
            return super().create(validated_data)
        else:
            raise ValidationError("user is not of type teacher")


class StudentSerializer(serializers.ModelSerializer):
    """
    Serilizer used to create Student Object
    """

    password = serializers.CharField(write_only=True)
    classroom_id = serializers.IntegerField(write_only=True)


    class Meta:
        """
        A class that defines metadata for a Django ModelForm for Student.
        """

        model = account_models.Student
        fields = (
            "username",
            "email",
            "classroom",
            "password",
            "first_name",
            "last_name",
            "user_type",
            "classroom_id",
            )

    def create(self, validated_data):
        """
        overridden to check if user is student and
        request teacher belong to given classroom
        """
        user_type = validated_data["user_type"]
        classroom_id = validated_data.pop('classroom_id')

        if user_type == account_constants.UserType.STUDENT:
            try:
                classroom = Classroom.objects.get(
                    id=classroom_id)
            except:
                raise ObjectDoesNotExist("given classroom doesn't exist")
            request_user_type = self.context["request"].user.user_type
            request_user_type = int(request_user_type)

            if request_user_type == account_constants.UserType.TEACHER:
                class_teacher_id = classroom.teacher.id
                if class_teacher_id != self.context["request"].user.id:
                    raise ValidationError(
                        "teacher doesn't belong to this classroom")

            student =  super().create(validated_data)
            student.classroom.add(classroom)
            student.save()
            return student


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
        """validate username and password and returns token"""
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )
            if not user:
                msg = "Unable to authenticate with provided credentials"
                raise serializers.ValidationError(msg, code="authentication")

        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user

        # Create or update the user's token
        token, _ = Token.objects.get_or_create(user=user)
        attrs["token"] = token.key
        attrs["id"] = user.id
        return attrs
