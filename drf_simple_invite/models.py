import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model



class InvitationToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(get_user_model(), related_name='invitation_tokes', on_delete=models.CASCADE,
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


    def __str__(self):
        return "Invitation token for user %s is %s." % (user, id)
    


def get_invitation_token_expiry_time():
    return getattr(settings, 'DJANGO_REST_INVITATION_TOKEN_EXPIRY_TIME', 24)
