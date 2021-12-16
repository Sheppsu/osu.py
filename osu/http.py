import requests
import time
import math
from threading import Condition

from .exceptions import ScopeException
from .constants import base_url


class HTTPHandler:
    def __init__(self, auth, client, limit_per_second=1):
        self.auth = auth
        self.client = client
        self.rate_limit = RateLimiter(limit_per_second)

    def get_headers(self, **kwargs):
        headers = {
            'Authorization': f'Bearer {self.auth.token}',
            **{str(key): str(value) for key, value in kwargs.items() if value is not None}
        }
        return headers

    def __getattr__(self, method):
        if not self.rate_limit.can_request:
            self.rate_limit.wait()

        def func(path, data=None, headers=None, stream=False, **kwargs):
            if headers is None:
                headers = {}
            if data is None:
                data = {}
            scope_required = path.scope
            if scope_required.scopes not in self.client.auth.scope:
                raise ScopeException(f"You don't have the {scope_required} scope, which is required to do this action.")
            headers = self.get_headers(**headers)
            response = getattr(requests, method)(base_url + path.path, headers=headers, data=data, stream=stream, params=kwargs)
            self.rate_limit.request_used()
            response.raise_for_status()
            return response.json()

        return func


class RateLimiter:
    def __init__(self, limit_per_second=1):
        self.limit = limit_per_second
        self.last_request = time.perf_counter() - self.limit

    def request_used(self):
        self.last_request = time.perf_counter()

    def wait(self):
        time.sleep(1-(time.perf_counter()-self.last_request))

    @property
    def can_request(self):
        return time.perf_counter()-self.last_request >= self.limit
