from asyncio import exceptions


class AsyncCacheException(Exception):

    def __init__(self, message):
        super().__init__(message)
        self.message = message


class AsyncCacheTimeoutException(exceptions.TimeoutError):

    def __init__(self, message=None):
        self.message = message
        if not message:
            self.message = 'Time to Request API more than cache ttl. You must increase the ttl parameter!'
        super().__init__(self.message)
