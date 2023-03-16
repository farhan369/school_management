from django.shortcuts import render, get_object_or_404
from  django_filters.rest_framework import DjangoFilterBackend


from rest_framework import generics

from . import models as event_models
from . import serializers as event_serializers

from account import permissions
# Create your views here.


class SportsFestivalView(generics.ListCreateAPIView):
    """
    View for creating and retriving sports festivals
    """
    queryset = event_models.SportsFestival.objects.all()
    serializer_class = event_serializers.SportsFestivalSerializer
    permission_classes = [permissions.IsAdmin]
    filterset_fields = ['name']


class EventView(generics.ListCreateAPIView):
    """
    View for creating and retriving events in sports festivals
    """
    serializer_class = event_serializers.EventSerializer
    permission_classes = [permissions.IsAdmin]
    filterset_fields = ['name']

    def get_queryset(self):
        """
        Returns a queryset of event instances filtered by the 'fest_id'
        parameter passed in the URL.
        """
        fest_id = self.kwargs.get('fest_id')
        queryset = event_models.Event.objects.filter(fest_id=fest_id)
        return queryset



class EventRegistrationView(generics.CreateAPIView):
    """
    View for creating and retriving student reistrations
    """
    queryset = event_models.EventRegistration.objects.all()
    serializer_class = event_serializers.EventRegistrationSerializer

class TryView(generics.CreateAPIView):
    """
    View where teachers can mark the attempts of student
    """
    queryset = event_models.Try.objects.all()
    serializer_class = event_serializers.TrySerializer
    permission_classes = [permissions.IsStaff]


class LeaderBoardView(generics.ListAPIView):
    """
    View will print the leaderboard having student username and result
    of every event
    """
    serializer_class = event_serializers.LeaderboardSerializer
    
    def get_queryset(self):
        # to only event object requested by user
        event_id = self.kwargs.get('event_id')
        queryset = event_models.Event.objects.filter(id=event_id)
        return queryset
    
