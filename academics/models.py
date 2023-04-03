from django.db import models

from . import constants as academics_constants

from datetime import date


class AcademicYear(models.Model):
    """
    To store the value for academics year for a school
    
    Attributes:
        year : to store academic year value
    """
    
    start_year = models.IntegerField(
        default=2020,
        blank=True,
        unique=True
    )
    end_year = models.IntegerField(
        default=2020,
        blank=True,
        unique=True
    )

    class Meta:
        """to give unique together constraint"""
        
        unique_together  = (('start_year','end_year'))
    
    def __str__(self):
        """returns string representation the AcademicYear object"""
        
        return f'{self.start_year}-{self.end_year}'


class Standard(models.Model):
    """
    to store standard of a class
    
    Attributes:
        name : to store detail of standard
    """
    
    name = models.IntegerField(
        blank=True,
        default=1,
        unique=True
    )

    def __str__(self):
        """returns string representation the Standard object"""
        
        return f'{self.name}'
    

class Subject(models.Model):
    """
    To store the subjects available in a school
    
    Attributes:
        name : to store name of the subject
    """

    name = models.CharField(
        max_length=25,
        blank=True,
        default="",
        unique=True
    )

    def __str__(self):
        """returns string representation the Subject object"""
  
        return self.name


class Classroom(models.Model):
    """
    Model to store Classroom details
    
    Attribs:
        standard : foriegn key from model standard
        division : division od class A-Z ETC
        teacher  : to know which class student belongs foreign key from class Teacher in accounts
    """

    standard = models.ForeignKey(
        Standard,
        on_delete=models.CASCADE,
        related_name='classrooms',
        default=None
        )
    division = models.IntegerField(
        choices= academics_constants.Divisions.choices(),
        blank=True, 
        default=academics_constants.Divisions.A
        )
    teacher = models.ForeignKey(
        'account.Teacher',
        on_delete=models.CASCADE,
        related_name="classroom",
        )
    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.CASCADE,
        related_name='classrooms'
    )
    subjects = models.ManyToManyField(
        Subject,
        related_name='classroom_subjects'
    )

    class Meta:
        """overriden to give unique together constraint"""
        
        unique_together = (('standard','division','academic_year'))
        unique_together = (('teacher','academic_year'))
    
    def __str__(self):
        """returns string representaion of a class like 10-H"""
        
        division = self.division
        div = academics_constants.Divisions.get_division_by_value(division)
        return f'{self.standard.name}-{div}-{self.academic_year.start_year}'


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

    name = models.CharField(
        max_length=20,
        unique=False, 
        blank=True, 
        default=""
        )
    standard = models.ManyToManyField(
        Standard, 
        related_name="exam_standards",
        through='ExamStandard'
        )
    start_date = models.DateField(
        null=True, 
        blank=True, 
        default=None
        )
    end_date = models.DateField(
        null=True, 
        blank=True, 
        default=None
        )
    academics_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.CASCADE,
        related_name='exams',
        default=None
    )

    class Meta:
        """overriden to give unique together constraint"""
        
        unique_together = (("academics_year","name"))
    
    def __str__(self):
        """returns string representation of exam"""
        
        return self.name

class ExamStandard(models.Model):
    """
    Model representing a specific standard for an exam and 
    subjects of an exam

    Attributes:
        exam : foreign key from exam model
        standard : foreign key from standard model
        subjects : manytomany field of subject model

    """
    
    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
    )
    standard = models.ForeignKey(
        Standard,
        on_delete=models.CASCADE
    )
    subjects = models.ManyToManyField(
        Subject,
        through='ExamStandardSubject'
    )


class ExamStandardSubject(models.Model):
    """
    Model representing a subject in a exam_standard

    Attributes:
        exam_standard : foreign from ExamStandard model
        subject : foreign key from Subject Model
    """
    
    exam_standard = models.ForeignKey(
        ExamStandard,
        on_delete=models.CASCADE
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE
    )

    class Meta:
        """overriden to give unique together constraint"""
        
        unique_together = (("exam_standard","subject"))


class Question(models.Model):
    """
    Model to store values for formula fields.

    Attribs:
        Model to store all questions
        question: question itself
        exam   : foreign key to know which exam holds the question
    """

    text = models.CharField(
        max_length=50,
        blank=True,
        default=""
        )
    exam = models.ForeignKey(
        ExamStandardSubject,
        on_delete=models.CASCADE, 
        related_name="questions",
        )
    mark = models.IntegerField(
        blank=True,
        default=1,
        null=True
        )

    def __str__(self):
        """returns string representation of this object"""
        
        return self.text


class Option(models.Model):
    """
    Model to store all options
    
    Attribs:
        is_correct   : denotes whether the option is correct
        option       : option itself
        question     : foreign key to know which question holds the option
    """

    is_correct = models.BooleanField(
        default=False
        )
    text = models.CharField(
        max_length=50,
        default="",
        blank=True
        )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="options",
        )

    def __str__(self):
        """returns string representation of object """
       
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
        default=None
    )
    student = models.ForeignKey(
        'account.Student', 
        on_delete=models.CASCADE,
        related_name="responses"
        )


class Enrollment(models.Model):
    """
    Model to store the relationship between a student and a classroom.
    
    Attribs:
        classroom : foreign key to know which class the student belongs
        student : foreign key to know which student belongs to the class
        enroll_date : date on which the student enrolled in the class
    """
    classroom = models.ForeignKey(
        Classroom,
        on_delete=models.CASCADE
        )
    student = models.ForeignKey(
        'account.Student',
        on_delete=models.CASCADE
        )
    enroll_date = models.DateField(
        default=date.today
        )

    def __str__(self):
        """returns string representation of object enrollment"""
        
        return f'{self.student} - {self.classroom}'


class Attendance(models.Model):
    """
    Model to store attendance of students and teachers.
    
    Attribs:
        user       : ForeignKey to get the user id of Account
        date       : date for which attendance is taken
        is_present : whether the user is present or absent on the given date
    """
    
    user = models.ForeignKey(
        'account.Account',
        on_delete=models.CASCADE
        )
    date = models.DateField(
        default=date.today
        )
    is_present = models.BooleanField(
        default=False
        )

    def __str__(self):
        """
        String Representation of attendence instance
        """
        
        status = 'Present' if self.is_present else 'Absent'
        return f'{self.user.username} - {status} on {self.date}'
    


    

        
        