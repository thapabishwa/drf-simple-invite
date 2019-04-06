from django.conf.urls import include
from django.urls import path
from rest_framework import routers

from .views import SetUserPasswordViewSet, InviteUserViewSet

router = routers.DefaultRouter()

router.register(r'confirm/(?P<invitation_token>.+)', SetUserPasswordViewSet, base_name='confirm_user')
router.register(r'', InviteUserViewSet, base_name='invite_user')
app_name = 'drf_simple_invite'
urlpatterns = [
    path(r'', include(router.urls)),
]
