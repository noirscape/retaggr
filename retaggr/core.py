from retaggr.config import ReverseSearchConfig

# Boorus
from retaggr.boorus.danbooru import Danbooru

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
    _all_boorus = ["danbooru"]

    def __init__(self, config):
        self.config = config
        self.accessible_boorus = {}

        if hasattr(self.config, "danbooru_username", "danbooru_api_key"):
            self.accessible_boorus["danbooru"] = Danbooru(self.config.danbooru_username, self.config.danbooru_api_key)

    async def reverse_search(self, url, callback=None, download=False):
        r"""Reverse searches all available boorus for ``url``.

        This automatically silences any and all MissingAPIKeysExceptions that could occur due to lack of initialization.

        ``callback`` is an optional parameter that can refer to a method with a single parameter (``callback(name)``).

        After a reverse search, this method will be called with the booru name that was just searched.

        :param url: The URL to search.
        :type url: str
        :param callback: Callback function.
        :type callback: Optional[function]
        :param download: Run searches on boorus that require a file download.
        :type download: Optional[bool]
        :return: A list of tags
        :rtype: List[str]
        """
        for booru in self.accessible_boorus:
            await self.search_image(booru, url)


    async def search_image(self, booru, url):
        r"""Reverse search a booru for ``url``.

        :param booru: Booru to search, this must match a filename in the boorus folder.
        :type booru: str
        :param url: The URL to search.
        :type url: str
        :raises MissingAPIKeysException: Required keys in config object missing.
        :raises NotAValidBooruException: The passed in booru is not a valid booru.
        :return: A list of tags
        :rtype: List[str]
        """
        if booru not in self._all_boorus:
            raise NotAValidBooruException("%s is not a valid booru", booru)
        if booru not in self.accessible_boorus:
            raise MissingAPIKeysException("%s is misisng one or more needed API keys. Check the documentation.")
        self.accessible_boorus[booru].search_image(url)