# Create your models here.

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

from . import constants as account_constants


class Account(AbstractUser):
    """
    Custom user model inherited from AbstractUser with additional fields.

    Inheritted Attribs:
        email       : Made email compulsory
        user_type   : to identify whether the user is student,teacher,admin
        username    : username
        first_name  : first_name of the User.
        last_name   : last name of the User.
        password    : password set for auth
        is_staff    : whether staff permission given
        is_active   : whether active
        is_superuser: whether superuser permission given
        last_login  : last login time
        date_joined : when the account was created
    """

    user_type = models.PositiveSmallIntegerField(
        default=None, choices=account_constants.UserType.USER_TYPE_CHOICES,
        null=True, blank=True
    )
    

    class Meta:
        """
        overridden to change name to Account in Django admin
        """
        
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    def __str__(self):
        """
        Returns a string representation of the object.
        """
        
        return self.username
    
    def get_fullname(self):
        """
        Returns full name of the account
        """
        
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        """
        hashes the password when account is created
        """
        
        if self.pk is None:
            self.set_password(self.password)
        super().save(*args, **kwargs)


class Student(Account):
    """
    Model to store values for student.

    Attribs:
        classroom   : to know which class student belongs
    """

    classroom = models.ManyToManyField(
        "academics.Classroom",
        default=None,
        through='academics.Enrollment',
        related_name="students",
    )
    

    class Meta:
        """ 
        overridden to change name to Account in Django admin
        """
        
        verbose_name = "Student"
        verbose_name_plural = "Students"

    def __str__(self):
        """
        Returns a string representation of the object.
        """
       
        return self.username

class Teacher(Account):
    """
    model to store teacher details . created to use as foreign key to classroom
    """

    def __str__(self):
        return self.username
    

    class Meta:
        """
        overridden to change name to Account in Django admin
        """
        
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"