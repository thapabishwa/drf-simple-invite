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


class TestUserSignUpTestCase(APITestCase):

    def setUp(self):
        self.url = reverse('user-create-list')
        self.user_data = model_to_dict(UserFactory.build())
        self.client = APIClient()

    def test_create_user_creates_invitation_token(self):
        response = self.client.post(self.url, self.user_data)
        eq_(response.status_code, status.HTTP_201_CREATED)
        eq_(InvitationToken.objects.all().exists(), True)


class TestSignedUpUserCreatesAndInvitesUserTestCase(APITestCase):

    def setUp(self):
        self.url = reverse('user-create-list')
        self.login_user = UserPasswordFactory.create()
        self.invite_url = reverse('drf_simple_invite:invite-user')
        self.confirm_url = reverse('drf_simple_invite:confirm-user')
        self.user_data = model_to_dict(UserFactory.build())

    def authenticate(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.login_user)

    def test_create_user_with_login(self):
        self.authenticate()
        response = self.client.post(self.url, self.user_data)
        eq_(response.status_code, status.HTTP_201_CREATED)

    def test_invite_user_with_login(self):
        self.authenticate()
        response = self.client.post(self.url, self.user_data)
        eq_(response.status_code, status.HTTP_201_CREATED)

        payload = {'email': self.user_data['email']}
        response = self.client.post(self.invite_url, payload, format='json')
        eq_(response.status_code, status.HTTP_200_OK)

    def test_set_password_success(self):
        self.authenticate()
        response = self.client.post(self.url, self.user_data)
        eq_(response.status_code, status.HTTP_201_CREATED)

        payload = {'email': self.user_data['email']}
        response = self.client.post(self.invite_url, payload, format='json')
        eq_(response.status_code, status.HTTP_200_OK)

        invitation_token = InvitationToken.objects.filter(user__email=self.user_data['email']).first()
        encoded = base64.urlsafe_b64encode(str(invitation_token.id).encode()).decode()

        payload = {'invitation_token': encoded, 'password': '`1234567890-='}
        response = self.client.post(self.confirm_url, payload, format='json')
        eq_(response.status_code, status.HTTP_201_CREATED)

        ok_(invitation_token.user.check_password('`1234567890-='))

    def test_set_password_invalid_password(self):
        self.authenticate()
        response = self.client.post(self.url, self.user_data)
        eq_(response.status_code, status.HTTP_201_CREATED)

        payload = {'email': self.user_data['email']}
        response = self.client.post(self.invite_url, payload, format='json')
        eq_(response.status_code, status.HTTP_200_OK)

        invitation_token = InvitationToken.objects.filter(user__email=self.user_data['email']).first()
        encoded = base64.urlsafe_b64encode(str(invitation_token.id).encode()).decode()

        payload = {'invitation_token': encoded, 'password': 'password'}
        response = self.client.post(self.confirm_url, payload, format='json')
        eq_(response.status_code, status.HTTP_400_BAD_REQUEST)
