from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializers
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterUserView(APIView):

    def post(self, request):
        reg_serializer = RegisterSerializers(data=request.data)
        if reg_serializer.is_valid():
            user = reg_serializer.save()
            if user:
                return Response(status=status.HTTP_201_CREATED)
        return Response(reg_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlacklistTokenView(APIView):

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)