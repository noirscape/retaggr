import datetime
import asyncio
import functools

from retaggr.engines.base import Engine, ImageResult
from retaggr.engines.saucenao.handlers import DanbooruHandler, GelbooruHandler, E621Handler, KonachanHandler, YandereHandler
from retaggr.errors import NotAvailableSearchException, EngineCooldownException
import requests as fuck_aiohttp

class SauceNao(Engine):
    """Reverse searches the SauceNao API and then does additional matching.

    This booru does not require images to be downloaded before searching.

    This API is subject to rate limits.

    :param api_key: SauceNao API key. You can get this by registering an account on saucenao.com
    :type api_key: str
    :param test_mode: Enable test mode. Test mode is unique in that it does not need an API key, but it only works on one URL.
    """
    host = "https://saucenao.com"
    download_required = False

    def __init__(self, api_key, test_mode=False):
        self.api_key = api_key
        self.handlers = {
            DanbooruHandler.engine_id : DanbooruHandler(),
            GelbooruHandler.engine_id : GelbooruHandler(),
            KonachanHandler.engine_id : KonachanHandler(),
            YandereHandler.engine_id : YandereHandler(),
        }
        self.test_mode = test_mode

    def enable_e621(self, username, app_name, version):
        """Enable the E621 parser. This allows for looking up tag information on E621.
        
        :param username: An E621 username.
        :type username: str
        :param app_name: The name of the application.
        :type app_name: str
        :param version: The version of the appliation.
        :type version: str
        """
        self.handlers[E621Handler.engine_id] = E621Handler(username, app_name, version)

    async def search_image(self, url):
        request_url = "https://saucenao.com/search.php"
        params = {
            "db": "999", # No clever bitmasking -> need help with how to do that.
            "api_key": self.api_key,
            "output_type": "2", # 2 is the JSON API,
            "url": url
        }

        if self.test_mode:
            params = {
                "db": "999",
                "output_type": "2",
                "testmode": "1",
                "numres": "16",
                "url": "http://saucenao.com/images/static/banner.gif"
            }

        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, functools.partial(fuck_aiohttp.get, request_url, params=params))
        j = r.json()
        if r.status_code == 200:
            return await self.index_parser(j)
        elif r.status_code == 429: # pragma: no cover
            raise EngineCooldownException()

    async def search_tag(self, tag):
        raise NotAvailableSearchException("This engine cannot search tags.")

    async def index_parser(self, json):
        """Parse the output from a succesful saucenao search to retrieve data from specific indexes.
        
        :param json: JSON output from the API.
        :type json: dict
        :return: Dictionary containing data that matches the output for :meth:`SauceNao.search_image_source`
        :rtype: ImageResult
        """
        base_similarity = json["header"]["minimum_similarity"] # Grab the minimum similarity saucenao advises, going lower is generally gonna give false positives.

        # Below we cast the _entry_ similarity to a float since somehow it's stored as an str.
        # Damn API inaccuracy
        valid_results = [entry for entry in json["results"] if float(entry["header"]["similarity"]) > base_similarity]

        # Test mode similarity override
        if self.test_mode:
            valid_results = json["results"]

        # Kinda looks stupid, but whatever.
        loop = asyncio.get_event_loop()
        source = set()
        tags = set()
        for entry in valid_results:
            if "ext_urls" in entry["data"]: # Some of these responses dont have ext_url...
                for url in entry["data"]["ext_urls"]:
                    source.add(url)
            handler = self.handlers.get(entry["header"]["index_id"], None)
            if handler:
                if handler.tag_capable:
                    tags.update(await handler.get_tag_data(entry["data"]))
                if handler.source_capable:
                    source.update(await handler.get_source_data(entry["data"]))

        return ImageResult(tags, source, None)
