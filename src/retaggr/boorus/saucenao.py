from retaggr.boorus.base import Booru
from retaggr.errors import NotAvailableSearchOption
import requests as fuck_aiohttp

class SauceNao(Booru):
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

    def __init__(self, api_key):
        self.api_key = api_key

    async def search_image(self, url):
        result =  await self.search_image_source(url)
        return result["tags"]

    async def search_image_source(self, url):
        request_url = "https://saucenao.com/search.php"
        params = {
            "db": "999", # No clever bitmasking -> need help with how to do that.
            "api_key": self.api_key,
            "output_type": "2", # 2 is the JSON API,
            "url": url
        }
        r = fuck_aiohttp.get(request_url, params=params)
        return await self.index_parser(r.json())

    async def search_tag(self, tag):
        raise NotAvailableSearchOption("This engine cannot search tags.")

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
        tags = []
        for index_id, entry in tag_results.items():
            if index_id == 9: # Danbooru
                r = fuck_aiohttp.get("https://danbooru.donmai.us/posts/" + str(entry["data"]["danbooru_id"]) + ".json")
                j = r.json()
                tags += j["tag_string"].split()
            if index_id == 12: # Yande.re
                r = fuck_aiohttp.get("https://yande.re/post.json", params={"tags": "id:" + str(entry["data"]["yandere_id"])})
                j = r.json()
                tags += j[0]["tags"].split()
            if index_id == 26: # Konachan
                r = fuck_aiohttp.get("http://konachan.com/post.json", params={"tags": "id:" + str(entry["data"]["konachan_id"])})
                j = r.json()
                tags += j[0]["tags"].split()

        return {"tags": tags, "source": source}