import datetime
import asyncio
import functools

from retaggr.engines.base import Engine, ImageResult
from retaggr.errors import NotAvailableSearchException, EngineCooldownException
import requests as fuck_aiohttp

class SauceNao(Engine):
    """Reverse searches the SauceNao API and then does additional matching.

    This booru does not require images to be downloaded before searching.

    This API is subject to rate limits.

    :param api_key: SauceNao API key. You can get this by registering an account on saucenao.com
    :type api_key: str
    """
    host = "https://saucenao.com"
    download_required = False


    tag_indexes = set([9, 12, 26])
    """Tag indexes we can parse.

    Valid index numbers can be found at https://saucenao.com/status.html .

    List of indexes we can parse for tags:

    * 9: Danbooru
    * 12: Yande.re
    * 26: Konachan
    """

    source_indexes = [5, 16, 37, 34]
    """List of source indexes in preferred order (key 0 is preferred, last key is least preferred).
    
    Valid index numbers can be found at https://saucenao.com/status.html .

    List of indexes we use for sources:

    * 5: Pixiv (preferred, low quantity/risk of reuploads)
    * 16: FAKKU (official redistribution)
    * 37: MangaDex (not official redistribution, but metadata is accurate)
    * 34: DeviantART (not preferred, large number of art theft and reuploads)
    """

    long_remaining = 1
    """The total amount of requests remaining for the next 24 hours. If this is 0, the library will raise an :class:`retaggr.errors.EngineCooldownException` until the rate limit expires."""

    short_remaining = 1
    """The total amount of requests remaining for the next 30 seconds. If this is 0, the library will sleep until it expires."""

    last_request = None
    """The last request date the engine made to saucenao. Used to regulate the ratelimits."""

    def __init__(self, api_key):
        self.api_key = api_key
        self.last_request = datetime.datetime.now()

    async def search_image(self, url):
        request_url = "https://saucenao.com/search.php"
        params = {
            "db": "999", # No clever bitmasking -> need help with how to do that.
            "api_key": self.api_key,
            "output_type": "2", # 2 is the JSON API,
            "url": url
        }
        if self.last_request: # pragma: no cover
            long_ratelimit_ends = self.last_request + datetime.timedelta(hours=24)
            if self.long_remaining <= 1 and long_ratelimit_ends < datetime.datetime.now():
                raise EngineCooldownException(until=long_ratelimit_ends)

        if self.short_remaining <= 1: # pragma: no cover
            await self.sleep_until_ratelimit(35) # 35 seconds = no issue

        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, functools.partial(fuck_aiohttp.get, request_url, params=params))
        j = r.json()
        self.last_request = datetime.datetime.now()
        if r.status_code == 200:
            self.short_remaining = j["header"]["short_remaining"] - 1
            self.long_remaining = j["header"]["long_remaining"] - 1
            return await self.index_parser(j)
        elif r.status_code == 429: # 429 indicates we hit a rate limit, but not one we could've accounted for before.
            self.short_remaining = 0
            # We do raise an EngineCooldownException, since this indicates that it occured before API instantiating a request
            # (rest of library handles it with a previously done request already)
            raise EngineCooldownException(until=datetime.datetime.now() + datetime.timedelta(seconds=35)) 

    async def search_tag(self, tag):
        raise NotAvailableSearchException("This engine cannot search tags.")

    async def index_parser(self, json):
        """Parse the output from a succesful saucenao search to retrieve data from specific indexes.
        
        :param json: JSON output from the API.
        :type json: dict
        :return: Dictionary containing data that matches the output for :meth:`SauceNao.search_image_source`
        :rtype: dict
        """
        base_similarity = json["header"]["minimum_similarity"] # Grab the minimum similarity saucenao advises, going lower is generally gonna give false positives.

        # Below we cast the _entry_ similarity to a float since somehow it's stored as an str.
        # Damn API inaccuracy
        source_results = [entry for entry in json["results"] if entry["header"]["index_id"] in self.source_indexes and float(entry["header"]["similarity"]) > base_similarity]

        source = None
        source_priority = len(self.source_indexes) # No result priority is 1 above the least wanted result
        for entry in source_results:
            list_index = self.source_indexes.index(entry["header"]["index_id"])
            if list_index < source_priority: # If our exsting result priority is lower than the current result...
                source = entry["data"]["ext_urls"][0] # We update the source with that result
                source_priority = list_index # And we update the priority

        # See my comment above source_results as to what I'm doing here.
        tag_results_list = [entry for entry in json["results"] if entry["header"]["index_id"] in self.tag_indexes and float(entry["header"]["similarity"]) > base_similarity]

        # Unlike the source, these require specific lookups based on their ID. As a result, I'll rearrange the results to a dict.
        tag_results = {}
        for entry in tag_results_list:
            tag_results[entry["header"]["index_id"]] = entry

        # Kinda looks stupid, but whatever.
        loop = asyncio.get_event_loop()
        tags = []
        for index_id, entry in tag_results.items():
            if index_id == 9: # Danbooru
                r = await loop.run_in_executor(None, functools.partial(fuck_aiohttp.get, "https://danbooru.donmai.us/posts/" + str(entry["data"]["danbooru_id"]) + ".json"))
                j = r.json()
                tags += j["tag_string"].split()
            if index_id == 12: # Yande.re # pragma: no cover
                r = await loop.run_in_executor(None, functools.partial(fuck_aiohttp.get, "https://yande.re/post.json", params={"tags": "id:" + str(entry["data"]["yandere_id"])}))
                j = r.json()
                tags += j[0]["tags"].split()
            if index_id == 26: # Konachan # pragma: no cover
                r = await loop.run_in_executor(None, functools.partial(fuck_aiohttp.get, "http://konachan.com/post.json", params={"tags": "id:" + str(entry["data"]["konachan_id"])}))
                j = r.json()
                tags += j[0]["tags"].split()

        return ImageResult(tags, source, None)