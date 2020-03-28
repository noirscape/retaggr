import asyncio
import functools

import requests as fuck_aiohttp

from .base import SauceNaoHandler

class YandereHandler(SauceNaoHandler):
    engine_id = 12
    """"""

    tag_capable = True
    """"""

    source_capable = False
    """"""

    async def get_tag_data(self, data):
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, functools.partial(fuck_aiohttp.get, "https://yande.re/post.json", params={"tags": "id:" + str(data["yandere_id"])}))
        j = r.json()
        return set(j[0]["tags"].split())