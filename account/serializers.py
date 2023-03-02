from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Account,Teacher,Student
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from . import constants as account_constants
from rest_framework.response import Response
from rest_framework import status
from academics.serializer import ClassroomSerializer




class AccountCreateSerializer(serializers.ModelSerializer):

    # This serializer is used to create an admin user 
    

    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    password = serializers.CharField(source='user.password', write_only=True)
    first_name = serializers.CharField(source='user.first_name')    
    last_name = serializers.CharField(source='user.last_name')
    
    
    class Meta:
        # this class define the model and the variables that need to be
        # serialized in order
        model = Account
        fields = ('id','username', 'email', 'password', 'first_name','last_name'
                  ,'user_type')
    
    """     
    def validate_email(self, value):
        # this function is to check whether another account exist with
        # given email
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email address must be unique')
        return value
        """
    
    # to create Account object in DataBase
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_type = validated_data['user_type']
        print(user_type)

        if user_type == account_constants.ADMIN:
            
            user = User.objects.create_user(**user_data,is_active = True)
            account = Account.objects.create(user=user, **validated_data)
            return account
            


class TeacherSerializer(serializers.ModelSerializer):
    """ Serilizer used to create Teacher Object
    """
    user = AccountCreateSerializer(required=True)

    class Meta:
        model = Teacher
        fields = ('user',)

class StudentSerializer(serializers.ModelSerializer):
    """ Serilizer used to create Student Object
    """
    user      = AccountCreateSerializer(required=True)
    classroom = ClassroomSerializer(required = True)


    class Meta:
        model = Student
        fields = ('user','classroom')






   

class AuthTokenSerializer(serializers.Serializer):
    """This is a serializer for the Django Rest Framework authentication 
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
    
    


    

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

    
        if username and password:
            # checks if username and password enetered
            user = authenticate(request=self.context.get('request'),
                                username=username,password=password)
            

            if not user:
                # if user object is not created the credentials were incorrect
                msg = 'Unable to authenticate with provided credentials'
                raise serializers.ValidationError(msg,code='authentication')


        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')
        

        try:
            # we are retrieving the account object associated with user
            # using  'user.account' synntax
            account = user.account
        except Account.DoesNotExist:
            msg = 'User account not found'
            raise serializers.ValidationError(msg, code='authentication')
        
        # using the one to one field of model 'user' to set atributes of
        # Account model
        attrs['user'] = account.user

        # Create or update the user's token
        token, _ = Token.objects.get_or_create(user=user)
        attrs['token'] = token.key
        attrs['id']=account.user.id
        return attrs




    