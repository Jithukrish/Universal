from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.crypto import salted_hmac

class CustomTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # Include unique user information and timestamp to generate token
        return f"{user.pk}{user.is_active}{timestamp}"

generate_token = CustomTokenGenerator()
