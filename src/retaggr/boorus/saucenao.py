from retaggr.boorus.base import Booru
from retaggr.errors import NotAvailableSearchOption
from aiohttp_requests import requests

class SauceNao(Booru):
    """Reverse searches the SauceNao API and then does additional matching.

    This booru does not require images to be downloaded before searching.

    This API is subject to rate limits.
    :param api_key: SauceNao API key. You can get this by registering an account on saucenao.com
    :type api_key: str
    """
    host = "https://saucenao.com"
    download_required = False

    def __init__(self, api_key):
        self.api_key = api_key

    async def search_image(self, url):
        request_url = "https://saucenao.com/search.php"
        params = {
            "db": "999", # No clever bitmasking -> need help with how to do that.
            "api_key": self.api_key,
            "output_type": "2" # 2 is the JSON API
        }
        await requests.get(request_url, params=params)

    async def search_tag(self, tag):
        raise NotAvailableSearchOption("This engine cannot search tags.")