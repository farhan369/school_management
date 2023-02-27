# Create your models here.

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from . import constants as account_constants



class Account(models.Model):

    """
Model to store values for user fields.

Attribs:
    user        : OneToOneField to get attribute of django User
    email       : Made email compulsory
    birth_date  : date of birth of the user
    user_type   : to identify whether the user is student,teacher,admin
Inherited Attribs:
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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True, null=True, db_index=True)
    birth_date = models.DateField(null=True, blank=True)
    user_type = models.PositiveSmallIntegerField(default=2, choices=account_constants.USER_TYPE_CHOICES,null=True,blank=True)

    def __str__(self):
        return self.user.username

 
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)


class Student(models.Model):
    """
Model to store values for student.

Attribs:
    user        : OneToOneField to get attribute of Account
    classroom   : to know which class student belongs
    
    """
    user            = models.OneToOneField(Account,on_delete=models.CASCADE,primary_key=True)
    classroom       = models.ForeignKey('academics.Classroom',on_delete=models.CASCADE,default=1)


class Teacher(models.Model):
    """
model to store teacher details . created to use as foreign key to class
Attribs:
    user : OneToOneField to get attribute of Account
    """
    user     = models.OneToOneField(Account,on_delete=models.CASCADE,primary_key=True)

    
