## Description

This is simple cache for corutines with a ttl parameter.

It have been make for corutines what getting a large data volume for over external api request.

## Installation
```python
pip install asyniocache
```

## Simple usage:

```python
import asyncio

from fastapi import FastAPI

from LogSettings import get_logger
from asyncache import AsyncCache

logger = get_logger('consolemode')
app = FastAPI()


@AsyncCache(ttl=20)
async def load_from_api(params=None):
    await asyncio.sleep(3)
    logger.debug(f'LOAD FROM API')
    return [{'namespace': 'A1'}, {'namespace': 'A2'}, {'namespace': 'A3'}]


@app.get("/")
async def root():
    result = await load_from_api(32)
    logger.info(f'Result: {result}')
    return result

```

## License
This project is licensed under the MIT License - see the [MIT LICENSE](https://opensource.org/license/mit) file for details.