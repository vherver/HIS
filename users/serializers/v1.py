from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_new_password = serializers.CharField(required=True, write_only=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def validate(self, data):
        if data["new_password"] != data["confirm_new_password"]:
            raise serializers.ValidationError("New passwords do not match")
        return data

    def save(self, user):
        user = User.objects.get(pk=user.pk)
        if not user.check_password(self.validated_data["old_password"]):
            raise serializers.ValidationError("Old password is incorrect")
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user


class LogoutSerializer(serializers.Serializer):
    token = serializers.CharField()
