import requests
import time
import threading
import logging
from datetime import datetime, timezone
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


class BaseHTTPHandler:
    __slots__ = ("auth", "api_version", "domain", "base_url", "auth_url", "token_url")

    def __init__(self, auth: Optional["BaseAuthHandler"], api_version: Optional[str] = None):
        self.auth: Optional[BaseAuthHandler] = auth
        self.set_api_version(api_version)

        self.domain = DEFAULT_DOMAIN
        self.auth_url = DEFAULT_AUTH_URL
        self.token_url = DEFAULT_TOKEN_URL
        self.base_url = DEFAULT_BASE_URL

    def set_domain(self, domain: str) -> None:
        self.domain = domain
        self.auth_url = auth_url(domain)
        self.token_url = token_url(domain)
        self.base_url = base_url(domain)

    def set_api_version(self, api_version: Optional[str]):
        self.api_version: str = api_version or datetime.now(tz=timezone.utc).strftime("%Y%m%d")

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
        params = {str(key): value for key, value in kwargs.items() if value is not None}

        with self.rate_limit:
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
        with self.rate_limit:
            return requests.post(self.token_url, data=data)

    @classmethod
    def from_async(cls, http: "AsynchronousHTTPHandler", auth: Optional["BaseAuthHandler"] = None):
        new_http = cls(auth, http.rate_limit.wait_time, http.rate_limit.limit, http.api_version)
        new_http.rate_limit._requests_finished = http.rate_limit._requests_finished
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
        "_finish_evt",
        "_requests_in_progress",
        "_requests_finished",
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
        self._finish_evt: threading.Event = threading.Event()
        self._requests_in_progress = 0
        self._requests_finished: List[float] = []

    def __enter__(self):
        self._lock.acquire()

        if self.wait_time > 0:
            self._wait_with_wait_time()
        else:
            self._wait_without_wait_time()

        self._requests_in_progress += 1

        self._lock.release()

    def _wait_with_wait_time(self):
        # acquiring _waiting_lock could take a bit
        # so let's release this one
        self._lock.release()
        # once acquired, we can choose the appropriate way to wait
        # without worry about race conditions. waiting one at a time
        # is perfectly valid since wait time between requests is > 0
        self._waiting_lock.acquire()

        self._lock.acquire()
        # wait for current request to finish
        if self._requests_in_progress > 0:
            # clear before releasing to make sure a request doesn't
            # finish in between and cause a deadlock
            self._finish_evt.clear()
            self._lock.release()

            self._finish_evt.wait()
            time.sleep(self.wait_time)
            self._lock.acquire()
        # wait until enough time as passed since last request finished
        elif len(requests_finished := self._get_requests_finished()) > 0:
            wait_time = max(0.0, self.wait_time - (time.monotonic() - requests_finished[-1]))
            if wait_time > 0:
                self._lock.release()
                time.sleep(wait_time)
                self._lock.acquire()

        self._waiting_lock.release()

    def _wait_without_wait_time(self):
        # under rate limit still
        if self._requests_in_progress + len(self._get_requests_finished()) < self.limit:
            return

        # acquiring _waiting_lock could take a bit
        # so let's release this one
        self._lock.release()
        self._waiting_lock.acquire()

        self._lock.acquire()
        should_wait = len(self._get_requests_finished()) == 0
        # if a request finishes between declaring should_wait
        # and the if statement below, it will know because
        # _finish_evt will be set
        self._finish_evt.clear()
        self._lock.release()

        # can't wait based on request history
        # so we wait until a request finishes and sets self._finish_evt
        if should_wait:
            self._finish_evt.wait()

        self._lock.acquire()
        oldest_req = None if len(requests_finished := self._get_requests_finished()) == 0 else requests_finished[0]
        should_wait = len(requests_finished) + self._requests_in_progress >= self.limit
        self._lock.release()

        # wait until back under limit
        if should_wait and oldest_req is not None:
            wait_time = max(0.0, 60 - (time.monotonic() - oldest_req))
            if wait_time > 0:
                time.sleep(wait_time)

        self._waiting_lock.release()
        self._lock.acquire()

    def __exit__(self, exc_type, exc_val, exc_tb):
        finished_at = time.monotonic()
        self._lock.acquire()
        self._requests_in_progress -= 1
        self._get_requests_finished().append(finished_at)
        # alert any waiting requests that one has just finished
        self._finish_evt.set()
        self._lock.release()

    def _get_requests_finished(self):
        """expects self._lock is acquired when calling this function"""
        # update list
        while len(self._requests_finished) > 0 and time.monotonic() - self._requests_finished[0] >= 60:
            self._requests_finished.pop(0)

        return self._requests_finished
