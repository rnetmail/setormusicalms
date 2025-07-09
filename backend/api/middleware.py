# backend/api/middleware.py

import logging

logger = logging.getLogger(__name__)

class AuthDebugMiddleware:
    """
    Middleware para debug de autenticação
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log headers de autorização
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if auth_header:
            logger.info(f"Authorization header found: {auth_header[:20]}...")
        else:
            logger.info("No Authorization header found")
            
        # Log user info
        if hasattr(request, 'user') and request.user.is_authenticated:
            logger.info(f"Authenticated user: {request.user.username}")
        else:
            logger.info("User not authenticated")

        response = self.get_response(request)
        return response

