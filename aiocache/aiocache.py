import threading
from time import sleep, time

from LogSettings import get_logger

logger = get_logger('asyncio')


class AsyncCache:
    _cache = {}
    _ttl = {}
    _first_run = True

    def __init__(self, ttl):
        self.ttl = ttl
        if type(self)._first_run:
            logger.info('First run...')
            check_ttl_thread = threading.Thread(target=self.__loop_check_ttl, daemon=True)
            check_ttl_thread.start()
            type(self)._first_run = False

    def __expire_ttl(self, created_time) -> bool:
        return time() - created_time > self.ttl

    def __loop_check_ttl(self):
        while True:
            keys = tuple(type(self)._ttl.keys())
            for key in keys:
                created_time = type(self)._ttl[key]
                if self.__expire_ttl(created_time):
                    type(self)._ttl.pop(key)
                    type(self)._cache.pop(key)
                    logger.debug(f'Remove cache: {key=}')
            sleep(self.ttl / 2)

    async def _create_cache(self, func, *args, **kwargs):
        key = f'{func.__name__}{args}{kwargs}'
        type(self)._cache[key] = await func(*args, **kwargs)
        type(self)._ttl[key] = time()

    def __call__(self, func):
        async def wrapper(*args, **kwargs):
            key = f'{func.__name__}{args}{kwargs}'
            if key not in type(self)._cache:
                logger.info('Create cache...')
                await self._create_cache(func, *args, **kwargs)

            logger.debug(f'The current cache: {type(self)._ttl=}')
            return type(self)._cache[key]

        return wrapper
