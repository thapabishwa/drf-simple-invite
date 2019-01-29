from django.conf.urls import url

from drf_simple_invite.views import InvitationTokenViewSet

app_name = 'invitation_token'

urlpatterns = [
    url(r'^(?P<invitation_token>.+)/', InvitationTokenViewSet, name="reset-password-confirm"),
]
