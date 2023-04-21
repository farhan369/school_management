from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics,viewsets

from . import models as academics_models
from . import serializers as academics_serializers
from . import filters as academics_filters

import account.permissions


# Create your views here.
class AcademicYearView(generics.CreateAPIView):
    """ view for creating an academic year"""
    
    permission_classes = [account.permissions.IsAdmin]
    serializer_class = academics_serializers.AcademicYearSerilizer
    queryset = academics_models.AcademicYear.objects.all()


class SubjectView(generics.ListCreateAPIView):
    """view for creating an subject"""
   
    permission_classes = [account.permissions.IsAdmin]
    serializer_class = academics_serializers.SubjectSerializer
    queryset = academics_models.Subject.objects.all()


class StandardView(generics.CreateAPIView):
    """view for creating a subject"""
    
    permission_classes = [account.permissions.IsAdmin]
    serializer_class = academics_serializers.StandardSerializer
    queryset = academics_models.Standard.objects.all()


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
    
    permission_classes = [account.permissions.IsAdmin]
    serializer_class = academics_serializers.ClassroomSerializer
    filterset_fields = ['standard','division']
    queryset = academics_models.Classroom.objects.all()
    

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

class ExamStandardViewSet(viewsets.ModelViewSet):
    """
    view to get ExamStandard id using filters and
    to add subjects to the ExamStandard object 
    """
    
    permission_classes = [account.permissions.IsStaff]
    serializer_class = academics_serializers.ExamStandardSerializer
    filterset_class = academics_filters.ExamStandardFilter
    queryset = academics_models.ExamStandard.objects.all()


class ExamStandardSubjectView(generics.ListAPIView):
    """
    view to get ExamStandardSubject id using filters
    
    this id can be passed through header in QuestionCreateView
    to know which exampaper this question belongs
    """
    
    permission_classes = [account.permissions.IsStaff]
    serializer_class = academics_serializers.ExamStandardSubjectSerializer
    filterset_class = academics_filters.ExamStandardSubjectFilter
    queryset = academics_models.ExamStandardSubject.objects.all()


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
        queryset = academics_models.ExamStandardSubject.objects.filter(id=exam_id)
        return queryset
    

class MarkAttendenceView(generics.CreateAPIView):
    """
    View for marking attendence for teachers and students

    permissions:
    - Only teacher and students can mark attendence
    """
    
    permission_classes = [account.permissions.IsStudent |
                           account.permissions.IsTeacher]
    serializer_class = academics_serializers.MarkAttendence
    queryset = academics_models.Attendance.objects.all()
    
    
    
