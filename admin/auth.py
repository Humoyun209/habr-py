from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.config import Settings
from app.users.auth import create_access_token
from app.users.dependencies import get_current_user


settings = Settings()


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]
        if username == "humoyun209" and password == "humo6050":
            request.session.update(
                {"token": create_access_token({"sub": username}, expired_day=5)}
            )
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return RedirectResponse(request.url_for("admin:login"))

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        if not token:
            return RedirectResponse(request.url_for("admin:login"))
        user = await get_current_user(token)
        if not user:
            return RedirectResponse(request.url_for("admin:login"))
        if user.username == "humoyun209":
            return True
        return RedirectResponse(request.url_for("admin:login"))


authentication_backend = AdminAuth(secret_key=settings.security.private_key.read_text())
