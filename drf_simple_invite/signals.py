import django.dispatch

__all__ = [
    'invitation_token_created',
    'pre_password_creation',
    'post_password_creation'
]
invitation_token_created = django.dispatch.Signal()

pre_password_creation = django.dispatch.Signal()

post_password_creation = django.dispatch.Signal()
