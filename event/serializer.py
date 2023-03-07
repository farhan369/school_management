from rest_framework import serializers
from account.models import Teacher, Account, Student
from django.contrib.auth.models import User
from .models import *
from rest_framework.response import Response
from rest_framework import status
from account.serializers import StudentSerializer

class SportsFestivalSerializer(serializers.ModelSerializer):
    # this serilizer is for SportsFest model

    class Meta:
        model = SportsFestival
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    # this serializer is for Event model
    fest = SportsFestivalSerializer(read_only = True)
    fest_id = serializers.IntegerField(write_only = True)

    class Meta:
        model = Event
        fields = ['id','name','fest','class_limit','event_type','fest_id']


class EventRegistrationSerializer(serializers.ModelSerializer):
    # this serializer is for EventRegistration model
    event = EventSerializer(read_only = True)
    event_id = serializers.IntegerField(write_only = True)
    student = StudentSerializer(read_only=True)

    class Meta:
        model = EventRegistration
        fields = ['id','event','event_id','student']

    def create(self, validated_data):
        """
        create function is overridden to check the the student 
        is eligible to register for this particular event
        """
        event_id = validated_data['event_id']
        event = Event.objects.get(id=event_id)
        student = self.context['request'].user.account.student 
        latest_enrollment = student.enrollment_set.order_by(
                            '-enroll_date').first()
        print(latest_enrollment.classroom.standard)

        if event.class_limit >= latest_enrollment.classroom.standard :
            print('hi')
            event_registration = EventRegistration.objects.create(
                                 event=event,student=student)
            print(event_registration)
            return event_registration
        return Response({"message":"you are above the class limit"})
