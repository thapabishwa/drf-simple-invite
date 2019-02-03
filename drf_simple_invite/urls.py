from django.conf.urls import url,include
from django.urls import path
from rest_framework import routers
from drf_simple_invite.views import InvitationTokenViewSet

router = routers.DefaultRouter()


router.register(r'^(?P<invitation_token>.+)', InvitationTokenViewSet, base_name='invitation_token_consume')
app_name='drf_simple_invite'
urlpatterns = [
    path(r'', include(router.urls)),
]
