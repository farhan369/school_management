from django.db import models
import account.models
from django.core.validators import MaxValueValidator, MinValueValidator
from . import constants as event_constants


# Create your models here.
class SportsFestival(models.Model):
    """
Model to store sports_festival details
Attribs:
    fest        : name of the fest
    from_date   : start date of fest
    to_date     : end date of fest
    """
    fest         = models.CharField(max_length=20)
    from_date    = models.DateField(null=True,blank=True)
    to_date      = models.DateField(null=True,blank=True)
    


class Event(models.Model):
    """
    Model to store Event details
Attribs:
    event        : name of the event
    fest         : shows which fest this event belongs to
    class_limit  : to know upto which class standard this event is open to
    start_time   : when the event starts
    end_time     : when the event ends 
    event_type   : type of event showing whether time or distance is used to declare the winner
    """

    
    event          = models.CharField(max_length=25,blank=True,default=None)
    fest           = models.ForeignKey(SportsFestival,on_delete=models.CASCADE)
    class_limit    = models.IntegerField(null=True,blank=True,default=2)
    start_time     = models.DateTimeField(null=True,blank=True)
    end_time       = models.DateTimeField(null=True,blank=True)
    event_type     = models.IntegerField(default=event_constants.TIME,choices=event_constants.EVENT_TYPE_CHOICE,null=True,blank=True)
    

class EventRegistration(models.Model):
    """
Model to store which student register to which event details
Attribs:
    event   : foriegn key of the event
    student : foriegn key of student
    """
    event   = models.ForeignKey(Event,on_delete=models.CASCADE)
    student = models.ForeignKey(account.models.Student,on_delete=models.CASCADE)


class Try(models.Model):
    """
Model to store the score of each attempt of student details
Attribs:
    event_reg : foriegn key of the event registration table
    try_no    : counts the attempt max=3
    result    : store the score of each attempt
    """
    event_reg = models.ForeignKey(EventRegistration,on_delete=models.CASCADE)
    try_no    = models.IntegerField(null=True,blank=True,default=2)
    result   = models.IntegerField(null=True,blank=True,default=2)
    