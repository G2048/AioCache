import asyncio
import logging
from functools import wraps
from time import time

logger = logging.getLogger('asyncio')


class AsyncCache:
    _cache = {}
    _ttl = {}

    def __init__(self, ttl: float, *, refresh: bool = False):
        self.ttl = ttl
        self.refresh = refresh

    def __del_cache(self, key):
        type(self)._ttl.pop(key)
        type(self)._cache.pop(key)
        logger.debug(f'Remove cache: {key=}')

    async def _create_cache(self, func, *args, **kwargs):
        key = f'{func.__name__}{args}{kwargs}'
        type(self)._cache[key] = await func(*args, **kwargs)
        type(self)._ttl[key] = time()

    def __call__(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            key = f'{func.__name__}{args}{kwargs}'
            loop = asyncio.get_event_loop()

            cached_data = type(self)._cache.get(key)
            time_later = loop.call_later(self.ttl, self.__del_cache, key)
            if not cached_data:
                logger.info('Create cache...')
                await self._create_cache(func, *args, **kwargs)
                cached_data = type(self)._cache.get(key)
            elif self.refresh:
                time_later.cancelled()

            logger.debug(f'The current cache: {type(self)._ttl=}')
            return cached_data

        return wrapper
