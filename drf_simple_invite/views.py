from django.shortcuts import get_object_or_404
from rest_framework import renderers
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from drf_simple_invite.models import InvitationToken
from drf_simple_invite.serializers import PasswordSerializer


class InvitationTokenViewSet(mixins.CreateModelMixin, viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_classes = PasswordSerializer
    renderer_classes = (renderers.JSONRenderer, renderers.BrowsableAPIRenderer)

    def create(self):
        if 'invitation_token' in self.kwargs:
            invitation_token = get_object_or_404(InvitationToken, id=self.kwargs['invitation_token'])

            password = self.request.data['password']

            invitation_token.user.set_password(password)

            return Response({'detail': 'Password sucessfully created'}, status=status.HTTP_201_CREATED)
        return Response({'detail': 'Cannot Find Invitation Token'}, status=status.HTTP_204_NO_CONTENT)
