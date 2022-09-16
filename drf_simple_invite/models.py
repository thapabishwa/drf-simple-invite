import base64
import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from drf_simple_invite.signals import invitation_token_created

__all__ = [
    'InvitationToken',
    'get_invitation_token_expiry_time',
]


class InvitationToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(get_user_model(), related_name='invitation_tokens', on_delete=models.CASCADE,
                             verbose_name=_("The User which is associated to this invitation token"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("When was the token generated"))

    ip_address = models.GenericIPAddressField(
        _("The IP address of this session"),
        default="127.0.0.1"
    )

    user_agent = models.CharField(
        max_length=256,
        verbose_name=_("HTTP User Agent"),
        default=""
    )


@receiver(post_save, sender=get_user_model())
def create_invitation_token(sender, instance=None, created=False, **kwargs):
    if created:
        invitation_token = InvitationToken.objects.create(user=instance)
        encoded = base64.urlsafe_b64encode(str(invitation_token.id).encode()).decode()
        invitation_token_created.send(sender=sender, instance=instance, user=instance, invitation_token=encoded)


def get_invitation_token_expiry_time():
    return getattr(settings, 'DJANGO_REST_INVITATION_TOKEN_EXPIRY_TIME', 24)
