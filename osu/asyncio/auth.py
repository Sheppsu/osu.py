from typing import Optional
from time import monotonic
import asyncio

from .http import AsynchronousHTTPHandler
from ..auth import FunctionalAuthHandler, AuthHandler
from ..scope import Scope


__all__ = ("AsynchronousAuthHandler",)


class AsynchronousAuthHandler(FunctionalAuthHandler):
    __slots__ = ("http", "_lock")

    def __init__(
        self,
        client_id: int,
        client_secret: str,
        redirect_url: Optional[str],
        scope: Optional[Scope] = None,
    ):
        super().__init__(client_id, client_secret, redirect_url, scope)

        self.http: AsynchronousHTTPHandler = AsynchronousHTTPHandler(self)
        self._lock: asyncio.Lock = asyncio.Lock()

    @staticmethod
    async def _raise_for_status(resp):
        try:
            resp.raise_for_status()
        except Exception as exc:
            try:
                msg = (await resp.json())["error"]
            except:
                msg = None
            raise type(exc)(str(exc) + ": " + msg) if msg is not None else exc from None

    async def _request(self, data):
        json = await self.http.make_auth_request(data)
        self._handle_response(json)

    async def get_auth_token(self, code: Optional[str] = None):
        data = self._get_data("client_credentials" if code is None else "authorization_code", code)
        await self._request(data)

    async def refresh_access_token(self, refresh_token: Optional[str] = None):
        if refresh_token:
            self.refresh_token = refresh_token

        data = self._get_data("client_credentials" if self.refresh_token is None else "refresh_token")
        await self._request(data)

        if self._refresh_callback:
            self._refresh_callback(self)

    async def get_token(self) -> Optional[str]:
        async with self._lock:
            if self.expire_time - 5 <= monotonic():
                await self.refresh_access_token()
            return self._token

    @classmethod
    async def _from_save_data(cls, save_data: dict) -> "AsynchronousAuthHandler":
        client_id = save_data["client_id"]
        client_secret = save_data["client_secret"]
        redirect_url = save_data["redirect_url"]
        scope = Scope(*save_data["scope"].split())
        auth = cls(client_id, client_secret, redirect_url, scope)
        auth.http.set_domain(save_data["domain"])
        await auth.refresh_access_token(save_data["refresh_token"])
        return auth

    @classmethod
    async def from_save_data(cls, save_data: dict) -> "AsynchronousAuthHandler":
        awaitable = super().from_save_data(save_data)
        return await awaitable  # type: ignore

    def as_sync(self) -> AuthHandler:
        """
        Return a synchronous version of this auth handler
        """
        auth = AuthHandler(self.client_id, self.client_secret, self.redirect_url, self.scope)
        auth.refresh_token = self.refresh_token
        auth._token = self._token
        auth.expire_time = self.expire_time
        auth._refresh_callback = self._refresh_callback
        auth.http.set_domain(self.http.domain)
        return auth
