from django.db import models
import account.models
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

class Classroom(models.Model):
    """
Model to store Classroom details
Attribs:
    standard : standard of class 1-12
    division : division od class A-Z ETC
    teacher  : to know which class student belongs foreign key from class Teacher in accounts
    """
    standard = models.IntegerField(null=True,blank=True,default=1)
    division = models.CharField(max_length=2,null=True,blank=True,default='A')
    teacher  = models.ForeignKey(account.models.Teacher,on_delete=models.CASCADE)

   

class Exam(models.Model):
    """
Model to store values for formula fields.

Attribs:
    Model to store all exam details
    exam        : name of exam
    classroom   : foreign key to know which class is eligible to write exam
    start_time  : time when exam can be written
    end_time    : time when exam is expired
    """
    exam          = models.CharField(max_length=20,unique=False,blank=True)
    classroom     = models.ForeignKey(Classroom,on_delete=models.CASCADE)
    start_time    = models.DateTimeField(null=True,blank=True)
    end_time      = models.DateTimeField(null=True,blank=True)



class Question(models.Model):
    """
Model to store values for formula fields.

Attribs:
    Model to store all questions
    question: question itself
    exam   : foreign key to know which exam holds the question
    """
    question = models.CharField(max_length=50,blank=True,default=None)
    exam     = models.ForeignKey(Exam,on_delete=models.CASCADE)



class Option(models.Model):
    """
    Model to store all options 
    Attribs:
    is_correct   : denotes whether the option is correct
    option       : option itself
    question     : foreign key to know which question holds the option
    """
    is_correct = models.BooleanField(null=True,blank=True,default=False)
    option     = models.CharField(max_length=50,default=None,blank=True)
    question   = models.ForeignKey(Question,on_delete=models.CASCADE)


class Response(models.Model):
    """
    Model to the response a student to a question
    Attribs:
    option   :  foreign key to know which option was selected
    student  :  foreign key to know which student choose 
    
    """
    option      = models.ManyToManyField(Option,related_name='selected_options',blank=True,)
    student     = models.ForeignKey(account.models.Student,on_delete=models.CASCADE)
    
