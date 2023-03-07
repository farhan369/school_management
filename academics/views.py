from django.shortcuts import render

from rest_framework import generics, status
from .models import Classroom, Exam, Question, Option, Response as Responsee
from .serializer import \
ClassroomSerializer, ExamSerilalizer, QuestionSerializer, ResponseSerializer \
,ExamResultSerializer
from account.permissions import IsAdmin
from account.models import Teacher
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from account.permissions import IsAdmin

# Create your views here.

class ClassroomCreateView(generics.ListCreateAPIView):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    permission_classes = [
        IsAdmin,
    ]


@method_decorator(csrf_exempt, name="dispatch")
class ExamCreateView(generics.ListCreateAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerilalizer


class QuestionCreateView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class ResponseView(generics.ListCreateAPIView):
    queryset = Responsee.objects.all()
    serializer_class = ResponseSerializer


class ExamResultView(generics.ListAPIView):
    serializer_class = ExamResultSerializer
    queryset = Responsee.objects.all()