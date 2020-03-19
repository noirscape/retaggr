from typing import Set

class SauceNaoHandler:
    """Base class to handle SauceNao engine results.

    :ivar engine_id: The engine ID. Engine IDs can be located on https://saucenao.com/status.html.
    :vartype engine_id: int
    """
    engine_id = None

    tag_capable = False
    source_capable = False

    async def get_tag_data(self, data) -> Set[str]:
        """Get all the tags matching the supplied data."""
        pass

    async def get_source_data(self, data) -> Set[str]:
        """Extract the source from the supplied data."""
        pass