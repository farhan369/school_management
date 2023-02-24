from django.db import models
import account.models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Classroom(models.Model):
    standard = models.IntegerField(validators=[
            MaxValueValidator(12),
            MinValueValidator(1)
        ])
    division = models.CharField(max_length=2)
    teacher  = models.ForeignKey(account.models.Teacher,on_delete=models.CASCADE)

    """
Model to store Classroom details
Attribs:
    standard : standard of class 1-12
    division : division od class A-Z ETC
    teacher  : to know which class student belongs foreign key from class Teacher in accounts
    """

class Exam(models.Model):
    examname      = models.CharField(max_length=20,unique=False)
    classroom = models.ForeignKey(Classroom,on_delete=models.CASCADE)
    start_time    = models.DateTimeField()
    end_time      = models.DateTimeField()

"""
Model to store values for formula fields.

Attribs:
    Model to store all exam details
    examname    : name of exam
    classroom   : foreign key to know which class is eligible to write exam
    start_time  : time when exam can be written
    end_time    : time when exam is expired
    """

class Question(models.Model):
    Questionname = models.CharField(max_length=50)
    exam         = models.ForeignKey(Exam,on_delete=models.CASCADE)

"""
Model to store values for formula fields.

Attribs:
    Model to store all questions
    Questionname: question itself
    exam   : foreign key to know which exam holds the question
    """

class Option(models.Model):
    is_correct = models.BooleanField()
    optionname = models.CharField(max_length=50)
    question   = models.ForeignKey(Question,on_delete=models.CASCADE)
"""
    Model to store all options 
    Attribs:
    is_correct   : denotes whether the option is correct
    optionname   : option itself
    question     : foreign key to know which question holds the option
    """

class Response(models.Model):
    option      = models.ForeignKey(Option, on_delete=models.CASCADE)
    student     = models.ForeignKey(account.models.Student,on_delete=models.CASCADE)
    
"""
    Model to the response a student to a question
    Attribs:
    option   :  foreign key to know which option was selected
    student  :  foreign key to know which student choose 
    
    """