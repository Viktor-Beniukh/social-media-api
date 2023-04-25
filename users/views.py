from django.contrib.auth import logout
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics, views, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from users.models import User
from users.serializers import UserSerializer, AuthTokenSerializer


class UserViewSet(viewsets.ViewSet):
    authentication_classes = (TokenAuthentication, )

    @staticmethod
    def list(request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    @staticmethod
    def retrieve(request, pk):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    serializer_class = AuthTokenSerializer


class UserLogoutView(views.APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            request.user.auth_token.delete()
            logout(request)
            return Response(
                {"message": "You logged out. Token revoked successfully."},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "You are not logged in."},
                status=status.HTTP_400_BAD_REQUEST
            )


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
