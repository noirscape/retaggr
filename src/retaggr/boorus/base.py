class Booru:
    """Base class for a booru.
    
    All the booru classes must derive from this class.

    :ivar host: The base URL for the reverse image domain. This is not an API endpoint, but can be a link to IQDB or something similar.
    :vartype host: str
    :ivar download_required: Determines if the ``search_image()`` function will download the image to be searched beforehand or not.
    :vartype download_required: bool"""
    host = None
    download_required = False

    def __init__(self): # pragma: no cover
        raise NotImplementedError("Expand this method to include all needed keys.")

    async def search_image(self, url):
        """
        .. deprecated:: 1.2
            Use :meth:`Booru.search_image_source` instead
        """
        result = await self.search_image_source(url)
        return result["tags"]

    async def search_tag(self, tag): # pragma: no cover
        """Reverse search the booru for tag data.
        """
        raise NotImplementedError("Expand this method to include the logic needed to reverse search.")

    async def search_image_source(self, url): # pragma: no cover
        """Reverse search the booru for ``url``.

        This method should return a dict with two keys:

        * source: Contains a string that is the source URL. Can be None if not found or if the Engine doesn't support it.
        * tags: Contains a list of tags. Can be empty if the Engine doesn't support it.

        :param str url: URL to search
        :return str: dict[str, Set]
        """
        raise NotImplementedError("Expand this method to include the logic needed to reverse search.")