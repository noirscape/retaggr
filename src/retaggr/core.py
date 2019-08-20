from retaggr.config import ReverseSearchConfig

# Boorus
from retaggr.boorus.danbooru import Danbooru
from retaggr.boorus.e621 import E621
from retaggr.boorus.iqdb import Iqdb
from retaggr.boorus.paheal import Paheal

# Exceptions
from retaggr.errors import MissingAPIKeysException, NotAValidBooruException

class ReverseSearch:
    r"""Core class used for Reverse Searching. 
    
    This class can only be instantiated with a :class:`ReverseSearchConfig` instance.

    All listed methods can only be ran from an asynchronous context.

    :ivar accessible_boorus: The accessible boorus from the passed in configuration object.
    :param config: The config object.
    :type config: ReverseSearchConfig
    """
    _all_boorus = [
        "danbooru",
        "e621",
        "iqdb",
        "paheal"
        ]

    def __init__(self, config):
        self.config = config
        self.accessible_boorus = {}

        if hasattr(self.config, "min_score"):
            if hasattr(self.config, "danbooru_username") and hasattr(self.config, "danbooru_api_key"):
                self.accessible_boorus["danbooru"] = Danbooru(self.config.danbooru_username, self.config.danbooru_api_key, self.config.min_score)
            if hasattr(self.config, "e621_username") and hasattr(self.config, "app_name") and hasattr(self.config, "version"):
                self.accessible_boorus["e621"] = E621(self.config.e621_username, self.config.app_name, self.config.version, self.config.min_score)
            self.accessible_boorus["iqdb"] = Iqdb(self.config.min_score)

        self.accessible_boorus["paheal"] = Paheal()

    async def reverse_search(self, url, callback=None, download=False):
        r"""Reverse searches all accessible boorus for ``url``.

        ``callback`` is an optional parameter that can refer to a method with a single parameter (``callback(name)``).

        After a reverse search, this method will be called with the booru name that was just searched.

        :param url: The URL to search.
        :type url: str
        :param callback: Callback function.
        :type callback: Optional[function]
        :param download: Run searches on boorus that require a file download. Defaults to False.
        :type download: Optional[bool]
        :return: A set of tags
        :rtype: Set[str]
        """
        tags = set()
        for booru in self.accessible_boorus:
            if self.accessible_boorus[booru].download_required:
                if not download:
                    continue
            tags.update(await self.search_image(booru, url))
            if callback:
                callback(booru)
        return tags


    async def search_image(self, booru, url):
        r"""Reverse search a booru for ``url``.

        :param booru: Booru to search, this must match a filename in the boorus folder.
        :type booru: str
        :param url: The URL to search.
        :type url: str
        :raises MissingAPIKeysException: Required keys in config object missing.
        :raises NotAValidBooruException: The passed in booru is not a valid booru.
        :return: A set of tags
        :rtype: Set[str]
        """
        if booru not in self._all_boorus:
            raise NotAValidBooruException("%s is not a valid booru", booru)
        if booru not in self.accessible_boorus:
            raise MissingAPIKeysException("%s is misisng one or more needed API keys. Check the documentation.")
        return set(await self.accessible_boorus[booru].search_image(url))