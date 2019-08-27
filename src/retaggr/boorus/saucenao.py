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


    tag_indexes = set([5, 9, 12, 26, 29])
    """Tag indexes we can parse.

    Valid index numbers can be found at https://saucenao.com/status.html .

    List of indexes we can parse for tags:

    * 9: Danbooru
    * 12: Yande.re
    * 26: Konachan
    * 29: E621
    """

    source_indexes = [5, 16, 37, 34]
    """List of source indexes in preferred order.
    
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
        request_url = "https://saucenao.com/search.php"
        params = {
            "db": "999", # No clever bitmasking -> need help with how to do that.
            "api_key": self.api_key,
            "output_type": "2", # 2 is the JSON API,
            "url": url
        }
        r = fuck_aiohttp.get(request_url, params=params)
        return r.json()

    async def search_tag(self, tag):
        raise NotAvailableSearchOption("This engine cannot search tags.")

    async def index_parser(self, json):
        """Parse the output from a succesful saucenao search to retrieve data from specific indexes.
        
        :param json: JSON output from the API.
        :type json: dict
        """
        pass