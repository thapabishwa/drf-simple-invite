import uuid
import base64
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save


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


def get_invitation_token_expiry_time():
    return getattr(settings, 'DJANGO_REST_INVITATION_TOKEN_EXPIRY_TIME', 24)


@receiver(post_save, sender=InvitationToken)
def send_email(sender, instance, **kwargs):
    api_root='http://test.com/api/v1/invite/'
    encoded = base64.urlsafe_b64encode(str(instance.id).encode()).decode()
    api_root = api_root + encoded
    return send_mail('Invitation token for %s'% instance.user.email,
                    api_root, "superuser@yourdomain.com", [instance.user.email, ], fail_silently=False)