import time
import asyncio
from typing import Optional, List, AsyncGenerator, TYPE_CHECKING
from inspect import iscoroutinefunction

try:
    import aiohttp
except ImportError:
    aiohttp = None

from ..http import BaseHTTPHandler, HTTPHandler
from ..exceptions import RequestException

if TYPE_CHECKING:
    from .auth import BaseAsynchronousAuthHandler
    from ..auth import BaseAuthHandler


__all__ = ("AsynchronousHTTPHandler", "BaseAsynchronousHTTPHandler")


class BaseAsynchronousHTTPHandler(BaseHTTPHandler):
    auth: "BaseAsynchronousAuthHandler"

    def __init__(
        self,
        auth: Optional["BaseAsynchronousAuthHandler"],
        api_version: Optional[str] = None
    ):
        super().__init__(auth, api_version)

        if not iscoroutinefunction(self.auth.get_token):
            raise ValueError("auth must have an async get_token method")

        if aiohttp is None:
            raise RuntimeError(
                "Missing aiohttp package, which is required to use asynchronous features."
                'Install osu.py with the async feature: "pip install osu.py[async]"'
            )

    def get_req_gen(self, path, *args, **kwargs) -> AsyncGenerator:
        raise NotImplementedError()

    async def make_request(self, path, *args, **kwargs):
        raise NotImplementedError()


class AsynchronousHTTPHandler(BaseAsynchronousHTTPHandler):
    """
    Handles making asynchronous requests. Used by :class:`osu.AsynchronousClient`.
    """

    def __init__(
        self,
        auth: Optional["BaseAsynchronousAuthHandler"],
        request_wait_time: float = 1.0,
        limit_per_minute: int = 60,
        api_version: Optional[str] = None,
    ):
        super().__init__(auth, api_version)

        self.rate_limit: RateLimitHandler = RateLimitHandler(request_wait_time, limit_per_minute)

    def set_ratelimit(self, request_wait_time: float = 1.0, limit_per_minute: int = 60):
        self.rate_limit.wait_time = request_wait_time
        self.rate_limit.limit = limit_per_minute

    async def get_headers(self, path, is_files=False, **kwargs):
        headers = {
            "charset": "utf-8",
            "x-api-version": self.api_version,
            "Accept": path.accept,
        }

        if not is_files:  # otherwise let requests library handle it
            headers["Content-Type"] = path.content_type

        if path.requires_auth and "Authorization" not in headers:
            token = await self.auth.get_token()
            if token is None:
                raise ValueError("Cannot make request requiring authorization with a null token")
            headers["Authorization"] = f"Bearer {token}"

        for key, value in kwargs.items():
            if value is not None:
                headers[str(key)] = str(value)

        return headers

    async def make_request_to_endpoint(self, endpoint, path, data=None, headers=None, files=None, **kwargs):
        if headers is None:
            headers = {}
        json = data
        file_data = None

        self.check_path_validity(path)

        headers = await self.get_headers(path, files is not None, **headers)
        params = {str(key): value for key, value in kwargs.items() if value is not None}
        if files is not None:
            file_data = dict(map(lambda item: (item[0], item[1][1]), files.items()))

        async with self.rate_limit:
            async with aiohttp.ClientSession() as session:
                async with session.request(
                    path.method,
                    endpoint + path.path,
                    headers=headers,
                    data=file_data,
                    json=json,
                    params=params,
                ) as resp:
                    await self._raise_for_status(resp)

                    if resp.content_length == 0:
                        return
                    yield resp

    async def _raise_for_status(self, resp):
        try:
            resp.raise_for_status()
        except Exception as e:
            try:
                err = (await resp.json())["error"]
            except:
                err = None

            if err:
                raise RequestException(err) from e

            raise e

    def get_req_gen(self, path, *args, **kwargs):
        return self.make_request_to_endpoint(self.base_url, path, *args, **kwargs)

    async def make_request(self, path, *args, **kwargs):
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
        gen = self.get_req_gen(path, *args, **kwargs)
        async for resp in gen:
            try:
                return await resp.json()
            except aiohttp.client_exceptions.ContentTypeError:
                return

    async def make_auth_request(self, data):
        async with self.rate_limit:
            async with aiohttp.ClientSession() as session:
                async with session.request("POST", self.token_url, json=data) as resp:
                    await self._raise_for_status(resp)
                    return await resp.json()

    @classmethod
    def from_sync(cls, http: HTTPHandler, auth: Optional["BaseAsynchronousAuthHandler"] = None):
        new_http = cls(
            auth,
            http.rate_limit.wait_time,
            http.rate_limit.limit,
            http.api_version
        )
        new_http.rate_limit._requests_finished = http.rate_limit._requests_finished
        new_http.base_url = http.base_url
        new_http.auth_url = http.auth_url
        new_http.token_url = http.token_url
        return new_http

    def as_sync(self, auth: Optional["BaseAuthHandler"]) -> HTTPHandler:
        return HTTPHandler.from_async(self, auth)


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
        self._lock: asyncio.Lock = asyncio.Lock()
        # to make sure only one request is waiting at a time
        # okay to acquire for long periods of time
        self._waiting_lock: asyncio.Lock = asyncio.Lock()
        self._finish_evt: asyncio.Event = asyncio.Event()
        self._requests_in_progress = 0
        self._requests_finished: List[float] = []

    async def __aenter__(self):
        await self._lock.acquire()

        if self.wait_time > 0:
            await self._wait_with_wait_time()
        else:
            await self._wait_without_wait_time()

        self._requests_in_progress += 1

        self._lock.release()

    async def _wait_with_wait_time(self):
        # acquiring _waiting_lock could take a bit
        # so let's release this one
        self._lock.release()
        # once acquired, we can choose the appropriate way to wait
        # without worry about race conditions. waiting one at a time
        # is perfectly valid since wait time between requests is > 0
        await self._waiting_lock.acquire()

        await self._lock.acquire()
        # wait for current request to finish
        if self._requests_in_progress > 0:
            # clear before releasing to make sure a request doesn't
            # finish in between and cause a deadlock
            self._finish_evt.clear()
            self._lock.release()

            await self._finish_evt.wait()
            time.sleep(self.wait_time)
            await self._lock.acquire()
        # wait until enough time as passed since last request finished
        elif len(requests_finished := self._get_requests_finished()) > 0:
            wait_time = max(0.0, self.wait_time - (time.monotonic() - requests_finished[-1]))
            if wait_time > 0:
                self._lock.release()
                time.sleep(wait_time)

            await self._lock.acquire()

        self._waiting_lock.release()

    async def _wait_without_wait_time(self):
        # under rate limit still
        if self._requests_in_progress + len(self._get_requests_finished()) < self.limit:
            return

        # acquiring _waiting_lock could take a bit
        # so let's release this one
        self._lock.release()
        await self._waiting_lock.acquire()

        await self._lock.acquire()
        should_wait = len(self._get_requests_finished()) == 0
        # if a request finishes between declaring should_wait
        # and the if statement below, it will know because
        # _finish_evt will be set
        self._finish_evt.clear()
        self._lock.release()

        # can't wait based on request history
        # so we wait until a request finishes and sets self._finish_evt
        if should_wait:
            await self._finish_evt.wait()

        await self._lock.acquire()
        oldest_req = None if len(requests_finished := self._get_requests_finished()) == 0 else requests_finished[0]
        should_wait = len(requests_finished) + self._requests_in_progress >= self.limit
        self._lock.release()

        # wait until back under limit
        if should_wait and oldest_req is not None:
            wait_time = max(0.0, 60 - (time.monotonic() - oldest_req))
            if wait_time > 0:
                time.sleep(wait_time)

        self._waiting_lock.release()
        await self._lock.acquire()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        finished_at = time.monotonic()
        await self._lock.acquire()
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
