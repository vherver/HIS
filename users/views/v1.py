from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import BlacklistedToken
from users.serializers.v1 import ChangePasswordSerializer, LogoutSerializer


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data["old_password"]):
                return Response(
                    {"detail": "Old password is incorrect"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user.set_password(serializer.validated_data["new_password"])
            user.save()
            return Response(
                {"detail": "Password has been updated"}, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data["token"]

            BlacklistedToken.objects.create(token=token)

            return Response(
                {"detail": "Successfully logged out"}, status=status.HTTP_204_NO_CONTENT
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
