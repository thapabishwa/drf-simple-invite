from django.urls import reverse
from django.forms.models import model_to_dict
from django.contrib.auth.hashers import check_password
from nose.tools import ok_, eq_
from rest_framework.test import APITestCase
from rest_framework import status
from faker import Faker
from .factories import InvitationTokenFactory, UserFactory

fake = Faker()

class TestUserSignUpTestCase(APITestCase):

    def setUp(self):
        self.url = reverse('signup')
        self.user_data = model_to_dict(UserFactory.build())