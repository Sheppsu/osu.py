from time import monotonic
from typing import Callable, Optional, Union
from collections.abc import Awaitable
import threading

from .scope import Scope
from .exceptions import ScopeException
from .http import HTTPHandler, BaseHTTPHandler


__all__ = ("BaseAuthHandler", "FunctionalAuthHandler", "AuthHandler")


class BaseAuthHandler:
    """
    An abstract class for implementing authentication logic.
    """

    scope: Scope
    http: BaseHTTPHandler

    def get_token(self) -> Optional[str]:
        """
        Returns the access token. If the token is expired, it will be refreshed before being returned.
        """
        raise NotImplementedError()

    def has_user(self) -> bool:
        raise NotImplementedError()


class FunctionalAuthHandler(BaseAuthHandler):
    """
    Abstract class that helps to go through the oauth process easily, as well as refresh
    tokens without the user needing to worry about it.

    Certain functions expect that the `_http` attribute is defined by classes implementing this one.

    .. note::
        If you're not authorizing a user with a url for a code, this does not apply to you.
        AuthHandler does not save refresh tokens past the program finishing.
        AuthHandler will save the refresh token to refresh the access token
        while the program is running, so make sure to save the refresh token
        before shutting down the program, so you can use it to get a valid access token
        without having the user reauthorize.

    **Init Parameters**

    client_id: int
        Client id

    client_secret: str
        Client secret

    redirect_uri: str
        Redirect uri

    scope: Optional[:class:`Scope`]
        Scopes to authorize under. Default is :func:`Scope.default`.
    """

    __slots__ = (
        "client_id",
        "client_secret",
        "redirect_url",
        "scope",
        "refresh_token",
        "_token",
        "expire_time",
        "_refresh_callback",
    )

    SAVE_VERSION = 2

    def __init__(
        self,
        client_id: int,
        client_secret: str,
        redirect_url: Optional[str],
        scope: Optional[Scope] = None,
    ):
        super().__init__()

        if scope is None:
            scope = Scope.default()

        if scope == "lazer":
            raise ScopeException("The lazer scope signifies that an endpoint only meant for use by the lazer client.")
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_url = redirect_url
        self.scope = scope

        self.refresh_token = None
        self._token = None
        self.expire_time = monotonic()
        self._refresh_callback = None

    def _get_data(self, grant_type, code=None):
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": grant_type,
        }

        data.update(
            {
                "client_credentials": {"scope": self.scope.scopes},
                "authorization_code": {"code": code, "redirect_uri": self.redirect_url},
                "refresh_token": {"refresh_token": self.refresh_token},
            }[grant_type]
        )

        return data

    def _handle_response(self, data):
        if "refresh_token" in data:
            self.refresh_token = data["refresh_token"]
        self._token = data["access_token"]
        self.expire_time = monotonic() + data["expires_in"]

    def get_auth_url(self, state: Optional[str] = ""):
        """
        Returns a url that a user can authorize their account at. They'll then be returned to
        the redirect_uri with a code that can be used under get_auth_token.

        **Parameters**

        state: Optional[str]
            Will be returned to the redirect_uri along with the code.
        """
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_url,
            "response_type": "code",
            "scope": self.scope.scopes,
            "state": state,
        }
        if not params["state"]:
            del params["state"]
        return self.http.auth_url + "?" + "&".join([f"{key}={value}" for key, value in params.items()])

    def has_user(self):
        """
        Returns whether this auth has access to endpoints requiring a user
        """
        return "delegate" in self.scope or self.refresh_token is not None

    def set_refresh_callback(self, callback: Callable[["FunctionalAuthHandler"], None]):
        """
        Set a callback to be called everytime the access token is refreshed.

        **Parameters**

        callback: :class:`Callable[['AuthHandler'], None]`
        """
        self._refresh_callback = callback

    def get_save_data(self):
        """
        Get save data in json format. Can be used to easily initiate a new :class:`AuthHandler` object
        in a new session.

        **Returns**

        {

        'save_version': int,

        'client_id': int,

        'client_secret': str,

        'redirect_url': str,

        'scope': str,

        'refresh_token': str,

        'domain': str,

        }
        """
        return {
            "save_version": self.SAVE_VERSION,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_url": self.redirect_url,
            "scope": self.scope.scopes,
            "refresh_token": self.refresh_token,
            "domain": self.http.domain,
        }

    @classmethod
    def from_save_data(cls, save_data: dict) -> "FunctionalAuthHandler":
        """
        Create a new :class:`FunctionalAuthHandler` object from save data.
        """
        save_version = save_data["save_version"]
        if save_version != cls.SAVE_VERSION:
            raise ValueError(
                f"The version of this save data ({save_version}) is not compatible "
                f"with the save data version of this AuthHandler object ({cls.SAVE_VERSION})."
            )

        return cls._from_save_data(save_data)

    @classmethod
    def _from_save_data(cls, save_data: dict) -> "FunctionalAuthHandler":
        raise NotImplementedError()

    def get_auth_token(self, code: Optional[str] = None) -> None:
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
        raise NotImplementedError()

    def refresh_access_token(self, refresh_token: Optional[str] = None) -> Union[None, Awaitable]:
        """
        This function is usually executed by HTTPHandler, but if you have a
        refresh token saved from the last session, then you can fill in the
        `refresh_token` argument which this function will use to get a valid token.

        **Parameters**

        refresh_token: Optional[str]
            A refresh token used to get a new access token.
        """
        raise NotImplementedError()


class AuthHandler(FunctionalAuthHandler):
    __slots__ = ("http", "_lock")

    def __init__(
        self,
        client_id: int,
        client_secret: str,
        redirect_url: Optional[str],
        scope: Optional[Scope] = None,
    ):
        super().__init__(client_id, client_secret, redirect_url, scope)

        self.http: HTTPHandler = HTTPHandler(self)
        self._lock: threading.Lock = threading.Lock()

    @staticmethod
    def _raise_for_status(resp):
        try:
            resp.raise_for_status()
        except Exception as exc:
            try:
                msg = resp.json()["error"]
            except:
                msg = None
            raise type(exc)(str(exc) + ": " + msg) if msg is not None else exc from None

    def get_auth_token(self, code: Optional[str] = None) -> None:
        data = self._get_data("client_credentials" if code is None else "authorization_code", code)

        response = self.http.get_auth_token(data)
        self._raise_for_status(response)
        response = response.json()

        self._handle_response(response)

    def refresh_access_token(self, refresh_token: Optional[str] = None) -> None:
        if refresh_token:
            self.refresh_token = refresh_token

        data = self._get_data("client_credentials" if self.refresh_token is None else "refresh_token")

        response = self.http.get_auth_token(data)
        self._raise_for_status(response)
        response = response.json()

        self._handle_response(response)

        if self._refresh_callback:
            self._refresh_callback(self)

    def get_token(self) -> Optional[str]:
        with self._lock:
            if self.expire_time - 5 <= monotonic():
                self.refresh_access_token()
            return self._token

    @classmethod
    def _from_save_data(cls, save_data: dict) -> "AuthHandler":
        client_id = save_data["client_id"]
        client_secret = save_data["client_secret"]
        redirect_url = save_data["redirect_url"]
        scope = Scope(*save_data["scope"].split())
        auth = cls(client_id, client_secret, redirect_url, scope)
        auth.http.set_domain(save_data["domain"])
        auth.refresh_access_token(save_data["refresh_token"])
        return auth

    @classmethod
    def from_save_data(cls, save_data: dict) -> "AuthHandler":
        return super().from_save_data(save_data)  # type: ignore

    def as_async(self) -> "AsynchronousAuthHandler":
        """
        Return an asynchronous version of this auth handler
        """
        from .asyncio.auth import AsynchronousAuthHandler

        auth = AsynchronousAuthHandler(self.client_id, self.client_secret, self.redirect_url, self.scope)
        auth.refresh_token = self.refresh_token
        auth._token = self._token
        auth.expire_time = self.expire_time
        auth._refresh_callback = self._refresh_callback
        auth.http.set_domain(self.http.domain)
        return auth
