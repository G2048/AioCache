import asyncio
import unittest

from asynciocache import AsyncCache
from LogSettings import get_logger

logger = get_logger('consolemode')


@AsyncCache(ttl=10)
async def long_api():
    logger.debug('Load from async API')
    await asyncio.sleep(3)
    return [{'namespace': 'A1'}, {'namespace': 'A2'}, {'namespace': 'A3'}]


@AsyncCache(ttl=10)
async def long_api_2():
    logger.debug('Load from async API')
    await asyncio.sleep(3)
    return [{'namespace': 'A4'}, {'namespace': 'A5'}, {'namespace': 'A6'}]


class AiocacheTestCase(unittest.IsolatedAsyncioTestCase):

    async def test_aiocache(self):
        result = await long_api()
        logger.info(f'Result: {result}')
        result = await long_api()
        logger.info(f'Result: {result}')

        await asyncio.sleep(0.5)

        result = await long_api()
        logger.info(f'Result: {result}')
        result = await long_api()
        logger.info(f'Result: {result}')

    async def test_expire_aiocache(self):
        result = await long_api()
        print(f'Result: {result}')
        result = await long_api_2()
        print(f'Result: {result}')

        await asyncio.sleep(10.0)

        result = await long_api_2()
        print(f'Result: {result}')
        result = await long_api_2()
        print(f'Result: {result}')


if __name__ == '__main__':
    unittest.main()
