from django.urls import path
from .views import *
from .excels import *


urlpatterns = [
    # create admin url
     path("signup/", SignUpView.as_view(), name="signup"),
     path("login/", ObtainAuthTokenView.as_view(), name="login"),
     path("createteacher/", CreateTeacherView.as_view(), name="createteacher"),
     path("createstudent/", CreateStudentView.as_view(), name="createstudent"),
    
    #excel urls
     path("teacher/classroomexport/<int:classroom_id>",
         ClassroomExport.as_view(), name="classroomexprot"),
     path("student/<int:student_id>/generateexcel",
          StudentReportExport.as_view(), name="student_report"),
     path("schoolmembers/",SchoolMembers.as_view(), name="school_report"),
     path("teacherreport/",BestTeacher.as_view(), name="teacher_report"),

]
