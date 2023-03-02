from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Classroom
from .serializer import ClassroomSerializer
from account.permissions import IsAdmin

class ClassroomCreateView(generics.CreateAPIView):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    permission_classes = [IsAdmin]
