import datetime
import asyncio
import functools

from retaggr.engines.base import Engine, ImageResult
from retaggr.engines.saucenao.handlers import DanbooruHandler, E621Handler, KonachanHandler, YandereHandler
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


    tag_indexes = set([9, 12, 26, 29])
    """Tag indexes we can parse.

    Valid index numbers can be found at https://saucenao.com/status.html .

    List of indexes we can parse for tags:

    * 9: Danbooru
    * 12: Yande.re
    * 26: Konachan
    * 29: E621
    """

    source_indexes = [5, 16, 29, 37, 34]
    """List of source indexes in preferred order (key 0 is preferred, last key is least preferred).
    
    Valid index numbers can be found at https://saucenao.com/status.html .

    List of indexes we use for sources:

    * 5: Pixiv (preferred, low quantity/risk of reuploads)
    * 16: FAKKU (official redistribution)
    * 37: MangaDex (not official redistribution, but metadata is accurate)
    * 34: DeviantART (not preferred, large number of art theft and reuploads)
    """

    indirect_source_indexes = [29]
    """List of indirect source indexes.

    There is no preferred order.

    Some of these may require extra steps to obtain the source.

    * 29: E621
    """
    def __init__(self, api_key, test_mode=False):
        self.api_key = api_key
        self.handlers = {
            DanbooruHandler.engine_id : DanbooruHandler(),
            KonachanHandler.engine_id : KonachanHandler(),
            YandereHandler.engine_id : YandereHandler(),
        }

    def enable_e621(self, username, app_name, version):
        """Activate the E621 parser."""
        self.handlers[E621Handler.engine_id] = E621Handler(username, app_name, version)

    async def search_image(self, url):
        request_url = "https://saucenao.com/search.php"
        params = {
            "db": "999", # No clever bitmasking -> need help with how to do that.
            "api_key": self.api_key,
            "output_type": "2", # 2 is the JSON API,
            "url": url
        }
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, functools.partial(fuck_aiohttp.get, request_url, params=params))
        j = r.json()
        if r.status_code == 200:
            return await self.index_parser(j)
        elif r.status_code == 429: 
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

        # Kinda looks stupid, but whatever.
        loop = asyncio.get_event_loop()
        source = set()
        tags = set()
        for entry in valid_results:
            for url in entry["data"]["ext_urls"]:
                source.add(url)
            handler = self.handlers.get(entry["header"]["index_id"], None)
            if handler:
                if handler.tag_capable:
                    tags.update(await handler.get_tag_data(entry["data"]))
                if handler.source_capable:
                    source.update(await handler.get_source_data(entry["data"]))

        return ImageResult(tags, source, None)