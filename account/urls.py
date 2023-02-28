from django.urls import path
from .views import *


urlpatterns = [
    #admin signup url
    path('signup/',SignUpView.as_view(),name='signup')
]