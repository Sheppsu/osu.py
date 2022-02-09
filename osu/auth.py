import requests
from time import time

from .constants import auth_url, token_url
from .objects import Scope
from .exceptions import ScopeException


class AuthHandler:
    """
    Helps to go through the oauth process easily, as well as refresh
    tokens without the user needing to worry about it.

    Note
    ----
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

    scope: :class:`Scope`
        Scope object helps the program identify what requests you can
        and can't make with your scope. Default is 'identify' (Scope.default())
    """
    def __init__(self, client_id: int, client_secret: str, redirect_url: str, scope: Scope = Scope.default()):
        if scope == 'lazer':
            raise ScopeException("The lazer scope signifies that an endpoint only meant for use by the lazer client.")
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_url = redirect_url
        self.scope = scope

        self.refresh_token = None
        self._token = None
        self.expire_time = time()

    def get_auth_url(self, state=''):
        """
        Returns a url that a user can authorize their account at. They'll then be returned to
        the redirect_uri with a code that can be used under get_auth_token.

        **Parameters**

        state: :class:`str`
            Will be returned to the redirect_uri along with the code.
        """
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_url,
            'response_type': 'code',
            'scope': self.scope.scopes,
            'state': state,
        }
        if not params['state']:
            del params['state']
        return auth_url + "?" + "&".join([f'{key}={value}' for key, value in params.items()])

    def get_auth_token(self, code=None):
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

        code: :class:`str`
            code from user authorizing at a specific url

        delegate: :class:`bool`
            Whether or not to use delegate scope. This scope is only available for Client Credential Grants.
        """
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }

        if code is None:
            data.update({
                'grant_type': 'client_credentials',
                'scope': 'public' if 'delegate' not in self.scope else self.scope.scopes,
            })
        else:
            data.update({
                'code': code,
                'grant_type': 'authorization_code',
                'redirect_uri': self.redirect_url,
            })

        response = requests.post(token_url, data=data)
        response.raise_for_status()
        response = response.json()
        if 'refresh_token' in response:
            self.refresh_token = response['refresh_token']
        self._token = response['access_token']
        self.expire_time = time() + response['expires_in'] - 5

    def refresh_access_token(self, refresh_token=None):
        """
        This function is usually executed by HTTPHandler, but if you have a
        refresh token saved from the last session, then you can fill in the
        `refresh_token` argument which this function will use to get a valid token.

        **Parameters**

        refresh_token: :class:`str`
            A refresh token saved from the last session
            (ex. You authorize with a user, save the refresh token,
            don't use the api long enough for the token to expire, but
            use the saved refresh token to get a valid access token
            without the user having to authorize again.)
        """
        if refresh_token:
            self.refresh_token = refresh_token
        if time() < self.expire_time:
            return
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }
        if self.refresh_token:
            data.update({
                'grant_type': 'refresh_token',
                'refresh_token': self.refresh_token,
            })
        else:
            data.update({
                'grant_type': 'client_credentials',
                'scope': 'public',
            })
        response = requests.post(token_url, data=data)
        response.raise_for_status()
        response = response.json()
        if 'refresh_token' in response:
            self.refresh_token = response['refresh_token']
        self._token = response['access_token']
        self.expire_time = time() + response['expires_in'] - 5

    @property
    def token(self):
        if self.expire_time <= time():
            self.refresh_access_token()
        return self._token
