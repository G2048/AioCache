import asyncio
import logging
from asyncio import exceptions
from functools import wraps
from time import time

from coroutincache.exceptions import AsyncCacheException, AsyncCacheTimeoutException

logger = logging.getLogger('asyncio')


class AsyncCache:
    _ttl = {}
    _cache = {}
    _background_tasks = set()

    def __init__(self, ttl: float, *, refresh: bool = False, auto_refresh: bool = True):
        self.ttl = ttl
        self.refresh = refresh
        self.auto_refresh = auto_refresh

    def __del_cache(self, key):
        type(self)._ttl.pop(key)
        type(self)._cache.pop(key)
        logger.debug(f'Remove cache: {key=}')

    async def _create_cache(self, func, *args, **kwargs):
        logger.info('Create cache...')
        key = f'{func.__name__}{args}{kwargs}'
        try:
            res = await asyncio.wait_for(func(*args, **kwargs), self.ttl)
            logger.info(f'Result: {res}')
            type(self)._cache[key] = res
        except exceptions.TimeoutError:
            raise AsyncCacheTimeoutException()
        type(self)._ttl[key] = time()

    def _callback(self, func, *args, **kwargs):
        logger.info(f'Auto refresh cache... {func=}')

        loop = asyncio.get_event_loop()
        loop.call_later(self.ttl, self._callback, func, *args, **kwargs)

        task = asyncio.create_task(self._create_cache(func, *args, **kwargs))
        type(self)._background_tasks.add(task)
        task.add_done_callback(type(self)._background_tasks.discard)

    def __call__(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            key = f'{func.__name__}{args}{kwargs}'
            loop = asyncio.get_event_loop()
            cached_data = type(self)._cache.get(key)

            if self.auto_refresh and not cached_data:
                loop.call_later(self.ttl, self._callback, func, *args, **kwargs)
            if self.refresh:
                time_later = loop.call_later(self.ttl, self.__del_cache, key)

            if not cached_data:
                await self._create_cache(func, *args, **kwargs)
                cached_data = type(self)._cache.get(key)
            elif self.refresh and not self.auto_refresh:
                time_later.cancelled()

            logger.debug(f'The current cache: {type(self)._ttl=}')
            return cached_data

        return wrapper
