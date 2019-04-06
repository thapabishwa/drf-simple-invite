import django.dispatch

invitation_token_created = django.dispatch.Signal(
    providing_args=["instance", "invite_token"],
)

pre_token_creation = django.dispatch.Signal(providing_args=["user"])

post_token_creation = django.dispatch.Signal(providing_args=["user"])