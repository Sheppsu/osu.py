import requests
import time
from typing import Optional

from .auth import BaseAuthHandler
from .exceptions import ScopeException
from .constants import base_url


__all__ = ("HTTPHandler",)


class HTTPHandler:
    def __init__(
        self,
        auth: Optional[BaseAuthHandler],
        request_wait_time: float,
        limit_per_minute: int,
        api_version: str = "20220705",
    ):
        self.auth: Optional[BaseAuthHandler] = auth
        self.rate_limit: RateLimitHandler = RateLimitHandler(request_wait_time, limit_per_minute)
        self.api_version: str = api_version

    def get_headers(self, path, is_files=False, **kwargs):
        headers = {
            "charset": "utf-8",
            "x-api-version": self.api_version,
            "Accept": path.accept,
        }
        if not is_files:  # otherwise let requests library handle it
            headers["Content-Type"] = path.content_type
        if path.requires_auth and "Authorization" not in headers:
            token = self.auth.get_token()
            if token is None:
                raise ValueError("Cannot make request requiring authorization with a null token")
            headers["Authorization"] = f"Bearer {token}"
        for key, value in kwargs.items():
            if value is not None:
                headers[str(key)] = str(value)
        return headers

    def make_request_to_endpoint(
        self, endpoint, path, data=None, headers=None, is_download=False, files=None, **kwargs
    ):
        if headers is None:
            headers = {}
        if data is None:
            data = {}

        if path.requires_auth and self.auth is None:
            raise ScopeException("You need to be authenticated to make this request.")

        if path.requires_auth and path.scope not in self.auth.scope:
            raise ScopeException(f"You don't have the {path.scope} scope, which is required to make this request.")

        if path.requires_user and not self.auth.has_user():
            raise ScopeException(
                "This request requires a user. You need either a delegate scope or "
                "to register OAuth with Authorization Code Grant."
            )

        if not self.rate_limit.can_request:
            self.rate_limit.wait()

        headers = self.get_headers(path, files is not None, **headers)
        params = {str(key): value for key, value in kwargs.items() if value is not None}
        response = getattr(requests, path.method)(
            endpoint + path.path, headers=headers, data=data, params=params, files=files
        )
        self.rate_limit.request_used()
        try:
            response.raise_for_status()
        except Exception as e:
            try:
                err = response.json()["error"]
            except:
                err = None
            raise type(e)(str(e) + ": " + err) if err is not None else e from None
        if response.content == b"":
            return
        return response.json() if not is_download else response

    def make_request(self, path, *args, **kwargs):
        return self.make_request_to_endpoint(base_url, path, *args, **kwargs)


class RateLimitHandler:
    def __init__(self, request_wait_limit: float, limit_per_minute: int):
        self.wait_limit: float = request_wait_limit
        self.limit: int = limit_per_minute
        self.last_request: float = time.monotonic() - self.wait_limit
        self.requests: list[float] = []

    def request_used(self):
        self.requests.append(time.monotonic())
        self.last_request = time.monotonic()

    def wait(self):
        next_available_request = self.wait_limit - (time.monotonic() - self.last_request)
        if len(self.requests) >= self.limit:
            next_available_request = max(next_available_request, self.requests[0] + 60 - time.monotonic())
        if next_available_request <= 0:
            return
        time.sleep(next_available_request)

    def reset(self):
        while len(self.requests) > 0:
            if self.requests[0] + 60 < time.monotonic():
                self.requests.pop(0)
            else:
                break

    @property
    def can_request(self):
        self.reset()
        return time.monotonic() - self.last_request >= self.wait_limit and len(self.requests) < self.limit
