import requests
import time
import threading
import logging
from typing import Optional, List, TYPE_CHECKING

from .exceptions import ScopeException, RequestException
from .constants import (
    DEFAULT_BASE_URL,
    DEFAULT_AUTH_URL,
    DEFAULT_TOKEN_URL,
    DEFAULT_DOMAIN,
    auth_url,
    token_url,
    base_url,
)
from .path import Path

if TYPE_CHECKING:
    from .auth import BaseAuthHandler
    from .asyncio.http import AsynchronousHTTPHandler
    from .asyncio.auth import BaseAsynchronousAuthHandler


__all__ = ("BaseHTTPHandler", "HTTPHandler")


_log = logging.getLogger(__name__)


def _convert_param_value(value):
    if isinstance(value, bool):
        return "true" if value else "false"
    return value


class BaseHTTPHandler:
    """
    Abstract class for handling http requests.
    """

    __slots__ = ("auth", "api_version", "domain", "base_url", "auth_url", "token_url")

    DEFAULT_API_VERSION = "20260123"

    def __init__(self, auth: Optional["BaseAuthHandler"], api_version: Optional[str] = None):
        self.auth: Optional[BaseAuthHandler] = auth
        self.set_api_version(api_version)

        self.domain = DEFAULT_DOMAIN
        self.auth_url = DEFAULT_AUTH_URL
        self.token_url = DEFAULT_TOKEN_URL
        self.base_url = DEFAULT_BASE_URL

    def set_domain(self, domain: str) -> None:
        """Set the domain to use for requests."""
        self.domain = domain
        self.auth_url = auth_url(domain)
        self.token_url = token_url(domain)
        self.base_url = base_url(domain)

    def set_api_version(self, api_version: Optional[str]):
        """Sets x-api-version header. Should be in the format YYYYMMDD. Pass `None` to set back to default."""
        self.api_version: str = api_version or self.DEFAULT_API_VERSION

    def set_ratelimit(self, request_wait_time: float = 1.0, limit_per_minute: int = 60):
        raise NotImplementedError()

    def check_path_validity(self, path: Path):
        if path.requires_auth and self.auth is None:
            raise ScopeException("You need to be authenticated to make this request.")

        if path.requires_auth and path.scope not in self.auth.scope:
            raise ScopeException(f"You don't have the {path.scope} scope, which is required to make this request.")

        if path.requires_user and not self.auth.has_user():
            raise ScopeException(
                "This request requires a user. You need either a delegate scope or "
                "to register OAuth with Authorization Code Grant."
            )

    def make_request(self, path, *args, **kwargs):
        raise NotImplementedError()


class HTTPHandler(BaseHTTPHandler):
    """
    Handles making requests. Used by :class:`osu.Client`.
    """

    __slots__ = ("rate_limit",)

    def __init__(
        self,
        auth: Optional["BaseAuthHandler"],
        request_wait_time: float = 1.0,
        limit_per_minute: int = 60,
        api_version: Optional[str] = None,
    ):
        super().__init__(auth, api_version)

        self.rate_limit: RateLimitHandler = RateLimitHandler(request_wait_time, limit_per_minute)

    def set_ratelimit(self, request_wait_time: float = 1.0, limit_per_minute: int = 60):
        self.rate_limit.wait_time = request_wait_time
        self.rate_limit.limit = limit_per_minute

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

        self.check_path_validity(path)

        headers = self.get_headers(path, files is not None, **headers)
        params = {str(key): _convert_param_value(value) for key, value in kwargs.items() if value is not None}

        self.rate_limit.wait()
        response = getattr(requests, path.method)(
            endpoint + path.path, headers=headers, data=data, params=params, files=files
        )
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

        if len(response.content) == 0:
            return

        return response.json() if not is_download else response

    def make_request(self, path, *args, **kwargs):
        return self.make_request_to_endpoint(self.base_url, path, *args, **kwargs)

    def get_auth_token(self, data):
        self.rate_limit.wait()
        return requests.post(self.token_url, data=data)

    @classmethod
    def from_async(cls, http: "AsynchronousHTTPHandler", auth: Optional["BaseAuthHandler"] = None):
        new_http = cls(auth, http.rate_limit.wait_time, http.rate_limit.limit, http.api_version)
        new_http.rate_limit._requests_sent = http.rate_limit._requests_sent
        new_http.base_url = http.base_url
        new_http.auth_url = http.auth_url
        new_http.token_url = http.token_url
        return new_http

    def as_async(self, auth: Optional["BaseAsynchronousAuthHandler"]) -> "AsynchronousHTTPHandler":
        from .asyncio.http import AsynchronousHTTPHandler

        return AsynchronousHTTPHandler.from_sync(self, auth)


class RateLimitHandler:
    __slots__ = (
        "wait_time",
        "limit",
        "_lock",
        "_waiting_lock",
        "_requests_sent",
    )

    def __init__(self, request_wait_time: float, limit_per_minute: int):
        self.wait_time: float = request_wait_time
        self.limit: int = limit_per_minute
        # for accessing non-thread-safe variables
        # intended to be used for short durations
        self._lock: threading.Lock = threading.Lock()
        # to make sure only one request is waiting at a time
        # okay to acquire for long periods of time
        self._waiting_lock: threading.Lock = threading.Lock()
        self._requests_sent: List[float] = []

    def wait(self):
        self._lock.acquire()

        if self.wait_time > 0:
            self._wait_with_wait_time()
        else:
            self._wait_without_wait_time()

        self._get_requests_sent().append(time.monotonic())

        self._lock.release()

    def _wait_with_wait_time(self):
        # acquiring _waiting_lock could take a bit
        # so let's release this one
        self._lock.release()
        # once acquired, we can choose the appropriate way to wait
        # without worry about race conditions. waiting one at a time
        # is okay since wait time between requests is > 0
        self._waiting_lock.acquire()

        self._lock.acquire()
        if len(requests_sent := self._get_requests_sent()) > 0:
            wait_time = max(0.0, self.wait_time - (time.monotonic() - requests_sent[-1]))
            if wait_time > 0:
                self._lock.release()
                time.sleep(wait_time)
                self._lock.acquire()

        self._waiting_lock.release()

    def _wait_without_wait_time(self):
        # under rate limit still, good to send
        if len(self._get_requests_sent()) < self.limit:
            return

        # acquiring _waiting_lock could take a bit
        # so let's release this one
        self._lock.release()
        self._waiting_lock.acquire()
        self._lock.acquire()

        # check again, then wait till oldest request expires past 1 minute
        if len(requests_sent := self._get_requests_sent()) >= self.limit:
            wait_time = max(0.0, 60.0 - (time.monotonic() - requests_sent[0]))
            if wait_time > 0:
                self._lock.release()
                time.sleep(wait_time)
                self._lock.acquire()

        self._waiting_lock.release()

    def _get_requests_sent(self):
        """expects self._lock is acquired when calling this function"""
        # update list
        while len(self._requests_sent) > 0 and time.monotonic() - self._requests_sent[0] >= 60:
            self._requests_sent.pop(0)

        return self._requests_sent
