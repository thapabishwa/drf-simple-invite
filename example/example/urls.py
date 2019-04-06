from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/v1/invite', include('drf_simple_invite.urls', namespace='drf_simple_invite')),
]
