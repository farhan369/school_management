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
    #user = AccountSerilizer()
    username = serializers.CharField(source='user.username')
    id = serializers.CharField(source = 'user.id')

    class Meta:
        model = Teacher
        fields = ['username','id']

class ClassroomSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()

    class Meta:
        model = Classroom
        fields = ['id', 'standard', 'division', 'teacher']

    def create(self, validated_data):
        teacher_data = validated_data.pop('teacher')
        print(teacher_data)
        teacher = Teacher.objects.get(user_id=teacher_data['user']['id'])
        classroom = Classroom.objects.create(teacher=teacher, **validated_data)
        return classroom
