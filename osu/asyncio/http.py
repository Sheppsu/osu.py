import time
import asyncio
from typing import Optional, List, AsyncGenerator, TYPE_CHECKING
from inspect import iscoroutinefunction

try:
    import aiohttp
except ImportError:
    aiohttp = None

from ..http import BaseHTTPHandler, HTTPHandler, _convert_param_value
from ..exceptions import RequestException

if TYPE_CHECKING:
    from .auth import BaseAsynchronousAuthHandler
    from ..auth import BaseAuthHandler


__all__ = ("AsynchronousHTTPHandler", "BaseAsynchronousHTTPHandler")


class BaseAsynchronousHTTPHandler(BaseHTTPHandler):
    auth: "BaseAsynchronousAuthHandler"

    def __init__(self, auth: Optional["BaseAsynchronousAuthHandler"], api_version: Optional[str] = None):
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
        params = {str(key): _convert_param_value(value) for key, value in kwargs.items() if value is not None}
        if files is not None:
            file_data = dict(map(lambda item: (item[0], item[1][1]), files.items()))

        await self.rate_limit.wait()
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
        await self.rate_limit.wait()
        async with aiohttp.ClientSession() as session:
            async with session.request("POST", self.token_url, json=data) as resp:
                await self._raise_for_status(resp)
                return await resp.json()

    @classmethod
    def from_sync(cls, http: HTTPHandler, auth: Optional["BaseAsynchronousAuthHandler"] = None):
        new_http = cls(auth, http.rate_limit.wait_time, http.rate_limit.limit, http.api_version)
        new_http.rate_limit._requests_sent = http.rate_limit._requests_sent
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
        "_requests_sent",
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
        self._requests_sent: List[float] = []

    async def wait(self):
        await self._lock.acquire()

        if self.wait_time > 0:
            await self._wait_with_wait_time()
        else:
            await self._wait_without_wait_time()

        self._get_requests_sent().append(time.monotonic())

        self._lock.release()

    async def _wait_with_wait_time(self):
        # acquiring _waiting_lock could take a bit
        # so let's release this one
        self._lock.release()
        # once acquired, we can choose the appropriate way to wait
        # without worry about race conditions. waiting one at a time
        # is okay since wait time between requests is > 0
        await self._waiting_lock.acquire()

        await self._lock.acquire()
        if len(requests_sent := self._get_requests_sent()) > 0:
            wait_time = max(0.0, self.wait_time - (time.monotonic() - requests_sent[-1]))
            if wait_time > 0:
                self._lock.release()
                await asyncio.sleep(wait_time)
                await self._lock.acquire()

        self._waiting_lock.release()

    async def _wait_without_wait_time(self):
        # under rate limit still, good to send
        if len(self._get_requests_sent()) < self.limit:
            return

        # acquiring _waiting_lock could take a bit
        # so let's release this one
        self._lock.release()
        await self._waiting_lock.acquire()
        await self._lock.acquire()

        # check again, then wait till oldest request expires past 1 minute
        if len(requests_sent := self._get_requests_sent()) >= self.limit:
            wait_time = max(0.0, 60.0 - (time.monotonic() - requests_sent[0]))
            if wait_time > 0:
                self._lock.release()
                await asyncio.sleep(wait_time)
                await self._lock.acquire()

        self._waiting_lock.release()

    def _get_requests_sent(self):
        """expects self._lock is acquired when calling this function"""
        # update list
        while len(self._requests_sent) > 0 and time.monotonic() - self._requests_sent[0] >= 60:
            self._requests_sent.pop(0)

        return self._requests_sent
