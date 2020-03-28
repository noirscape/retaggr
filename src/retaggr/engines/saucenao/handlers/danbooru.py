import asyncio
import functools

import requests as fuck_aiohttp

from .base import SauceNaoHandler

class DanbooruHandler(SauceNaoHandler):
    engine_id = 9
    """"""

    tag_capable = True
    """"""

    source_capable = True
    """"""


    async def get_tag_data(self, data):
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, functools.partial(fuck_aiohttp.get, "https://danbooru.donmai.us/posts/" + str(data["danbooru_id"]) + ".json"))
        j = r.json()
        return set(j["tag_string"].split())

    async def get_source_data(self, data):
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, functools.partial(fuck_aiohttp.get, "https://danbooru.donmai.us/posts/" + str(data["danbooru_id"]) + ".json"))
        j = r.json()
        return set([j["source"]])