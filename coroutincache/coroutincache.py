import logging
from time import time

logger = logging.getLogger('asyncio')


class AsyncCache:
    _cache = {}
    _ttl = {}

    def __init__(self, ttl):
        self.ttl = ttl

    def __expire_ttl(self, created_time) -> bool:
        return time() - created_time > self.ttl

    def __refresh_cache(self):
        keys = tuple(type(self)._ttl.keys())
        for key in keys:
            created_time = type(self)._ttl[key]
            if self.__expire_ttl(created_time):
                type(self)._ttl.pop(key)
                type(self)._cache.pop(key)
                logger.debug(f'Remove cache: {key=}')

    async def _create_cache(self, func, *args, **kwargs):
        key = f'{func.__name__}{args}{kwargs}'
        type(self)._cache[key] = await func(*args, **kwargs)
        type(self)._ttl[key] = time()

    def __call__(self, func):
        async def wrapper(*args, **kwargs):
            key = f'{func.__name__}{args}{kwargs}'
            cached_data = type(self)._cache.get(key)
            if not cached_data:
                logger.info('Create cache...')
                await self._create_cache(func, *args, **kwargs)
            else:
                self.__refresh_cache()
                cached_data = type(self)._cache.get(key)
                if not cached_data:
                    await self._create_cache(func, *args, **kwargs)

            cached_data = type(self)._cache.get(key)
            logger.debug(f'The current cache: {type(self)._ttl=}')
            return cached_data

        return wrapper
