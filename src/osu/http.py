import requests
from .constants import base_url
import time
import math
from threading import Condition
from .exceptions import ScopeError


class HTTPHandler:
    def __init__(self, auth, client):
        self.auth = auth
        self.client = client
        self.rate_limit = RateLimiter()

    def get_headers(self, **kwargs):
        headers = {
            'Authorization': f'Bearer {self.auth.token}',
            **{str(key): str(value) for key, value in kwargs.items() if value is not None}
        }
        return headers

    def __getattr__(self, method):
        if not self.rate_limit.can_request:
            wait = Condition()
            wait.wait_for(self.rate_limit.get_can_request)

        def func(path, data=None, headers=None, **kwargs):
            if headers is None:
                headers = {}
            if data is None:
                data = {}
            scope_required = path.scope
            if scope_required.scopes[0] not in self.client.auth.scope:
                raise ScopeError("You don't have the right scope to be able to do this.")
            headers = self.get_headers(**headers)
            response = getattr(requests, method)(base_url + path.path, headers=headers, data=data, params=kwargs)
            response.raise_for_status()
            return response.json()
        return func


class RateLimiter:
    def __init__(self):
        self.offset = time.perf_counter() % 60
        self.minute_counter = 0
        self.rate_counter = 0

    def reset(self):
        if math.floor(self.time/60) != self.minute_counter:
            self.minute_counter = math.floor(self.time/60)
            self.rate_counter = 0

    def request_used(self):
        self.rate_counter += 1

    # Made a function to be used with threading.wait_for
    def get_can_request(self):
        return self.can_request

    @property
    def can_request(self):
        return self.rate_counter != 60

    @property
    def time(self):
        return time.perf_counter()-self.offset
