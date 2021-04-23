import requests
from .constants import auth_url, token_url
from .objects import Scope
from time import time


class AuthHandler:
    def __init__(self, client_id: int, client_secret, redirect_uri, scope: Scope = Scope.default()):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scope = scope

        self.refresh_token = None
        self.token = None
        self.expire_time = None

    def get_auth_url(self, state=''):
        params = {
            'client_id': self.client_id,
            'redirect_url': self.redirect_uri,
            'response_type': 'code',
            'scope': self.scope.scope,
            'state': state,
        }
        return auth_url + "?" + "&".join([f'{key}={value}' for key, value in params.items()])

    def get_auth_token(self, code=None):
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }

        if code is None:
            data.update({
                'grant_type': 'client_credentials',
                'scope': 'public',
            })
        else:
            data.update({
                'code': code,
                'grant_type': 'authorization_code',
                'redirect_uri': self.redirect_uri,
            })

        response = requests.post(token_url, data=data)
        response.raise_for_status()
        response = response.json()
        if 'refresh_token' in response:
            self.refresh_token = response['refresh_token']
        self.token = response['access_token']
        self.expire_time = time() + response['expires_in'] - 5

    def refresh_access_token(self):
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
        self.token = response['access_token']
        self.expire_time = time() + response['expires_in'] - 5
