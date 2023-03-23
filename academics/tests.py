from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APIClient,APITestCase

from . import models as academics_models

from account import models as account_models
from account import constants as account_constants

class ClassroomCreateViewTestCase(APITestCase):
    """
    Tests for the ClassroomCreateView view,
    which allows creating and listing Classroom instances.
    """
    def setUp(self):
        self.admin_user = User.objects.create(
            username='admin',
            email='admin@example.com',
            password='password',
            first_name='farhann',
            last_name='fmm'
        )
        self.admin_account = account_models.Account.objects.create(
            user = self.admin_user,
            user_type = account_constants.UserType.ADMIN
        )
        self.teacher_user = User.objects.create(
            username='teacher91',
            email='teacher@example.com',
            password='password',
            first_name='farhann',
            last_name='fmm'        
        )
        self.teacher_account = account_models.Account.objects.create(
            user = self.teacher_user,
            user_type = account_constants.UserType.TEACHER
        )
        self.teacher = account_models.Teacher.objects.create(
            user=self.teacher_account
        )
        self.classroom_data = {
            'standard':'5',
            'division':'P',
            'teacher_username':'teacher91'
        }
        self.url = reverse('createclassroom')

    def test_create_classroom(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(self.url, self.classroom_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(academics_models.Classroom.objects.count(),1)
        self.assertEqual(
            academics_models.Classroom.objects.first().teacher, self.teacher)
        
    def test_create_classroom_with_non_existing_teacher_username(self):
        self.client.force_authenticate(user=self.admin_user)
        invalid_data = self.classroom_data.copy()
        invalid_data['teacher_username'] = 'invalid_username'
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(academics_models.Classroom.objects.count(), 0) 
    
