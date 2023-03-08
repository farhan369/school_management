from django.urls import path
from .views import *

urlpatterns = [
    path("", SportsFestivalView.as_view(), name='fest'),
    path("events/", EventView.as_view(), name='events'),
    path("events/register/", EventRegistrationView.as_view(),
          name='event_register'),
    path("events/mark/", TryView.as_view(),name='mark_chance'),
    path("events/<int:event_id>/leaderboard/", LeaderBoardView.as_view(), name='leaderboard')

]
