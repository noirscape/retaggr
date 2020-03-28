import asyncio
import functools
import time

import requests as fuck_aiohttp

from .base import SauceNaoHandler
from retaggr.aiohttp_requests import requests

class E621Handler(SauceNaoHandler):
    engine_id = 29
    """"""

    tag_capable = True
    """"""

    source_capable = True
    """"""


    last_request = None

    def __init__(self, username, app_name, version):
        self.user_agent = {"User-Agent": f"{app_name}/{version} (by {username} on e621)"}

    async def rate_limit_wait(self):
        if self.last_request is not None: # pragma: no cover
            current_time = time.time()
            if current_time == self.last_request:
                asyncio.sleep(1)

    async def get_tag_data(self, data):
        await self.rate_limit_wait()
        r = await requests.get("https://e621.net/posts.json", headers=self.user_agent, params={"tags": "id:" + str(data["e621_id"])})
        j = await r.json()
        self.last_request = time.time()

        tags = set()
        for category in j["posts"][0]["tags"]:
            for tag in j["posts"][0]["tags"][category]:
                tags.add(tag)

        return tags

    async def get_source_data(self, data):
        await self.rate_limit_wait()
        r = await requests.get("https://e621.net/posts.json", headers=self.user_agent, params={"tags": "id:" + str(data["e621_id"])})
        j = await r.json()
        self.last_request = time.time()

        sources = set()
        for source in j["posts"][0]["sources"]:
            sources.add(source)

        return sources
