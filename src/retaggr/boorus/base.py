class Booru:
    """Base class for a booru.
    
    All the booru classes must derive from this class.

    :ivar host: The base URL for the reverse image domain. This is not an API endpoint, but can be a link to IQDB or something similar.
    :vartype host: str
    :ivar download_required: Determines if the ``search_image()`` function will download the image to be searched beforehand or not.
    :vartype download_required: bool"""
    host = None
    download_required = False

    def __init__(self):
        raise NotImplementedError("Expand this method to include all needed keys.")

    async def search_image(self, url: str):
        """Reverse search the Booru for ``url``.
        """
        raise NotImplementedError("Expand this method to include the logic needed to reverse search.")

    async def search_tag(self, tag: str):
        """Reverse search the booru for tag data.
        """
        raise NotImplementedError("Expand this method to include the logic needed to reverse search.")
