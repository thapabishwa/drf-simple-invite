import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class InvitationToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(AUTH_USER_MODEL, related_name='invitation_tokes', on_delete=models.CASCADE,
                             verbose_name=_("The User which is associated to this invitation token"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("When was the token generated"))


def get_invitation_token_expiry_time():
    return getattr(settings, 'DJANGO_REST_INVITATION_TOKEN_EXPIRY_TIME', 24)
