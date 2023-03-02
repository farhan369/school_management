from django.urls import path
from .views import *

urlpatterns = [
    #create academics url
        path('createclassroom/',ClassroomCreateView.as_view(),name='createclassroom'),

]