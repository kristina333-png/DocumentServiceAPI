from typing import Optional, Tuple

from rest_framework import authentication
from rest_framework import exceptions
from .models import ExternalSystem


class APIKeyAuthentication(authentication.BaseAuthentication):
    """
       Аутентификация внешних систем по API-ключу.
       Ключ передаётся в заголовке X-API-Key.
       """
    def authenticate(self, request) -> Optional[Tuple[ExternalSystem, None]]:

        api_key = request.headers.get('X-API-Key')

        if not api_key:
            raise exceptions.AuthenticationFailed('API ключ не предоставлен')

        try:
            external_system = ExternalSystem.objects.get(api_key=api_key, is_active=True)
        except ExternalSystem.DoesNotExist:
            raise exceptions.AuthenticationFailed('Неверный API ключ')

        return (external_system, None)