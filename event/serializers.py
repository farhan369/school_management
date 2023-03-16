from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status

from account.serializers import StudentSerializer
from account import models as account_models

import academics

from django.contrib.auth.models import User
from django.db.models import Max,Min

from . import models as event_models
from . import constants as event_type_constants


class SportsFestivalSerializer(serializers.ModelSerializer):
    # this serilizer is for SportsFest model

    class Meta:
        model = event_models.SportsFestival
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    # this serializer is for Event model
    fest = SportsFestivalSerializer(read_only = True)
    fest_id = serializers.IntegerField(write_only = True)
    standards_eligible = serializers.ListField(write_only = True)
    class Meta:
        model = event_models.Event
        fields = ['id','name','fest','event_type','fest_id','standards_eligible','standards']
    
    def create(self, validated_data):
        standards_eligible = validated_data.pop('standards_eligible')
        event = event_models.Event.objects.create(**validated_data)
        standards_eligible = eval(standards_eligible[0])
        for standard in standards_eligible:
            classrooms = academics.models.Classroom.objects.filter(standard=standard)
            standard = event.standards.add(*classrooms)
        return event
        

class EventRegistrationSerializer(serializers.ModelSerializer):
    # this serializer is for EventRegistration model
    event = EventSerializer(read_only = True)
    event_id = serializers.IntegerField(write_only = True)
    student = StudentSerializer(read_only=True)

    class Meta:
        model = event_models.EventRegistration
        fields = ['id','event','event_id','student']

    def create(self, validated_data):
        """
        create function is overridden to check the the student 
        is eligible to register for this particular event
        """
        event_id = validated_data['event_id']
        event = event_models.Event.objects.get(id=event_id)
        student = self.context['request'].user.account.student 
        latest_enrollment = student.enrollment_set.order_by(
                            '-enroll_date').first()
        eligible_classes = event.standards.all()
        if latest_enrollment.classroom in eligible_classes :
            event_registration = event_models.EventRegistration.objects.create(
                                 event=event,student=student)
            return event_registration
        return Response({"message":"you are above the class limit"})
    

class TrySerializer(serializers.ModelSerializer):
    # this serializer is for try model
    # to mark chances of student

    event_id = serializers.IntegerField(write_only = True)
    student_username = serializers.CharField(write_only = True)
    
    class Meta:
        model = event_models.Try
        fields = ['id','event_id','student_username','result']

    def create(self, validated_data):
        """
        This create function is overridden to check 
        how many tries does the student tried already
        """
        event_id = validated_data.pop('event_id')
        student_username = validated_data.pop('student_username')
        event = event_models.Event.objects.get(id=event_id)
        student = account_models.Student.objects.get(user__user__username = student_username)
        
        try:
            event_reg = event_models.EventRegistration.objects.get(
                        student=student,event=event)
        except Exception as e:
            return Response({
                "message":"event registration not present","error":str(e)})
        tries_num = event_reg.tries.count()
        
        if tries_num >= 3:
            return Response({"error": "Student has already made 3 tries"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
        try_object = event_models.Try.objects.create(event_reg=event_reg,**validated_data)
        return try_object
            

class LeaderboardSerializer(serializers.Serializer):
    """
    this serializer recieves an event object as instance
    using that instance the leaderboard of that event is 
    returned
    Attributes:
        ret = stores the leaderboard query
        pagenumber = to store pagenumber requested by user in url
        paginator = an instance of PageNumberPagination class 
                    used for pagination
        paginated_ret = to store ret that belong to page requested by user
    """
    def to_representation(self, instance):
        # To modify behaviour of parent class
        ret = super().to_representation(instance)
        event_id = instance.id
        
        # If Distance is event type the longest distance throwed is taken
        # If Time is event type shortest time runned is taken(input in seconds)
        if instance.event_type == event_type_constants.DISTANCE:
            ret = event_models.EventRegistration.objects.filter(
                        event_id=event_id).values(
                        'student__user__user__username').annotate(
                        max_result=Max('tries__result')).order_by(
                        '-max_result','student__user__user__username')
        
        elif instance.event_type == event_type_constants.TIME:
            ret =  event_models.EventRegistration.objects.filter(
                        event_id=event_id).values(
                        'student__user__user__username').annotate(
                        max_result=Min('tries__result')).order_by(
                        'max_result','student__user__user__username')

        # Pagination each page will contain 5 results
        page_number = self.context['request'].query_params.get('page', 1)
        paginator = PageNumberPagination()
        paginator.page_size = 5
        paginated_ret = paginator.paginate_queryset(
                        ret, self.context['request'], view=self)
        return {
            'count': len(ret),
            'page_number': page_number,
            'results': paginated_ret,
        }
        


