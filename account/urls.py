from django.urls import path
from .views import *
from .excels import *


urlpatterns = [
    # create admin url
     path("signup/", SignUpView.as_view(), name="signup"),

     # login returns AuthToken
     path("login/", ObtainAuthTokenView.as_view(), name="login"),

     # to create and get all teacher instances (can filter by classroom)
     path("teacher/", CreateTeacherView.as_view(), name="createteacher"),

     # to create and get all student instances (can filter by classroom)
     path("student/", CreateStudentView.as_view(), name="createstudent"),
    
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
