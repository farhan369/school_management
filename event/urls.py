from django.urls import path
from .views import *

urlpatterns = [
    # to create and list fests
    path("", SportsFestivalView.as_view(), name='fest'),

    # to create and list events in a fest 
    path("<int:fest_id>/events/", EventView.as_view(), name='events'),

    # to register for an event for students
    path("events/register/", EventRegistrationView.as_view(),
          name='event_register'),
    
    # to mark the students tries in an event for staffs
    path("events/mark/", TryView.as_view(),name='mark_chance'),

    # returns leaderboard of a event
    path("events/<int:event_id>/leaderboard/", 
        LeaderBoardView.as_view(), name='leaderboard')

]
