from django.shortcuts import render
from rest_framework import generics, status
from .models import *
from .serializer import *
from account.permissions import IsAdmin
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


class EventRegistrationView(generics.CreateAPIView):
    """
    View for creating and retriving student reistrations
    """
    queryset = Event.objects.all()
    serializer_class = EventRegistrationSerializer

