from retaggr.engines.base import Engine, ImageResult

# External modules
import asyncio
import requests as fuck_aiohttp
from aiohttp_requests import requests
import functools
import time
from lxml import html
import datetime

class E621(Engine):
    """Reverse searches https://e621.net through using the IQDB implementation over at https://iqdb.harry.lu in combination
    with the official e621 API.
    
    This booru does not required images to be downloaded before searching.

    :param username: Your e621 username
    :type username: str
    :param app_name: The name of your application.
    :type app_name: str
    :param version: The version of your application.
    :type version: float
    :param min_score: Minimum search match percentage needed.
    :type min_score: float
    """

    host = "https://iqdb.harry.lu/"
    e621_api = "https://e621.net/post/show.json"
    download_required = False

    last_request = None
    """The last request date the engine made to E621. Used to regulate the ratelimits."""


    def __init__(self, username, app_name, version, min_score):
        self.user_agent = {"User-Agent": f"{app_name}/{version} (by {username} on e621)"}
        self.min_score = min_score
        self.last_request = datetime.datetime.now()

    async def search_image(self, url):
        results = {
            "tags": [],
            "source": None
        }

        params = {"url" : url}

        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, functools.partial(fuck_aiohttp.post, self.host, params=params))

        doc = html.fromstring(r.text)
        tables = doc.xpath("//div[@id='pages']/div/table/tr/td")
    
        row = 5
        while row < len(tables):
            try:
                percent = float(str.split(tables[row].text)[0][:-1])
                # Get tags from page
                if percent > self.min_score:
                    post_id = tables[row - 3].xpath("//td/a")[0].get("href").split("/")[-1]
                    # Check tags from api
                    await self.sleep_until_ratelimit(1)
                    r = await requests.get(self.e621_api, headers=self.user_agent, params={"id": post_id})
                    self.last_request = datetime.datetime.now()
                    json = await r.json()
                    tags = json['tags'].split()
                    source = json['source']
                    rating = json['rating']
            except: # pragma: no cover
                pass
            row = row + 5
        return ImageResult(tags, source, rating)