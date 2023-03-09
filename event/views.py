from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status, views
from .models import *
from .serializers import *
from account.permissions import IsAdmin, IsStaff
# Create your views here.


class SportsFestivalView(generics.ListCreateAPIView):
    """
    View for creating and retriving sports festivals
    """
    queryset = SportsFestival.objects.all()
    serializer_class = SportsFestivalSerializer
    permission_classes = [IsAdmin]


class EventView(generics.ListCreateAPIView):
    """
    View for creating and retriving events in sports festivals
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAdmin]


class EventRegistrationView(generics.ListCreateAPIView):
    """
    View for creating and retriving student reistrations
    """
    queryset = EventRegistration.objects.all()
    serializer_class = EventRegistrationSerializer

class TryView(generics.ListCreateAPIView):
    """
    View where teachers can mark the attempts of student
    """
    queryset = Try.objects.all()
    serializer_class = TrySerializer
    permission_classes = [IsStaff]


class LeaderBoardView(generics.ListAPIView):
    """
    View will print the leaderboard having student username and result
    of every event
    """
    serializer_class = LeaderboardSerializer
    
    def get_queryset(self):
        event_id = self.kwargs.get('event_id')
        queryset = Event.objects.filter(id=event_id)
        return queryset
    
