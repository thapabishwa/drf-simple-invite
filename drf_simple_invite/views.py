import base64

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password, get_password_validators
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, status, serializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import InvitationToken
from .serializers import PasswordSerializer, EmailSerializer


class SetUserPasswordViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_class = PasswordSerializer

    def create(self, request, *args, **kwargs):
        if 'invitation_token' in kwargs:
            invitation_token = kwargs['invitation_token']
            decoded_token = base64.urlsafe_b64decode(invitation_token.encode()).decode()
            invitation_token = get_object_or_404(InvitationToken, id=decoded_token)
            password = self.request.data['password']

            try:
                validate_password(password, user=invitation_token.user,
                                  password_validators=get_password_validators(settings.AUTH_PASSWORD_VALIDATORS))
                invitation_token.user.set_password(password)
                invitation_token.user.is_active = True
                invitation_token.user.save()
                InvitationToken.objects.filter(user=invitation_token.user).delete()
                return Response({'detail': 'Password sucessfully created.'}, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                raise serializers.ValidationError(e.messages)

        return Response({'detail': 'Cannot Find Invitation Token in the url.'}, status=status.HTTP_204_NO_CONTENT)


class InviteUserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = EmailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data['email']
        users = get_object_or_404(get_user_model(), email=email)
        InvitationToken.objects.create(user=users)
        return Response({'detail': 'Invite User Done'}, status=status.HTTP_200_OK)
