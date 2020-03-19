from retaggr.engines.base import Engine, ImageResult

# External modules
import asyncio
import requests as fuck_aiohttp
import functools

class Danbooru(Engine):
    """Reverse searches https://danbooru.donmai.us for images.
    
    This booru does not required images to be downloaded before searching.

    :param username: The danbooru username you wish to use.
    :type username: str
    :param api_key: A danbooru API key. You can obtain one from your profile.
    :type api_key: str
    :param min_score: Minimum search match percentage needed.
    :type min_score: float
    """
    host = "https://danbooru.donmai.us"
    download_required = False

    def __init__(self, username, api_key, min_score):
        self.min_score = min_score
        self.username = username
        self.api_key = api_key

    async def search_image(self, url):
        tags = []
        source = []
        rating = None

        iqdb_url = self.host + "/iqdb_queries.json"
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, functools.partial(fuck_aiohttp.get, iqdb_url, params={"url":url}, auth=(self.username, self.api_key)))
        json = r.json()
        if 'success' in json:
            if not json['success']: # pragma: no cover
                return ImageResult(tags, source, rating)

        if len(json) > 0:
            if json[0]['score'] > self.min_score:
                tags = json[0]["post"]["tag_string"].split()
                source.append(json[0]["post"]["source"])
                rating = json[0]["post"]["rating"]
        return ImageResult(tags, source, rating)