from retaggr.boorus.base import Booru

# External modules
import asyncio
import requests as fuck_aiohttp
from aiohttp_requests import requests
import functools
import time
from lxml import html

class E621(Booru):
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

    def __init__(self, username, app_name, version, min_score):
        self.user_agent = {"User-Agent": f"{app_name}/{version} (by {username} on e621)"}
        self.min_score = min_score

    async def search_image(self, url: str):
        """Reverse search the Booru for ``url``.

        CRUCIAL: This implementation blocks for 1 second in order to not overload the e621 API.
        """
        results = []

        params = {"url" : url}

        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, functools.partial(fuck_aiohttp.post, self.host, params=params))
        time.sleep(1)

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
                    r = await requests.get(self.e621_api, headers=self.user_agent, params={"id": post_id})
                    json = await r.json()
                    results = json['tags'].split()
            except:
                pass
            row = row + 5
        return results

    async def search_tag(self, tag: str):
        """Reverse search the booru for tag data.
        """
        raise NotImplementedError("Expand this method to include the logic needed to reverse search.")