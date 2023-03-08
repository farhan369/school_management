from django.db import models

import account.models
import academics.models

from . import constants as event_constants


# Create your models here.
class SportsFestival(models.Model):
    """
    Model to store sports_festival details
    Attribs:
        name        : name of the fest
        from_date   : start date of fest
        to_date     : end date of fest
    """

    name = models.CharField(max_length=20)
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    """
    Model to store Event details
    Attribs:
        name        : name of the event
        fest         : shows which fest this event belongs to
        class_limit  : to know upto which class standard this event is open to
        start_time   : when the event starts
        end_time     : when the event ends
        event_type   : type of event showing whether time or distance is used to declare the winner
    """

    name = models.CharField(max_length=25, blank=True, default=None)
    fest = models.ForeignKey(
           SportsFestival, on_delete=models.CASCADE, related_name="events")
    standards = models.ManyToManyField(academics.models.Classroom,
                related_name="events", blank=True, default=None)
    event_type = models.IntegerField(
                 default=event_constants.TIME,
                 choices=event_constants.EVENT_TYPE_CHOICE,
                 null=True,blank=True)

    def __str__(self):
        return self.name

class EventRegistration(models.Model):
    """
    Model to store which student register to which event details
    Attribs:
        event   : foriegn key of the event
        student : foriegn key of student
    """

    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="eventregistrations"
    )
    student = models.ForeignKey(
        account.models.Student,
        on_delete=models.CASCADE,
        related_name="eventregistrations",
    )


class Try(models.Model):
    """
    Model to store the score of each attempt of student details
    Attribs:
        event_reg : foriegn key of the event registration table
        try_no    : counts the attempt max=3
        result    : store the score of each attempt
    """

    event_reg = models.ForeignKey(
        EventRegistration, on_delete=models.CASCADE, related_name="tries"
    )
    result = models.FloatField(null=True, blank=True, default=2)



