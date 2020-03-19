import datetime
import asyncio
from collections import namedtuple

ImageResult = namedtuple("ImageResult", ["tags", "source", "rating"])
"""The response from the engine.

.. py:attribute:: tags

    The tags the engine has located.

.. py:attribute:: source

    The sources that have been found for the image.

.. py:attribute:: rating

    The rating on the image.

"""


class Engine:
    """Base class for an engine.
    
    All the engine classes must derive from this class.

    :ivar host: The base URL for the reverse image domain. This is not an API endpoint, but can be a link to IQDB or something similar.
    :vartype host: str
    :ivar download_required: Determines if the ``search_image()`` function will download the image to be searched beforehand or not.
    :vartype download_required: bool
    :ivar datetime.datetime ~.last_request: Optional. Instance variable that can be set to make use of :meth:`Booru.sleep_until_ratelimit`. Update after making a request. If you just use the library, this should be done by the engine so there's no need to manually set it.
    """
    host = None
    download_required = False

    def __init__(self): # pragma: no cover
        self.last_request = None
        raise NotImplementedError("Expand this method to include all needed keys.")

    async def search_tag(self, tag): # pragma: no cover
        """Reverse search the booru for tag data.
        """
        raise NotImplementedError("Expand this method to include the logic needed to reverse search.")

    async def search_image(self, url): # pragma: no cover
        """Reverse search the engine for ``url``.

        :param str url: URL to search
        :rtype: ImageResult
        """
        raise NotImplementedError("Expand this method to include the logic needed to reverse search.")