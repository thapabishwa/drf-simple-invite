# Python Imports
import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
# Django Imports
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
# DRF Imports
from rest_framework.authtoken.models import Token

# Project Imports
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    User represents an entity who can log into the application.
    A user has at least one profile and may belong to one or many companies.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    email = models.EmailField(blank=False, null=False, unique=True)

    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=False, null=False)

    username = models.CharField(null=True, max_length=100)

    USERNAME_FIELD = 'email'
    objects = UserManager()

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )

    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as active. ''Unselect this instead of deleting '
            'accounts. '
        ),
    )

    is_verified = models.BooleanField(_('verified'),
                                      default=False,
                                      help_text=_('Designates whether this user is verified or not.'))

    class Meta:
        ordering = ['email']

    def __str__(self):
        return self.email


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
