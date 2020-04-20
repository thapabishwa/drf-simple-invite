import base64

from django.forms.models import model_to_dict
from django.urls import reverse
from drf_simple_invite.models import InvitationToken
from faker import Faker
from nose.tools import ok_, eq_
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .factories import UserFactory, UserPasswordFactory

fake = Faker()


class TestGetRequest(APITestCase):
    def setUp(self):
        self.url = reverse('user-list-list')
        self.client = APIClient()

    def test_get_request(self):
        response = self.client.get(self.url)
        eq_(response.status_code, status.HTTP_200_OK)
