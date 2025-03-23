from typing import Optional
from time import monotonic
import asyncio

from .http import AsynchronousHTTPHandler, BaseAsynchronousHTTPHandler
from ..auth import BaseAuthHandler, AuthUtil, AuthHandler
from ..scope import Scope


__all__ = ("AsynchronousAuthHandler", "BaseAsynchronousAuthHandler")


class BaseAsynchronousAuthHandler(BaseAuthHandler):
    http: BaseAsynchronousHTTPHandler

    async def get_token(self) -> Optional[str]:
        raise NotImplementedError()


class AsynchronousAuthHandler(BaseAsynchronousAuthHandler, AuthUtil):
    __slots__ = ("http", "_lock")

    def __init__(
        self,
        client_id: int,
        client_secret: str,
        redirect_url: Optional[str],
        scope: Optional[Scope] = None,
    ):
        AuthUtil.__init__(self, client_id, client_secret, redirect_url, scope)

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
        """
        `code` parameter is not required, but without a code the scopes are restricted to
        public and delegate (more on delegation below). You can obtain a code by having
        a user authorize themselves under a url which you can get with get_auth_url.
        Read more about it under that function.

        **Client Credentials Delegation**

        Client Credentials Grant tokens may be allowed to act on behalf of the owner of the OAuth client
        (delegation) by requesting the delegate scope, in addition to other scopes supporting delegation.
        When using delegation, scopes that support delegation cannot be used together with scopes that do
        not support delegation. Delegation is only available to Chat Bots. Currently, chat.write is the only
        other scope that supports delegation.

        **Parameters**

        code: Optional[str]
            code from user authorizing at a specific url
        """
        data = self._get_data("client_credentials" if code is None else "authorization_code", code)
        await self._request(data)

    async def refresh_access_token(self, refresh_token: Optional[str] = None):
        """
        This function is usually executed by HTTPHandler, but if you have a
        refresh token saved from the last session, then you can fill in the
        `refresh_token` argument which this function will use to get a valid token.

        **Parameters**

        refresh_token: Optional[str]
            A refresh token used to get a new access token.
        """
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
    def from_sync(cls, auth: AuthHandler):
        new_auth = cls(auth.client_id, auth.client_secret, auth.redirect_url, auth.scope)
        new_auth.refresh_token = auth.refresh_token
        new_auth._token = auth._token
        new_auth.expire_time = auth.expire_time
        new_auth._refresh_callback = auth._refresh_callback
        new_auth.http = auth.http.as_async(new_auth)
        return new_auth

    def as_sync(self) -> AuthHandler:
        return AuthHandler.from_async(self)
