from django.shortcuts import render
from  django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics

from . import models as academics_models
from . import serializers as academics_serializers

import account.permissions


# Create your views here.

class ClassroomCreateView(generics.ListCreateAPIView):
    """
    View for creating and listing classroom instances.

    GET:
    Returns a list of all existing classrooms.

    POST:
    Creates a new classroom instance.

    Permissions:
    - Only users with 'admin' role can access this view.
    """
    queryset = academics_models.Classroom.objects.all()
    serializer_class = academics_serializers.ClassroomSerializer
    permission_classes = [account.permissions.IsAdmin]
    filterset_fields = ['standard','division']
    

class ExamCreateView(generics.ListCreateAPIView):
    """
    View for creating and listing Exam instances.

    GET:
    Returns a list of all existing Exams.

    POST:
    Creates a new exam instance.

    Permissions:
    - Only users with 'admin or teacher' role can access this view.
    """
    serializer_class = academics_serializers.ExamSerilalizer
    permission_classes = [account.permissions.IsStaff]
    filterset_fields = ['name']

    def get_queryset(self):
        """
        Returns a queryset of exam instances filtered by the 'classroom_id'
        parameter passed in the URL.
        """
        classroom_id = self.kwargs.get('id')
        queryset = academics_models.Exam.objects.filter(classroom_id=classroom_id)
        return queryset


class QuestionCreateView(generics.ListCreateAPIView):
    """
    View for creating and listing Question instances.

    GET:
    Returns a list of all existing Question instances.

    POST:
    Creates a new question instance.

    Permissions:
    - Only users with 'admin or teacher' role can access this view.
    """
    queryset = academics_models.Question.objects.all()
    serializer_class = academics_serializers.QuestionSerializer
    permission_classes = [account.permissions.IsStaff]
    filterset_fields = ['mark','text']

    def get_queryset(self):
        """
        Returns a queryset of question instances filtered by the 'exam_id'
        parameter passed in the URL.
        """
        exam_id = self.kwargs.get('exam_id')
        queryset = academics_models.Question.objects.filter(exam_id=exam_id)
        return queryset


class ResponseView(generics.CreateAPIView):
    """
    View for creating response instances.

    POST:
    Creates a new response instance.

    Permissions:
    - Only users with 'student' role can access this view.
    """
    queryset = academics_models.Response.objects.all()
    serializer_class = academics_serializers.ResponseSerializer
    permission_classes = [account.permissions.IsStudent]


class ExamResultView(generics.ListAPIView):
    """
    View for listing exam results for a specific exam.

    Permissions:
    - Only authenticated users can access this view.
    """
    serializer_class = academics_serializers.ExamResultSerializer

    def get_queryset(self):
        """
        Returns a queryset of exam instances filtered by the 'exam_id'
        parameter passed in the URL.
        """
        exam_id = self.kwargs.get('exam_id')
        queryset = academics_models.Exam.objects.filter(id=exam_id)
        return queryset
    

class MarkAttendenceView(generics.CreateAPIView):
    """
    View for marking attendence for teachers and students

    permissions:
    - Only teacher and students can mark attendence
    """
    queryset = academics_models.Attendance.objects.all()
    permission_classes = [account.permissions.IsStudent |
                           account.permissions.IsTeacher]
    serializer_class = academics_serializers.MarkAttendence
    
