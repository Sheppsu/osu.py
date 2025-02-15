import requests
import time
from datetime import datetime, timezone
from typing import Optional, List

from .auth import BaseAuthHandler
from .exceptions import ScopeException, RequestException
from .constants import DEFAULT_BASE_URL, base_url


__all__ = ("HTTPHandler",)


class HTTPHandler:
    """
    Handles making requests. Used by :class:`osu.Client`.
    """

    __slots__ = ("auth", "rate_limit", "api_version", "base_url")

    def __init__(
        self,
        auth: Optional[BaseAuthHandler],
        request_wait_time: float,
        limit_per_minute: int,
        api_version: Optional[str] = None,
    ):
        self.auth: Optional[BaseAuthHandler] = auth
        self.rate_limit: RateLimitHandler = RateLimitHandler(request_wait_time, limit_per_minute)
        self.api_version: str = api_version or datetime.now(tz=timezone.utc).strftime("%Y%m%d")
        self.base_url = DEFAULT_BASE_URL

    def set_domain(self, domain: str) -> None:
        self.base_url = base_url(domain)
        if self.auth is not None:
            self.auth.set_domain(domain)

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

            if err:
                raise RequestException(err) from e

            raise e

        if response.content == b"":
            return

        return response.json() if not is_download else response

    def make_request(self, path, *args, **kwargs):
        """
        Make request to the api.

        :param path:
        :type path: :class:`osu.Path`

        :param data: (Default None)
            Json body of the request
        :type data: Optional[Union[dict, list]]

        :param headers: (Default None)
            Headers to send in the request
        :type headers: Optional[Dict[str, str]]

        :param is_download: (Default False)
            Returns response object if true
        :type is_download: bool

        :param files: (Default None)

        :param kwargs:
            All kwargs will be interpreted as query parameters for the request.
        :type kwargs: Dict[str, str]
        """
        return self.make_request_to_endpoint(self.base_url, path, *args, **kwargs)


class RateLimitHandler:
    __slots__ = ("wait_limit", "limit", "last_request", "requests")

    def __init__(self, request_wait_limit: float, limit_per_minute: int):
        self.wait_limit: float = request_wait_limit
        self.limit: int = limit_per_minute
        self.last_request: float = time.monotonic() - self.wait_limit
        self.requests: List[float] = []

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
