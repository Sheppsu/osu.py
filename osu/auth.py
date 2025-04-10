from time import monotonic
from typing import Callable, Optional, TYPE_CHECKING
import threading

from .scope import Scope
from .http import HTTPHandler, BaseHTTPHandler

if TYPE_CHECKING:
    from .asyncio.auth import AsynchronousAuthHandler


__all__ = ("BaseAuthHandler", "NoAuth", "FunctionalAuthHandler", "AuthUtil", "AuthHandler")


class BaseAuthHandler:
    """
    An abstract class for implementing authentication logic.
    """

    __slots__ = ("scope", "http")

    scope: Scope
    http: BaseHTTPHandler

    def get_token(self) -> Optional[str]:
        """
        Returns the access token. If the token is expired, it will be refreshed before being returned.
        """
        raise NotImplementedError()

    def has_user(self) -> bool:
        raise NotImplementedError()


class NoAuth(BaseAuthHandler):
    def __init__(self):
        self.scope = Scope()
        self.http = HTTPHandler(None)

    def get_token(self) -> Optional[str]:
        return

    def has_user(self) -> bool:
        return False


class AuthData:
    def __init__(self):
        self.refresh_token: Optional[str] = None
        self.token: Optional[str] = None
        self.expire_time: float = monotonic()

    def set_data(self, token: Optional[str], refresh_token: Optional[str], expires_in: float) -> None:
        self.token = token
        self.refresh_token = refresh_token
        self.expire_time = monotonic() + expires_in

    @property
    def has_expired(self):
        return self.expire_time - 5 <= monotonic()


class AuthUtil:
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

    client_id: int
    client_secret: str
    redirect_url: str
    scope: Scope
    http: BaseHTTPHandler
    _data: AuthData
    _refresh_callback: Optional[Callable[["AuthUtil"], None]]

    SAVE_VERSION = 2

    def __init__(
        self,
        client_id: int,
        client_secret: str,
        redirect_url: Optional[str],
        scope: Optional[Scope] = None,
    ):
        if scope is None:
            scope = Scope.default()

        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_url = redirect_url
        self.scope = scope

        self._data = AuthData()
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
                "refresh_token": {"refresh_token": self._data.refresh_token},
            }[grant_type]
        )

        return data

    def _handle_response(self, data):
        self._data.set_data(data["access_token"], data.get("refresh_token"), data["expires_in"])

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
            "scope": self.scope.scopes.replace(" ", "%20"),
            "state": state,
        }
        if not params["state"]:
            del params["state"]
        return self.http.auth_url + "?" + "&".join([f"{key}={value}" for key, value in params.items()])

    def has_user(self):
        """
        Returns whether this auth has access to endpoints requiring a user
        """
        return self.scope.has_user

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
            "refresh_token": self._data.refresh_token,
            "domain": self.http.domain,
        }

    @classmethod
    def from_save_data(cls, save_data: dict) -> "AuthUtil":
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
    def _from_save_data(cls, save_data: dict) -> "AuthUtil":
        client_id = save_data["client_id"]
        client_secret = save_data["client_secret"]
        redirect_url = save_data["redirect_url"]
        scope = Scope(*save_data["scope"].split())
        auth = cls(client_id, client_secret, redirect_url, scope)
        auth.http.set_domain(save_data["domain"])
        auth.refresh_token = save_data["refresh_token"]
        return auth

    def set_domain(self, domain: str):
        self.http.set_domain(domain)


# backwards compatibility
FunctionalAuthHandler = AuthUtil


class AuthHandler(BaseAuthHandler, AuthUtil):
    __slots__ = ("http", "_lock")

    def __init__(
        self,
        client_id: int,
        client_secret: str,
        redirect_url: Optional[str],
        scope: Optional[Scope] = None,
    ):
        AuthUtil.__init__(self, client_id, client_secret, redirect_url, scope)

        self.http: HTTPHandler = HTTPHandler(self)
        self._lock: threading.Lock = threading.Lock()

    def has_user(self) -> bool:
        return AuthUtil.has_user(self)

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

        response = self.http.get_auth_token(data)
        self._raise_for_status(response)
        response = response.json()

        self._handle_response(response)

    def refresh_access_token(self, refresh_token: Optional[str] = None) -> None:
        """
        This function is usually executed by HTTPHandler, but if you have a
        refresh token saved from the last session, then you can fill in the
        `refresh_token` argument which this function will use to get a valid token.

        **Parameters**

        refresh_token: Optional[str]
            A refresh token used to get a new access token.
        """
        if refresh_token:
            self._data.refresh_token = refresh_token

        data = self._get_data("client_credentials" if self._data.refresh_token is None else "refresh_token")

        response = self.http.get_auth_token(data)
        self._raise_for_status(response)
        response = response.json()

        self._handle_response(response)

        if self._refresh_callback:
            self._refresh_callback(self)

    def get_token(self) -> Optional[str]:
        with self._lock:
            if self._data.has_expired:
                self.refresh_access_token()
            return self._data.token

    @classmethod
    def from_async(cls, auth: "AsynchronousAuthHandler"):
        new_auth = cls(auth.client_id, auth.client_secret, auth.redirect_url, auth.scope)
        new_auth._data = auth._data
        new_auth._refresh_callback = auth._refresh_callback
        new_auth.http = auth.http.as_sync(new_auth)
        return new_auth

    def as_async(self) -> "AsynchronousAuthHandler":
        """
        Returns an asynchronous auth handler.
        Credentials are shared and updates in one apply to the other.
        This method primarily exists for running the library's tests.

        NOTE: Using both auth handlers in different threads at the same time is not safe.
        """
        from .asyncio.auth import AsynchronousAuthHandler

        return AsynchronousAuthHandler.from_sync(self)
