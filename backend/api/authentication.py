# backend/api/authentication.py

from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions
import logging

logger = logging.getLogger(__name__)

class CustomTokenAuthentication(TokenAuthentication):
    """
    Token authentication customizada com logs para debug
    """
    
    def authenticate(self, request):
        auth = self.get_authorization_header(request).split()
        
        if not auth or auth[0].lower() != self.keyword.lower().encode():
            logger.info(f"No valid auth header. Received: {auth}")
            return None

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            logger.error(msg)
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header. Token string should not contain spaces.'
            logger.error(msg)
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
            logger.info(f"Token received: {token[:10]}...")
        except UnicodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            logger.error(msg)
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)
    
    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
            logger.info(f"Token found for user: {token.user.username}")
        except model.DoesNotExist:
            logger.error(f"Token not found in database: {key[:10]}...")
            raise exceptions.AuthenticationFailed('Invalid token.')

        if not token.user.is_active:
            logger.error(f"User inactive: {token.user.username}")
            raise exceptions.AuthenticationFailed('User inactive or deleted.')

        logger.info(f"Authentication successful for user: {token.user.username}")
        return (token.user, token)

