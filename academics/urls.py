from django.urls import path
from .views import *

urlpatterns = [
    # create academics url
    path("createclassroom/", ClassroomCreateView.as_view(), name="createclassroom"),
    path("classroom/<int:id>/exam/", ExamCreateView.as_view(), name="exams"),
    path("classroom/<int:id>/exam/<int:exam_id>/question/"
         ,QuestionCreateView.as_view(),name='questions'),
    path("classroom/<int:id>/exam/<int:exam_id>/question/<int:question_id>/"
         ,ResponseView.as_view(),name='response'),
    path("classroom/<int:id>/exam/<int:exam_id>/student/<int:student_id>/"
         , ExamResultView.as_view(), name = 'result')
]
