import requests
from time import monotonic
from typing import Callable, Optional

from .constants import auth_url, token_url, lazer_token_url
from .objects import Scope
from .exceptions import ScopeException
from .util import create_multipart_formdata


class AuthHandler:
    """
    Helps to go through the oauth process easily, as well as refresh
    tokens without the user needing to worry about it.

    Note:
    If you're not authorizing a user with a url for a code, this does not apply to you.
    AuthHandler does not save refresh tokens past the program finishing.
    AuthHandler will save the refresh token to refresh the access token
    while the program is running, so make sure to save the refresh token
    before shutting down the program so you can use it to get a valid access token
    without having the user reauthorize.

    **Init Parameters**

    client_id: :class:`int`
        Client id

    client_secret: :class:`str`
        Client secret

    redirect_uri: :class:`str`
        Redirect uri

    scope: Optional[:class:`Scope`]
        Scope object helps the program identify what requests you can
        and can't make with your scope. Default is 'public' (Scope.default())
    """

    SAVE_VERSION = 1

    def __init__(
        self,
        client_id: int,
        client_secret: str,
        redirect_url: str,
        scope: Optional[Scope] = Scope.default(),
    ):
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

    def get_auth_url(self, state: Optional[str] = ""):
        """
        Returns a url that a user can authorize their account at. They'll then be returned to
        the redirect_uri with a code that can be used under get_auth_token.

        **Parameters**

        state: Optional[:class:`str`]
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
        return auth_url + "?" + "&".join([f"{key}={value}" for key, value in params.items()])

    def get_auth_token(self, code: Optional[str] = None):
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

        code: Optional[:class:`str`]
            code from user authorizing at a specific url
        """
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }

        if code is None:
            data.update(
                {
                    "grant_type": "client_credentials",
                    "scope": "public" if "delegate" not in self.scope else self.scope.scopes,
                }
            )
        else:
            data.update(
                {
                    "code": code,
                    "grant_type": "authorization_code",
                    "redirect_uri": self.redirect_url,
                }
            )

        response = requests.post(token_url, data=data)
        response.raise_for_status()
        response = response.json()
        if "refresh_token" in response:
            self.refresh_token = response["refresh_token"]
        self._token = response["access_token"]
        self.expire_time = monotonic() + response["expires_in"]

    def refresh_access_token(self, refresh_token: Optional[str] = None):
        """
        This function is usually executed by HTTPHandler, but if you have a
        refresh token saved from the last session, then you can fill in the
        `refresh_token` argument which this function will use to get a valid token.

        **Parameters**

        refresh_token: Optional[:class:`str`]
            A refresh token used to get a new access token.
        """
        if refresh_token:
            self.refresh_token = refresh_token
        if monotonic() < self.expire_time:
            return
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        if self.refresh_token:
            data.update(
                {
                    "grant_type": "refresh_token",
                    "refresh_token": self.refresh_token,
                }
            )
        else:
            data.update(
                {
                    "grant_type": "client_credentials",
                    "scope": "public",
                }
            )
        response = requests.post(token_url, data=data)
        response.raise_for_status()
        response = response.json()
        if "refresh_token" in response:
            self.refresh_token = response["refresh_token"]
        self._token = response["access_token"]
        self.expire_time = monotonic() + response["expires_in"]
        if self._refresh_callback:
            self._refresh_callback(self)

    @property
    def token(self):
        """
        Returns the access token. If the token is expired, it will be refreshed before being returned.
        """
        if self.expire_time - 5 <= monotonic():
            self.refresh_access_token()
        return self._token

    @property
    def has_user(self):
        return "delegate" in self.scope or self.refresh_token is not None

    def set_refresh_callback(self, callback: Callable[["AuthHandler"], None]):
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

        'save_version': :class:`int`,

        'client_id': :class:`int`,

        'client_secret': :class:`str`,

        'redirect_url': :class:`str`,

        'scope': :class:`str`,

        'refresh_token': :class:`str`,

        }
        """
        return {
            "save_version": self.SAVE_VERSION,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_url": self.redirect_url,
            "scope": self.scope.scopes,
            "refresh_token": self.refresh_token,
        }

    @classmethod
    def from_save_data(cls, save_data: dict):
        """
        Create a new :class:`AuthHandler` object from save data.
        """
        save_version = save_data["save_version"]
        if save_version != cls.SAVE_VERSION:
            raise ValueError(
                f"The version of this save data ({save_version}) is not compatible "
                f"with the save data version of this AuthHandler object ({cls.SAVE_VERSION})."
            )

        client_id = save_data["client_id"]
        client_secret = save_data["client_secret"]
        redirect_url = save_data["redirect_url"]
        scope = Scope(*save_data["scope"].split())
        auth = cls(client_id, client_secret, redirect_url, scope)
        auth.refresh_access_token(save_data["refresh_token"])
        return auth


class LazerAuthHandler:
    # https://github.com/ppy/osu/blob/master/osu.Game/Online/ProductionEndpointConfiguration.cs
    LAZER_CLIENT_ID = 5
    LAZER_CLIENT_SECRET = "FGc9GAtyHzeQDshWP5Ah7dega8hJACAJpQtw6OXk"

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.scope = Scope("*")

        self._token = None
        self.refresh_token = None
        self.expire_time = 0

    def get_auth_token(self):
        data = {
            "username": self.username,
            "password": self.password,
            "grant_type": "password",
            "client_id": self.LAZER_CLIENT_ID,
            "client_secret": self.LAZER_CLIENT_SECRET,
            "scope": self.scope.scopes,
        }

        resp = requests.post(lazer_token_url, files=create_multipart_formdata(data))
        resp.raise_for_status()
        resp = resp.json()
        self._token = resp["access_token"]
        self.refresh_token = resp["refresh_token"]
        self.expire_time = monotonic() + resp["expires_in"]

    def refresh_access_token(self):
        if self.refresh_token is None:
            return ValueError("refresh_token must have a value to refresh the access token (obviously)")
        data = {
            "client_id": self.LAZER_CLIENT_ID,
            "client_secret": self.LAZER_CLIENT_SECRET,
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
        }

        resp = requests.post(lazer_token_url, data=data)
        resp.raise_for_status()
        resp = resp.json()
        self._token = resp["access_token"]
        self.refresh_token = resp["refresh_token"]
        self.expire_time = monotonic() + resp["expires_in"]

    @property
    def token(self):
        if self.expire_time - 5 <= monotonic():
            self.refresh_access_token()
        return self._token

    @property
    def has_user(self):
        return self._token is not None
