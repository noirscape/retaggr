from typing import Set

class SauceNaoHandler:
    """Base class to handle SauceNao engine results.
    """
    engine_id = None
    """The engine ID. Engine IDs can be located on https://saucenao.com/status.html."""

    tag_capable = False
    """This determines if the Handler has the ability to retrieve tags. 
    
    If this is false, :meth:`get_tag_data` may not necessarily exist."""

    source_capable = False
    """This determines if the Handler has the ability to retrieve additional source data. 
    
    If this is false, :meth:`get_source_data` may not necessarily exist."""

    async def get_tag_data(self, data) -> Set[str]: # pragma: no cover
        """Get all the tags matching the supplied data."""
        pass

    async def get_source_data(self, data) -> Set[str]: # pragma: no cover
        """Extract the source from the supplied data."""
        pass