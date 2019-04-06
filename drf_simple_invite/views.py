import base64

from django.conf import settings
from django.contrib.auth.password_validation import validate_password, get_password_validators
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, status, serializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from drf_simple_invite.models import InvitationToken
from drf_simple_invite.serializers import PasswordSerializer, EmailSerializer
from .models import AUTH_USER_MODEL

class SetUserPasswordViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_class = PasswordSerializer

    def create(self, request,*args, **kwargs ):
        try:
            if 'invitation_token' in kwargs:
                invitation_token = kwargs['invitation_token']
                decoded_token = base64.url_sage_b64decode(invitation_token.encode()).decode()
                invitation_token = get_object_or_404(InvitationToken, id=decoded_token)
                password = self.request.data['password']

                try:
                    validate_password(password, user=invitation_token.user, password_validators=get_password_validators(settings.AUTH_PASSWORD_VALIDATORS))
                    invitation_token.user.set_password(password)
                    invitation_token.user.save()
                    InvitationToken.objects.filter(user=invitation_token.user).delete()
                    return Response({'detail': 'Password sucessfully created.'}, status=status.HTTP_201_CREATED)
                except ValidationError as e:
                    raise serializers.ValidationError(e.messages)

            return Response({'detail': 'Cannot Find Invitation Token in the url.'}, status=status.HTTP_204_NO_CONTENT)
        except:
            pass


class InviteUserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = EmailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = request.data['email']
        try:
            users = AUTH_USER_MODEL.objects.get(email__iexact=email)
        except:
            pass
        try:
            InvitationToken.objects.create(users=users)
            return Response({'detail': 'Invite User'})
        except:
            pass
