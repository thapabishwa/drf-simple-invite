from django.conf.urls import url
from django.contrib import admin
from django.urls import path, re_path, include, reverse_lazy
from django.views.generic.base import RedirectView
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, UserCreateViewSet

router = DefaultRouter()

router.register(r'signup', UserCreateViewSet, base_name='user-create')
router.register(r'users', UserViewSet, base_name='user-list')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    url(r'api/v1/invite/', include('drf_simple_invite.urls', namespace='drf_simple_invite')),

    path('api-token-auth/', views.obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    re_path(r'^$', RedirectView.as_view(url=reverse_lazy('api-root'), permanent=False)),

]
