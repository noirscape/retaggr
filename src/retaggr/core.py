# stdlib
import asyncio
from collections import namedtuple
import logging
import traceback

# Config
from retaggr.config import ReverseSearchConfig

# Engines
from retaggr.engines.base import ImageResult
from retaggr.engines.danbooru import Danbooru
from retaggr.engines.iqdb import Iqdb
from retaggr.engines.paheal import Paheal
from retaggr.engines.saucenao import SauceNao
from retaggr.engines.dummy import Dummy

# Exceptions
from retaggr.errors import MissingAPIKeysException, NotAValidEngineException, EngineCooldownException

ReverseResult = namedtuple("ReverseResult", ["tags", "source", "rating"])
"""The response from a reverse image search. All attributes are Sets.

.. py:attribute:: tags

    The tags the engine has located.

.. py:attribute:: source

    All the sources that have been found for the image.

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
    :param test_mode: Enable test mode. Test mode adds two dummy engines that can fail as well as return some very basic values.
    :type test_mode: bool
    """
    _all_engines = [
        "danbooru",
        "e621",
        "iqdb",
        "paheal",
        "saucenao"
        ]

    def __init__(self, config, test_mode=False):
        self.config = config
        self.accessible_engines = {}

        if hasattr(self.config, "min_score"):
            if hasattr(self.config, "danbooru_username") and hasattr(self.config, "danbooru_api_key"):
                self.accessible_engines["danbooru"] = Danbooru(self.config.danbooru_username, self.config.danbooru_api_key, self.config.min_score)
                logger.info("Created Danbooru engine")

            # IQDB stuff -> we do the check _first_ since someone might not specify this at all, in which case we do still instantiate it.
            if hasattr(self.config, "skip_iqdb") and self.config.skip_iqdb:
                skip_iqdb = True
            else:
                skip_iqdb = False
            if not skip_iqdb:
                self.accessible_engines["iqdb"] = Iqdb(self.config.min_score)
                logger.info("Created IQDB engine")

        if hasattr(self.config, "saucenao_api_key"):
            self.accessible_engines["saucenao"] = SauceNao(self.config.saucenao_api_key)
            logger.info("Created SauceNao engine")
            if hasattr(self.config, "e621_username") and hasattr(self.config, "app_name") and hasattr(self.config, "version"):
                self.accessible_engines["saucenao"].enable_e621(self.config.e621_username, self.config.app_name, self.config.version)
                logger.info("Activated E621 capabilites on saucenao.")

        self.accessible_engines["paheal"] = Paheal()

        if test_mode:
            self.accessible_engines["dummy"] = Dummy(False)
            self.accessible_engines["fail_dummy"] = Dummy(True)
            self._all_engines.append("dummy")
            self._all_engines.append("fail_dummy")

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
        tasks = []
        logger.info("Creating reverse search engine tasks.")
        for engine in self.accessible_engines:
            if self.accessible_engines[engine].download_required:
                if not download:
                    logger.info("[%s] Downloading files has been disabled. Skipping [%s]", url, engine)
                    continue
            tasks.append(self._gather_reverse_task(engine, url, callback))
        results = await asyncio.gather(*tasks)
        for result in results:
            if isinstance(result, Exception): # pragma: no cover
                logger.warning("[%s] An engine has failed!", url)
                logger.warning("[%s] This may or may not be an issue. Report it on the issue tracker: https://github.com/noirscape/retaggr/issues if the issue persists.", url)
                traceback.print_exc()
                continue
            if result.tags:
                tags.update(result.tags)
            if result.source:
                source.update(result.source)
            if result.rating:
                rating.add(result.rating)
        return ReverseResult(tags, source, rating)

    async def _gather_reverse_task(self, engine, url, callback) -> ImageResult:
        """Underlying method used to run reverse_search more asynchronously."""
        logger.info("[%s] Starting search in [%s] engine", url, engine)
        try:
            result = await self.search_image(engine, url)
        except: # pragma: no cover
            # reverse_search just can't except, it's meant to keep trucking no matter what.
            return ImageResult([], None, None)
        else:
            logger.info("[%s][%s] Found tags: %s", url, engine, result.tags)
            logger.info("[%s][%s] Found source: %s", url, engine, result.source)
            logger.info("[%s][%s] Found rating: %s", url, engine, result.rating)
            if callback:
                logger.info("[%s][%s] Executing callback", url, engine)
                await callback(engine, result)
        logger.info("[%s] Finished searching [%s]", url, engine)
        return result

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
