from django.urls import path
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    # create academics url
    
    path("academicyear/", AcademicYearView.as_view(), name="createyear"),
    path("subject/", SubjectView.as_view(), name="subject"),
    path("standard/", StandardView.as_view(), name='createstandard'),
    path("classroom/", ClassroomCreateView.as_view(), name="createclassroom"),
    path("get_exam_standard_subject_id/", 
         ExamStandardSubjectView.as_view(), name='get_exam_standard_subject_id'),
    path("exam/", ExamCreateView.as_view(), name="exams"),

     # to create and get  questions and options of an exam
    path("question/", QuestionCreateView.as_view(), name='questions'),

     # to save the response of a student taking exam  
    path("question/<int:question_id>/"
         ,ResponseView.as_view(),name='response'),

     # to get result of an student
    path("exam/<int:exam_id>/result/"
         , ExamResultView.as_view(), name = 'result'),

    # to mark attendence
    path("markattendence/",MarkAttendenceView.as_view(),name='mark_attendence')
]
router.register(
    "examstandard/addsubject", ExamStandardViewSet, basename='add_subject')

urlpatterns +=router.urls