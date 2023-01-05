import time
import asyncio
import aiohttp
from io import BytesIO

from ..exceptions import ScopeException
from ..constants import base_url, lazer_base_url


class AsynchronousHTTPHandler:
    def __init__(self, client, request_wait_time, limit_per_minute, use_lazer=False):
        self.client = client
        self.rate_limit = RateLimitHandler(request_wait_time, limit_per_minute)
        self.use_lazer = use_lazer

    def get_headers(self, requires_auth=True, is_files=False, **kwargs):
        headers = {
            'charset': 'utf-8',
            **{str(key): str(value) for key, value in kwargs.items() if value is not None}
        }
        if not is_files:
            headers["Content-Type"] = "application/json"
        if requires_auth:
            headers['Authorization'] = f"Bearer {self.client.auth.token}"
        return headers

    async def make_request(self, path, data=None, headers=None, is_download=False, files=None, **kwargs):
        if headers is None:
            headers = {}
        if data is None:
            data = {}

        if path.requires_auth and self.client.auth is None:
            raise ScopeException("You need to be authenticated to make this request.")

        if path.requires_auth and path.scope not in self.client.auth.scope:
            raise ScopeException(f"You don't have the {path.scope} scope, which is required to make this request.")

        if path.requires_user and not self.client.auth.has_user:
            raise ScopeException("This request requires a user. You need either a delegate scope or "
                                 "to register OAuth with Authorization Code Grant.")

        headers = self.get_headers(path.requires_auth, files is not None, **headers)
        params = {str(key): value for key, value in kwargs.items() if value is not None}
        if files is not None:
            data = dict(map(lambda item: (item[0], item[1][1]), files.items()))

        async with aiohttp.ClientSession() as session:
            if not self.rate_limit.can_request:
                await self.rate_limit.wait()

            self.rate_limit.request_used()
            async with session.request(path.method,
                                       (lazer_base_url if self.use_lazer else base_url) + path.path,
                                       headers=headers, data=data, params=params) as resp:
                try:
                    resp.raise_for_status()
                except Exception as e:
                    try:
                        err = (await resp.json())['error']
                    except:
                        err = None
                    raise type(e)(str(e) + ": " + err) if err is not None else e
                if resp.content == b"":
                    return
                return await resp.json() if not is_download else resp.content


class RateLimitHandler:
    def __init__(self, request_wait_limit, limit_per_minute):
        self.wait_limit = request_wait_limit
        self.limit = limit_per_minute
        self.requests = []
        self.waiting = False

    def request_used(self):
        self.requests.append(time.perf_counter())
        self.reset()

    async def wait(self):
        while self.waiting:
            await asyncio.sleep(0.1)
        self.waiting = True
        if self.can_request:  # Check again due to asynchronous running
            self.waiting = False
            return
        next_available_request = self.wait_limit-(time.perf_counter()-self.last_request)
        if len(self.requests) >= self.limit:
            next_available_request = max(next_available_request, self.requests[0]+60-time.perf_counter())
        await asyncio.sleep(next_available_request)
        self.waiting = False

    def reset(self):
        while len(self.requests) > 0:
            if self.requests[0] + 60 < time.perf_counter():
                self.requests.pop(0)
            else:
                break

    @property
    def can_request(self):
        self.reset()
        return time.perf_counter()-self.last_request >= self.wait_limit and len(self.requests) < self.limit

    @property
    def last_request(self):
        return self.requests[-1] if len(self.requests) > 0 else 0
