import django.dispatch

__all__ = [
    'invitation_token_created',
    'pre_password_creation',
    'post_password_creation'
]
invitation_token_created = django.dispatch.Signal(
    providing_args=["instance", "invitation_token", "user"],
)

pre_password_creation = django.dispatch.Signal(providing_args=["user"])

post_password_creation = django.dispatch.Signal(providing_args=["user"])
