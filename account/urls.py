from django.urls import path
from . import views as account_views
from .excels import *
from rest_framework import routers

router = routers.DefaultRouter()


urlpatterns = [
     # login returns AuthToken
     path("login/", account_views.ObtainAuthTokenView.as_view(), name="login"),

     # to create and get all teacher instances (can filter by classroom)
     path("teacher/", account_views.CreateTeacherView.as_view(), name="createteacher"),

     # to create and get all student instances (can filter by classroom)
     path("student/", account_views.CreateStudentView.as_view(), name="createstudent"),
    
    #excel urls

     #returns an excel of classroom's academic and event data
     path("teacher/classroomexport/<int:classroom_id>",
         ClassroomExport.as_view(), name="classroomexprot"),

     # returns an excel containing student's exam performances
     path("student/<int:student_id>/generateexcel",
          StudentReportExport.as_view(), name="student_report"),

     # returns an excel containg all active users in the school
     path("schoolmembers/",SchoolMembers.as_view(), name="school_report"),

     # returns an excel containg list of teachers sorted by their performance
     path("teacherreport/",BestTeacher.as_view(), name="teacher_report"),

]
router.register('admin',account_views.AdminViewSet,basename='admin')
urlpatterns += router.urls