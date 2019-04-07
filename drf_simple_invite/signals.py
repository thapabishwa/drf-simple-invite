import django.dispatch
__all__ =[
    'invitation_token_created',
    'pre_token_creation',
    'post_token_creation'
]
invitation_token_created = django.dispatch.Signal(
    providing_args=["instance", "invitation_token"],
)

pre_token_creation = django.dispatch.Signal(providing_args=["user"])

post_token_creation = django.dispatch.Signal(providing_args=["user"])