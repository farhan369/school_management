from django.db import models
import account.models

from datetime import date

# Create your models here.


class Classroom(models.Model):
    """
    Model to store Classroom details
    Attribs:
        standard : standard of class 1-12
        division : division od class A-Z ETC
        teacher  : to know which class student belongs foreign key from class Teacher in accounts
    """

    standard = models.IntegerField(null=True, blank=True, default=1)
    division = models.CharField(max_length=2, null=True, blank=True, default="A")
    teacher = models.OneToOneField(
        account.models.Teacher,
        on_delete=models.CASCADE,
        related_name="classroom",
    )
    class Meta:
        unique_together = (('standard','division'))
    def __str__(self):
        return str(self.standard) + self.division


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

    name = models.CharField(max_length=20, unique=False, blank=True)
    classroom = models.ForeignKey(
        Classroom, on_delete=models.CASCADE, related_name="exams"
    )
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    """
    Model to store values for formula fields.

    Attribs:
        Model to store all questions
        question: question itself
        exam   : foreign key to know which exam holds the question
    """

    text = models.CharField(max_length=50, blank=True, default=None)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="questions")
    mark = models.IntegerField(blank=True,default=1,null=True)

    def __str__(self):
        return self.text


class Option(models.Model):
    """
    Model to store all options
    Attribs:
    is_correct   : denotes whether the option is correct
    option       : option itself
    question     : foreign key to know which question holds the option
    """

    is_correct = models.BooleanField(null=True, blank=True, default=False)
    text = models.CharField(max_length=50, default=None, blank=True)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="options"
    )

    def __str__(self):
        return self.text


class Response(models.Model):
    """
    Model to the response a student to a question
    Attribs:
    option   :  foreign key to know which option was selected
    student  :  foreign key to know which student choose

    """

    option = models.ManyToManyField(
        Option,
        related_name="selected_options",
        blank=True,

    )
    student = models.ForeignKey(
        account.models.Student, on_delete=models.CASCADE, related_name="responses"
    )


class Enrollment(models.Model):
    """
    Model to store the relationship between a student and a classroom.
    Attribs:
    classroom : foreign key to know which class the student belongs
    student : foreign key to know which student belongs to the class
    enroll_date : date on which the student enrolled in the class
    """
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    student = models.ForeignKey(account.models.Student, on_delete=models.CASCADE)
    enroll_date = models.DateField(default=date.today)