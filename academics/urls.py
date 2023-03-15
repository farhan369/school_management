from django.urls import path
from .views import *

urlpatterns = [
    # create academics url
    
     # to create and get list of classes
     path("classroom/", ClassroomCreateView.as_view(), name="createclassroom"),
     
     # to create and get list of exams active to a class
     path("classroom/<int:id>/exam/", ExamCreateView.as_view(), name="exams"),

     # to create and get  questions and options of an exam
     path("classroom/<int:id>/exam/<int:exam_id>/question/"
         ,QuestionCreateView.as_view(),name='questions'),

     # to save the response of a student taking exam  
     path("classroom/<int:id>/exam/<int:exam_id>/question/<int:question_id>/"
         ,ResponseView.as_view(),name='response'),

     # to get result of an student
     path("classroom/<int:id>/exam/<int:exam_id>/student/<int:student_id>/"
         , ExamResultView.as_view(), name = 'result'),

    # to mark attendence
    path("markattendence/",MarkAttendenceView.as_view(),name='mark_attendence')
]
