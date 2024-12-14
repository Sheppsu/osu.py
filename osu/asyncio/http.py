import time
import asyncio
from typing import Optional, List
from inspect import isawaitable
from datetime import datetime, timezone

try:
    import aiohttp
    from aiohttp.client_exceptions import ContentTypeError

    has_aiohttp = True
except ImportError:
    has_aiohttp = False

from ..auth import BaseAuthHandler
from ..exceptions import ScopeException, RequestException
from ..constants import DEFAULT_BASE_URL, base_url
from ..util import raise_aiohttp_error


__all__ = ("AsynchronousHTTPHandler",)


class AsynchronousHTTPHandler:
    """
    Handles making asynchronous requests. Used by :class:`osu.AsynchronousClient`.
    """

    def __init__(
        self,
        auth: Optional[BaseAuthHandler],
        request_wait_time: float,
        limit_per_minute: int,
        api_version: Optional[str] = None,
    ):
        if not isawaitable(awaitable := auth.get_token()):
            raise ValueError("auth passed to AsynchronousHTTPHandler must have an asynchronous get_token method")

        if not has_aiohttp:
            raise_aiohttp_error()

        awaitable.close()  # type: ignore

        self.auth: Optional[BaseAuthHandler] = auth
        self.rate_limit: RateLimitHandler = RateLimitHandler(request_wait_time, limit_per_minute)
        self.api_version: str = api_version or datetime.now(tz=timezone.utc).strftime("%Y%m%d")
        self.base_url = DEFAULT_BASE_URL

    def set_domain(self, domain: str) -> None:
        self.base_url = base_url(domain)

    async def get_headers(self, path, is_files=False, **kwargs):
        headers = {
            "charset": "utf-8",
            "x-api-version": self.api_version,
            "Accept": path.accept,
        }
        if not is_files:  # otherwise let requests library handle it
            headers["Content-Type"] = path.content_type
        if path.requires_auth and "Authorization" not in headers:
            token = await self.auth.get_token()  # type: ignore
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

        if path.requires_auth and self.auth is None:
            raise ScopeException("You need to be authenticated to make this request.")

        if path.requires_auth and path.scope not in self.auth.scope:
            raise ScopeException(f"You don't have the {path.scope} scope, which is required to make this request.")

        if path.requires_user and not self.auth.has_user():
            raise ScopeException(
                "This request requires a user. You need either a delegate scope or "
                "to register OAuth with Authorization Code Grant."
            )

        headers = await self.get_headers(path, files is not None, **headers)
        params = {str(key): value for key, value in kwargs.items() if value is not None}
        if files is not None:
            file_data = dict(map(lambda item: (item[0], item[1][1]), files.items()))

        async with aiohttp.ClientSession() as session:
            if not self.rate_limit.can_request:
                await self.rate_limit.wait()

            self.rate_limit.request_used()
            async with session.request(
                path.method,
                endpoint + path.path,
                headers=headers,
                data=file_data,
                json=json,
                params=params,
            ) as resp:
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

                if resp.content_length == 0:
                    return
                yield resp

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
            except ContentTypeError:
                return


class RateLimitHandler:
    __slots__ = ("wait_limit", "limit", "requests", "_lock")

    def __init__(self, request_wait_limit: float, limit_per_minute: int):
        self.wait_limit: float = request_wait_limit
        self.limit: int = limit_per_minute
        self.requests: List[float] = []
        self._lock: asyncio.Lock = asyncio.Lock()

    def request_used(self):
        self.requests.append(time.monotonic())
        self.reset()

    async def wait(self):
        await self._lock.acquire()
        if self.can_request:
            self._lock.release()
            return
        next_available_request = self.wait_limit - (time.monotonic() - self.last_request)
        if len(self.requests) >= self.limit:
            next_available_request = max(next_available_request, self.requests[0] + 60 - time.monotonic())
        await asyncio.sleep(next_available_request)
        self._lock.release()

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

    @property
    def last_request(self):
        return self.requests[-1] if len(self.requests) > 0 else 0
