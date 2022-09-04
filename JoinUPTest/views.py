from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import User, ActivationCode, ActivationCodeType
from .serializers import UserSerializer, RegisterSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics


class UserDetailAPI(APIView):
    authentication_classes = (TokenAuthentication,)

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class ActivationView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        code_to_activate = get_object_or_404(ActivationCode, code=self.kwargs.get("code"))
        if code_to_activate.type == ActivationCodeType.SMS:
            code_to_activate.user.activate_phone()
        if code_to_activate.type == ActivationCodeType.EMAIL:
            code_to_activate.user.activate_email()

        code_to_activate.delete()
        return Response({"result": f"{code_to_activate.type} verified!"})
