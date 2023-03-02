from django.urls import path
from .views import *


urlpatterns = [
    #create admin url
    path('signup/',SignUpView.as_view(),name='signup'),
    path('login/',ObtainAuthTokenView.as_view(),name='login'),
    path('hello/', HelloAPIView.as_view(), name='hello'),
    path('createteacher/',CreateTeacherView.as_view(),name='createteacher'),
    path('createstudent/',CreateStudentView.as_view(),name='createstudent'),


]   