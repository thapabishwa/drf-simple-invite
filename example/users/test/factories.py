import factory
import faker

from drf_simple_invite.models import InvitationToken
from ..models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    id = factory.Faker('uuid4')
    username = factory.Sequence(lambda n: f'testuser{n}')
    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_active = False
    is_staff = False
    is_verified = False


class InvitationTokenFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = InvitationToken

    id = factory.Faker('uuid4')
    created_at = factory.Faker('date_time')
    ip_address = faker.ipv4_private(address_class='a')
    user_agent = factory.Sequence(lambda n: f'browser{n}')
    user = factory.SubFactory(UserFactory)
