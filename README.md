# Django Rest User Invitation [![Build Status](https://travis-ci.org/thapabishwa/drf_simple_invite.svg?branch=develop)](https://travis-ci.org/thapabishwa/drf_simple_invite)

The primary aim of this python package is to provides a simple user invitation strategy for django rest framework, where users can be invited using invitation tokens (by sending email to the provided e-mail address).

This package provides a REST endpoint that verifies an token and set the password for that particular user.

## Quickstart

1. Install the package from pypi using pip:
TODO:
```bash
pip install drf-simple-invite
```

2. Add ``drf_simple_invite`` to your ``INSTALLED_APPS`` (after ``rest_framework``) within your Django settings file:
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party apps
    'rest_framework',  # utilities for rest apis
    'rest_framework.authtoken',  # token

    # Simple Invite
    'drf_simple_invite',

    # Custom User Model
    'users',
]
```

3. This package provides an endpoint, which can be included by including ``drf_simple_invite.urls`` in your ``urls.py`` as follows:
```python
from django.conf.urls import url, include


urlpatterns = [
    ...
    url(r'api/v1/invite/', include('drf_simple_invite.urls', namespace='drf_simple_invite')),
    ...
]    
```
**Note**: You can adapt the api-url to your needs.

### Endpoints

The following endpoints are provided:
 * `POST ${API_URL}/` - invite the user by sending the email as parameter
 * `POST ${API_URL}/{invitation_token}` -  set password token by using the ``invitation_token`` parameter
 
where `${API_URL}/` is the url specified in your *urls.py* (e.g., `api/v1/invite/`)
and `{invitation_token}` is `base64.urlsafe` encoded uuid token. Since it is unsafe to sendout plain uuid, always make sure that the `{invitation_token}` is `base64.urlsafe` encoded


### Configuration / Settings

The following settings can be set in Djangos ``settings.py`` file:

* `DJANGO_REST_INVITATION_TOKEN_EXPIRY_TIME` - time in hours about how long the token is active (Default: 24)

  **Please note**: expired tokens are automatically cleared based on this setting in every call of ``post`` method on this endpoint.
 
### Signals
TODO: signals must be used to send emails to the target user.

