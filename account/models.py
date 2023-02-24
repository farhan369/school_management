# Create your models here.

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True, null=True, db_index=True)
    birth_date = models.DateField(null=True, blank=True)
    USER_TYPE_CHOICES = (
      (1, 'student'),
      (2, 'teacher'),
      (3, 'admin'),
  )

    user_type = models.PositiveSmallIntegerField(default=1, choices=USER_TYPE_CHOICES)

    def __str__(self):
        return self.user.username

 
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)

"""
Model to store values for formula fields.

Attribs:
    user        : OneToOneField to get attribute of django User
    email       : Made email compulsory
    birth_date  : date of birth of the user
    user_type   : to identify whether the user is student,teacher,aadmin
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



