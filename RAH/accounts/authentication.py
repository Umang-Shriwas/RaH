from rest_framework.authentication import TokenAuthentication

from accounts.models import MultiToken


class MultiTokenAuthentication(TokenAuthentication):
    model = MultiToken