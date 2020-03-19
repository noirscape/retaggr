import asyncio
import functools
import time

import requests as fuck_aiohttp

from .base import SauceNaoHandler
import retaggr.aiohttp_requests as requests

class E621Handler(SauceNaoHandler):
    engine_id = 29
    tag_capable = True
    source_capable = False

    last_request = None

    def __init__(self, username, app_name, version):
        self.e621_user_agent = {"User-Agent": f"{app_name}/{version} (by {username} on e621)"}

    async def rate_limit_wait(self):
        if self.last_request is not None:
            current_time = time.time()
            if current_time == self.last_request:
                asyncio.sleep(1)

    async def get_tag_data(self, data):
        await self.rate_limit_wait()
        r = await requests.get("https://e621.net/post/show.json", headers=self.user_agent, params={"tags": "id" + str(entry["data"]["e621_id"])})
        j = r.json()
        self.last_request = time.time()
        return set(j[0]["tags"].split())
