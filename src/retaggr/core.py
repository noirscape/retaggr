# stdlib
from collections import namedtuple

# Config
from retaggr.config import ReverseSearchConfig

# Boorus
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
            if hasattr(self.config, "e621_username") and hasattr(self.config, "app_name") and hasattr(self.config, "version"):
                self.accessible_engines["e621"] = E621(self.config.e621_username, self.config.app_name, self.config.version, self.config.min_score)
            self.accessible_engines["iqdb"] = Iqdb(self.config.min_score)

        if hasattr(self.config, "saucenao_api_key"):
            self.accessible_engines["saucenao"] = SauceNao(self.config.saucenao_api_key)

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
            if self.accessible_engines[engine].download_required:
                if not download:
                    continue
            try:
                result = await self.search_image(engine, url)
            except EngineCooldownException: # pragma: no cover
                pass
            else:
                tags.update(result.tags)
                if result.source:
                    source.update(result.source)
                if result.rating:
                    rating.update(result.rating)
                if callback:
                    await callback(engine, ReverseResult(result.tags, result.source, result.rating))
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
