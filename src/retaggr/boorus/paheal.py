from retaggr.boorus.base import Booru

# External imports
import hashlib
from aiohttp_requests import requests
import xml.etree.ElementTree as ET

class Paheal(Booru):
    """Reverse searches https://rule34.paheal.net for images.

    This booru does require images to be downloaded before searching.
    """
    host = None
    download_required = True

    def __init__(self):
        pass

    async def search_image(self, url: str):
        """Reverse search the Booru for ``url``.
        """
        m = hashlib.md5()
        r = await requests.get(url)
        async for data in r.content.iter_chunked(8192):
            m.update(data)
        md5_hash = m.hexdigest()
        paheal_request = await requests.get(f"http://rule34.paheal.net/api/danbooru/find_posts?md5={md5_hash}")
        xml_tree = ET.fromstring(await paheal_request.text())

        tags = [] # pointless but just in case it's zero, it won't error out.
        for post in xml_tree:
            for tag in post.attrib["tags"].split(): 
                tags.append(tag.lower())
        return tags

    async def search_tag(self, tag: str):
        """Reverse search the booru for tag data.
        """
        raise NotImplementedError("Expand this method to include the logic needed to reverse search.")
