import asyncio
import unittest

from coroutincache import asyncache
from LogSettings import get_logger
from coroutincache.exceptions import AsyncCacheTimeoutException

logger = get_logger('consolemode')


class Later:
    _loop = asyncio.get_event_loop()

    def del_cache(self, key):
        logger.debug(f'Remove cache: {key=}')

    async def later(self):
        loop = asyncio.get_event_loop()
        logger.info(f'{loop=}')
        logger.info(f'{self._loop=}')
        loop.call_later(2, self.del_cache, 'long_api')
        await asyncio.sleep(3)


@asyncache(ttl=5)
async def long_api(sleep=3):
    logger.debug('Load from async API')
    await asyncio.sleep(sleep)
    return [{'namespace': 'A1'}, {'namespace': 'A2'}, {'namespace': 'A3'}]


@asyncache(ttl=5)
async def long_api_with_exception(sleep=3):
    await asyncio.sleep(sleep)
    items = []
    items[0]


@asyncache(ttl=5)
async def long_api_2():
    logger.debug('Load from async API')
    await asyncio.sleep(3)
    return [{'namespace': 'A4'}, {'namespace': 'A5'}, {'namespace': 'A6'}]


class AiocacheTestCase(unittest.IsolatedAsyncioTestCase):

    async def test_autorefresh(self):
        result = await long_api()
        print(f'Result: {result}')
        result = await long_api()
        print(f'Result: {result}')

        print('time sleep...')
        await asyncio.sleep(15)
        print('time wakeup!')

        result = await long_api()
        print(f'Result: {result}')
        result = await long_api()
        print(f'Result: {result}')

    async def test_autorefresh_two_corutines(self):
        result = await long_api()
        print(f'Result: {result}')
        result = await long_api_2()
        print(f'Result: {result}')
        result = await long_api_2()
        print(f'Result: {result}')

        print('time sleep...')
        await asyncio.sleep(15)
        print('time wakeup!')

        result = await long_api_2()
        print(f'Result: {result}')
        result = await long_api()
        print(f'Result: {result}')

    async def test_aiocache(self):
        result = await long_api()
        print(f'Result: {result}')
        result = await long_api()
        print(f'Result: {result}')

        await asyncio.sleep(0.5)

        result = await long_api()
        print(f'Result: {result}')
        result = await long_api()
        print(f'Result: {result}')

    async def test_expire_aiocache(self):
        result = await long_api()
        print(f'Result: {result}')
        await asyncio.sleep(10.0)
        result = await long_api()
        print(f'Result: {result}')

        await asyncio.sleep(10.0)

        result = await long_api_2()
        print(f'Result: {result}')
        result = await long_api_2()
        print(f'Result: {result}')


class AiocacheExceptionsTestCase(unittest.IsolatedAsyncioTestCase):

    @unittest.expectedFailure
    async def test_negative_ttl_lesser_than_api_work(self):
        await long_api(20)

    @unittest.expectedFailure
    async def test_negative_raise_exeption(self):
        await long_api_with_exception(1)

    async def test_ttl_lesser_than_api_work(self):
        try:
            await long_api(20)
        except AsyncCacheTimeoutException:
            self.assertTrue(True)

    async def test_raise_exception(self):
        try:
            await long_api_with_exception(1)
        except IndexError:
            self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
