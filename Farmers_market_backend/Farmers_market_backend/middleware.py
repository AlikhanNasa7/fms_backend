from channels.db import database_sync_to_async
from jwt import decode as jwt_decode, ExpiredSignatureError
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from users.models import CustomUser
from channels.auth import AuthMiddlewareStack

@database_sync_to_async
def get_user_from_token(token):
    try:
        print(token)
        decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return CustomUser.objects.get(pk=decoded_data["user_id"])
    except (ExpiredSignatureError, CustomUser.DoesNotExist, KeyError):
        return AnonymousUser()


class TokenAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        query_string = scope["query_string"].decode()
        token = None

        if "token=" in query_string:
            token = query_string.split("token=")[-1]

        scope["user"] = await get_user_from_token(token) if token else AnonymousUser()

        return await self.inner(scope, receive, send)


# Middleware stack with token authentication
TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))
