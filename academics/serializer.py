from rest_framework import serializers
from account.models import Teacher,Account
from django.contrib.auth.models import User
from .models import Classroom


class AccountSerilizer(serializers.ModelSerializer):

    # This serializer is of Account Model 
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

class TeacherSerializer(serializers.ModelSerializer):
    # this serializer is for Teacher MOdel
    user = AccountSerilizer()
    class Meta:
        model = Teacher
        fields = ['user',]

class ClassroomSerializer(serializers.ModelSerializer):
    # this serilizer is for Classroom
    teacher = TeacherSerializer()

    class Meta:
        model = Classroom
        fields = ['id', 'standard', 'division', 'teacher']


