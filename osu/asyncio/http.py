import time
import asyncio
import aiohttp

from ..exceptions import ScopeException
from ..constants import base_url, lazer_base_url


class AsynchronousHTTPHandler:
    def __init__(self, client, request_wait_time, limit_per_minute, use_lazer=False):
        self.client = client
        self.rate_limit = RateLimitHandler(request_wait_time, limit_per_minute)
        self.use_lazer = use_lazer

    def get_headers(self, path, is_files=False, **kwargs):
        headers = {
            "charset": "utf-8",
            "x-api-version": "20220705",
            "Accept": path.accept,
        }
        if not is_files:  # otherwise let requests library handle it
            headers["Content-Type"] = path.content_type
        if path.requires_auth and "Authorization" not in headers:
            headers["Authorization"] = f"Bearer {self.client.auth.token}"
        for key, value in kwargs.items():
            if value is not None:
                headers[str(key)] = str(value)
        return headers

    async def make_request_to_endpoint(self, endpoint, path, data=None, headers=None, files=None, **kwargs):
        if headers is None:
            headers = {}
        json = data
        file_data = None

        if path.requires_auth and self.client.auth is None:
            raise ScopeException("You need to be authenticated to make this request.")

        if path.requires_auth and path.scope not in self.client.auth.scope:
            raise ScopeException(f"You don't have the {path.scope} scope, which is required to make this request.")

        if path.requires_user and not self.client.auth.has_user:
            raise ScopeException(
                "This request requires a user. You need either a delegate scope or "
                "to register OAuth with Authorization Code Grant."
            )

        headers = self.get_headers(path, files is not None, **headers)
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
                    raise type(e)(str(e) + ": " + err) if err is not None else e from None
                if resp.content_length == 0:
                    return
                yield resp

    def get_req_gen(self, path, *args, **kwargs):
        return self.make_request_to_endpoint(lazer_base_url if self.use_lazer else base_url, path, *args, **kwargs)

    async def make_request(self, path, *args, **kwargs):
        gen = self.get_req_gen(path, *args, **kwargs)
        async for resp in gen:
            return await resp.json()


class RateLimitHandler:
    def __init__(self, request_wait_limit, limit_per_minute):
        self.wait_limit = request_wait_limit
        self.limit = limit_per_minute
        self.requests = []
        self._lock = asyncio.Lock()

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
