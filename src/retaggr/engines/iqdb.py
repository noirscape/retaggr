from retaggr.engines.base import Engine, ImageResult
from retaggr.errors import NotAvailableSearchException

# External imports
import asyncio
import functools
import requests as fuck_aiohttp
from fake_useragent import UserAgent
from lxml import html

class Iqdb(Engine):
    """Reverse searches https://iqdb.org for images.

    This booru does not required images to be downloaded before searching.

    This method may have unexpected failures relating to HTML parsing. This is because IQDB does not officially offer an API and the raw HTML
    parsing is not functional if the page is not fully loaded.

    :param min_score: Minimum search match percentage needed.
    :type min_score: float
    """
    host = "https://iqdb.org"
    download_required = False

    def __init__(self, min_score):
        self.min_score = min_score
        self.ua = UserAgent()

    async def search_image(self, url):
        tags = []

        params = {"url" : url}
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, functools.partial(fuck_aiohttp.post, self.host, headers={"User-Agent": self.ua.random}, params=params))

        doc = html.fromstring(r.text)
        tables = doc.xpath("//div[@id='pages']/div/table/tr/td")

        row = 6
        while row < len(tables):
            # Percent similair
            if (tables[row].text) is None: # pragma: no cover
                row = row + 6
                continue
            try:
                percent = float(str.split(tables[row].text)[0][:-1])
                # Create tags list
                tags_str = tables[row-2].xpath("//a/img")
                temp_tags = tags_str[0].get('alt').split("Tags: ", 1)[1]
                # IQDBs tag responses leave... something to be desired. To be clear,
                # Given the tag string "a,b, c, D"
                # These two lines should sanitize the tags to
                # ["a", "b", "c", "d"]
                tags = [x.lower().replace(",", " ").split() for x in temp_tags.split()]
                tags = [x for y in tags for x in y]

                if percent > self.min_score:
                    tags.extend(tags)
            except: # pragma: no cover
                pass
            row = row + 6

        return ImageResult(tags, [], None)

    async def search_tag(self, tag):
        """Reverse search the booru for tag data.
        """
        raise NotAvailableSearchException("This engine cannot search tags.")