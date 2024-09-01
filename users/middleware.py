from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.exceptions import InvalidToken
from users.models import BlacklistedToken


class TokenBlacklistMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Get token from request headers
        token = request.headers.get("Authorization")
        if token and token.startswith("Bearer "):
            token = token[7:]  # Remove 'Bearer ' from the token

            # Check if the token is in the blacklist
            if BlacklistedToken.objects.filter(token=token).exists():
                raise InvalidToken("Token has been blacklisted.")
