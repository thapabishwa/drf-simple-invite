from django.urls import re_path as url
from rest_framework import routers

from drf_simple_invite.views import SetUserPasswordView, InviteUserView

router = routers.DefaultRouter()

app_name = 'drf_simple_invite'
urlpatterns = [

    url(r'^confirm', SetUserPasswordView.as_view(), name='confirm-user'),
    url(r'^', InviteUserView.as_view(), name='invite-user'),
]
