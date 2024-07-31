## Description

This is cache for coroutines with a ttl parameter and the `auto_refresh` functional.

### Explanation

- `auto_refresh` parameter is needs to call is cached coroutine again

It have been make for coroutines what getting a large data volume from third-party heavy APIs, information from which
may change periodically.

## Installation

```zsh
pip install coroutincache
```

## Usage

### Simple usage:

```python
import asyncio

from fastapi import FastAPI
from coroutincache import asyncache

from LogSettings import get_logger

logger = get_logger('consolemode')
app = FastAPI()


@asyncache(ttl=20)
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

### Like regular cache with ttl parameter

```python
import asyncio

from coroutincache import asyncache


@asyncache(ttl=20, auto_refresh=False)
async def load_from_api(params=None):
    await asyncio.sleep(3)
    return [{'namespace': 'A1'}, {'namespace': 'A2'}, {'namespace': 'A3'}]  # Large data

```

## License

This project is licensed under the MIT License - see the [MIT LICENSE](https://opensource.org/license/mit) file for
details.