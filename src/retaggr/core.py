# stdlib
from collections import namedtuple
import logging

# Config
from retaggr.config import ReverseSearchConfig

# Engines
from retaggr.engines.danbooru import Danbooru
from retaggr.engines.e621 import E621
from retaggr.engines.iqdb import Iqdb
from retaggr.engines.paheal import Paheal
from retaggr.engines.saucenao import SauceNao

# Exceptions
from retaggr.errors import MissingAPIKeysException, NotAValidEngineException, EngineCooldownException

ReverseResult = namedtuple("ReverseResult", ["tags", "source", "rating"])
"""The response from a reverse image search. All attributes are Sets.

.. py:attribute:: tags

    The tags the engine has located.

.. py:attribute:: source

    The source that has been found for the image.

.. py:attribute:: rating

    The rating on the image.

"""

# Set up logger
logger = logging.getLogger(__name__)

class ReverseSearch:
    r"""Core class used for Reverse Searching. 
    
    This class can only be instantiated with a :class:`ReverseSearchConfig` instance.

    All listed methods can only be ran from an asynchronous context.

    :ivar accessible_engines: The accessible boorus from the passed in configuration object.
    :param config: The config object.
    :type config: ReverseSearchConfig
    """
    _all_engines = [
        "danbooru",
        "e621",
        "iqdb",
        "paheal",
        "saucenao"
        ]

    def __init__(self, config):
        self.config = config
        self.accessible_engines = {}

        if hasattr(self.config, "min_score"):
            if hasattr(self.config, "danbooru_username") and hasattr(self.config, "danbooru_api_key"):
                self.accessible_engines["danbooru"] = Danbooru(self.config.danbooru_username, self.config.danbooru_api_key, self.config.min_score)
                logger.info("Created Danbooru engine")
            if hasattr(self.config, "e621_username") and hasattr(self.config, "app_name") and hasattr(self.config, "version"):
                self.accessible_engines["e621"] = E621(self.config.e621_username, self.config.app_name, self.config.version, self.config.min_score)
                logger.info("Created e621 engine")
            self.accessible_engines["iqdb"] = Iqdb(self.config.min_score)
            logger.info("Created IQDB engine")

        if hasattr(self.config, "saucenao_api_key"):
            self.accessible_engines["saucenao"] = SauceNao(self.config.saucenao_api_key)
            logger.info("Created SauceNao engine")

        self.accessible_engines["paheal"] = Paheal()

    async def reverse_search(self, url, callback=None, download=False):
        """
        Reverse searches all accessible boorus for ``url``.

        .. note::
            Callback is a callback function that can be passed in. This can be used to keep track of
            progress for certain methods and functions.

            .. code-block:: python
               :linenos:

                async def callback(engine, rresult):
                    print("This booru was searched: %s", booru)
                    print("These tags were found: %s", rresult.tags)
                    print("This source was found: %s", rresult.source)
                    print("This rating was found: %s", rresult.rating)

                # Callback will be called each time a search finishes.
                rs.reverse_search(url, callback)

        After a reverse search, this method will be called with the engine name that was just searched.

        :param url: The URL to search.
        :type url: str
        :param callback: Callback function.
        :type callback: Optional[function]
        :param download: Run searches on boorus that require a file download. Defaults to False.
        :type download: Optional[bool]
        :return: A :class:`ReverseResult` instance containing your data.
        :rtype: ReverseResult
        """
        tags = set()
        source = set()
        rating = set()
        for engine in self.accessible_engines:
            logging.info("[%s] Starting search in [%s] engine", url, engine)
            if self.accessible_engines[engine].download_required:
                if not download:
                    logging.info("[%s] Downloading files has been disabled. Skipping [%s]", url, engine)
                    continue
            try:
                result = await self.search_image(engine, url)
            except EngineCooldownException: # pragma: no cover
                pass
            else:
                if result.tags:
                    logging.info("[%s] Found tags: %s", url, result.tags)
                    tags.update(result.tags)
                if result.source:
                    logging.info("[%s] Found source: %s", url, result.source)
                    source.add(result.source)
                if result.rating:
                    logging.info("[%s] Found rating: %s", url, result.rating)
                    rating.add(result.rating)
                if callback:
                    logging.info("[%s] Executing callback", url)
                    await callback(engine, result)
            logging.info("[%s] Finished searching [%s]", url, engine)
        return ReverseResult(tags, source, rating)

    async def search_image(self, booru, url):
        r"""Reverse search a booru for ``url``.

        :param booru: Booru to search, this must match a filename in the boorus folder.
        :type booru: str
        :param url: The URL to search.
        :type url: str
        :raises MissingAPIKeysException: Required keys in config object missing.
        :raises NotAValidEngineException: The passed in booru is not a valid booru.
        :return: A :class:`ImageResult` instance containing your data.
        :rtype: ImageResult
        """
        if booru not in self._all_engines:
            raise NotAValidEngineException("%s is not a valid engine", booru)
        if booru not in self.accessible_engines:
            raise MissingAPIKeysException("%s is misisng one or more needed API keys. Check the documentation.")
        return await self.accessible_engines[booru].search_image(url)
