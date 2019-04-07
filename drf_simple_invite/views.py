import base64

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password, get_password_validators
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import status, serializers, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from drf_simple_invite.models import InvitationToken
from drf_simple_invite.serializers import PasswordSerializer, EmailSerializer
from drf_simple_invite.signals import invitation_token_created


class SetUserPasswordView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            invitation_token = request.data['invitation_token']
            decoded_token = base64.urlsafe_b64decode(invitation_token.encode()).decode()
            invitation_token = get_object_or_404(InvitationToken, id=decoded_token)
        except Exception as e:
            raise serializers.ValidationError({'detail': 'Invalid Invitation Token'})

        try:
            password = request.data['password']
            validate_password(password, user=invitation_token.user,
                              password_validators=get_password_validators(settings.AUTH_PASSWORD_VALIDATORS))
            invitation_token.user.set_password(password)
            invitation_token.user.is_active = True
            invitation_token.user.save()
            InvitationToken.objects.filter(user=invitation_token.user).delete()
        except ValidationError as e:
            raise serializers.ValidationError({e.messages})

        return Response({'detail': 'Password sucessfully created.'}, status=status.HTTP_201_CREATED)


class InviteUserView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EmailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data['email']
        user = get_object_or_404(get_user_model(), email=email)

        if user.is_active:
            raise serializers.ValidationError({'detail': 'Cannot Invite Active User'})

        invitation_token = InvitationToken.objects.create(user=user)
        encoded = base64.urlsafe_b64encode(str(invitation_token.id).encode()).decode()
        invitation_token_created.send(sender=self.__class__, instance=self, invitation_token=encoded)
        return Response({'detail': 'Invite User Done'}, status=status.HTTP_200_OK)
