from django.db import models
import account.models
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class Sports_festival(models.Model):
    festname    = models.CharField(max_length=20)
    from_date    = models.DateField()
    to_date      = models.DateField()
    """
Model to store sports_festival details
Attribs:
    festname : name of the fest
    from_date : start date of fest
    to_date  : end date of fest
    """


class Event(models.Model):
    EVENT_TYPE_CHOICE = (
        (0,'Time'),
        (1,'Distance'),
    )
    
    eventname   = models.CharField(max_length=25)
    fest        = models.ForeignKey(Sports_festival,on_delete=models.CASCADE)
    class_limit = models.IntegerField()
    start_time    = models.DateTimeField()
    end_time      = models.DateTimeField()
    event_type = models.IntegerField(default=0,choices=EVENT_TYPE_CHOICE)
    """
    Model to store Event details
Attribs:
    eventname    : name of the event
    fest         : shows which fest this event belongs to
    class_limit  : to know upto which class standard this event is open to
    start_time   : when the event starts
    end_time     : when the event ends 
    event_type   : type of event showing whether time or distance is used to declare the winner
    """

class Event_registration(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    student = models.ForeignKey(account.models.Student,on_delete=models.CASCADE)
"""
Model to store which student register to which event details
Attribs:
    event : foriegn key of the event
    student : foriegn key of student
    """

class Try_result(models.Model):
    eventreg = models.ForeignKey(Event_registration,on_delete=models.CASCADE)
    tryno    = models.IntegerField(validators=[
            MaxValueValidator(3),
            MinValueValidator(1)
        ])
    result   = models.IntegerField()
    """
Model to store the score of each attempt of student details
Attribs:
    eventreg : foriegn key of the event registration table
    tryno    : counts the attempt max=3
    result   : store the score of each attempt
    """