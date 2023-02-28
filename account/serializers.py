from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Account

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
        fields = ('username', 'email', 'password', 'first_name','last_name'
                  ,'user_type')
    
        
    def validate_email(self, value):
        # this function is to check whether another account exist with
        # given email
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email address must be unique')
        return value
    
    
    def create(self, validated_data):
        #this function takes the validated data as an input and 
        # saves it to the database
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data, is_active=True)
        account = Account.objects.create(user=user, **validated_data)
        return account
    
