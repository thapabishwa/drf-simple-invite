import factory
import faker

from factory.fuzzy import (
    FuzzyChoice,
)

from drf_simple_invite.models import InvitationToken
from ..models import User

ip_address_choices = [
    '181.2.220.112',
    '247.187.59.227',
    '4.177.15.85',
    '227.135.102.239',
    '123.0.110.149',
    '197.171.88.171',
    '11.7.66.189',
    '192.99.73.179',
    '189.53.206.210',
    '43.64.249.148',
]


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    id = factory.Faker('uuid4')
    username = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_active = False
    is_staff = False
    is_verified = False
    last_login = factory.Faker('date_time')


class UserPasswordFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    id = factory.Faker('uuid4')
    username = factory.Faker('email')
    password = factory.Faker('password')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('first_name')
    is_active = True
    is_staff = True
    is_verified = True
    last_login = factory.Faker('date_time')



class InvitationTokenFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = InvitationToken

    id = factory.Faker('uuid4')
    created_at = factory.Faker('date_time')
    ip_address = FuzzyChoice(choices=ip_address_choices)
    user_agent = factory.Sequence(lambda n: f'browser{n}')
    user = factory.SubFactory(UserFactory)
