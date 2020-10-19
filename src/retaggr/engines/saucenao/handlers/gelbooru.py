import asyncio
import functools

import requests as fuck_aiohttp

from .base import SauceNaoHandler

class GelbooruHandler(SauceNaoHandler):
    engine_id = 25
    """"""

    tag_capable = True
    """"""

    source_capable = True
    """"""


    async def get_tag_data(self, data):
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, functools.partial(fuck_aiohttp.get, "https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&id=" + str(data["gelbooru_id"])))
        j = r.json()[0]
        return set(j["tags"].split())

    async def get_source_data(self, data):
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, functools.partial(fuck_aiohttp.get, "https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&id=" + str(data["gelbooru_id"])))
        j = r.json()[0]
        return set([j["source"]])
