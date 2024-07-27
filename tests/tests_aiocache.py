import asyncio
import unittest

from coroutincache import asyncache
from LogSettings import get_logger

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


@asyncache(ttl=10)
async def long_api():
    logger.debug('Load from async API')
    await asyncio.sleep(3)
    return [{'namespace': 'A1'}, {'namespace': 'A2'}, {'namespace': 'A3'}]


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


if __name__ == '__main__':
    unittest.main()
