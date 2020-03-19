from retaggr.engines.base import Engine, ImageResult

# External modules
import asyncio
import requests as fuck_aiohttp
import functools

class Dummy(Engine):
    """A dummy engine that's only useful for testing.
    """
    host = "https://danbooru.donmai.us"
    download_required = False

    def __init__(self, fail):
        self.fail = fail

    async def search_image(self, url):
        if self.fail:
            raise Exception("Task failed (intentional)")
        else:
            return ImageResult(["test"], ["test"], "safe")