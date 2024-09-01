from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(
        self, email: str, password: str = None, is_staff: bool = False, **extra_fields
    ):
        """
        Create a user instance with the given credentials
        :username email:
        :param password:
        :param is_staff: boolean field to indicate if user can access to django
        :return: User instance
        """

        user = self.model(email=email, is_staff=is_staff, **extra_fields)

        if password:
            user.set_password(password)

        user.save()

        return user

    def create_superuser(self, email: str, password: str):
        """
        Create superuser with the given credentials
        :param email:
        :param password:
        :return: User instance
        """
        extra_fields = {"is_staff": True, "is_superuser": True}
        return self.create_user(email, password, **extra_fields)
