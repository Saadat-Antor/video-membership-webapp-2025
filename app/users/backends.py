from starlette.authentication import (
    AuthenticationBackend,
    SimpleUser,
    UnauthenticatedUser,
    AuthCredentials
)
from . import auth

class JWTCookieBackend(AuthenticationBackend):
    async def authenticate(self, request):
        session_id = request.cookies.get("cookies")
        user_data = auth.verify_user_id(session_id)
        if user_data is None:
            role = ["anon"]
            return AuthCredentials(role), UnauthenticatedUser()
        user_id = user_data.get("user_id")
        roles = ['authenticated']
        return AuthCredentials(roles), SimpleUser(user_id)