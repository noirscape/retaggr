class MissingAPIKeysException(Exception):
    """Raised if a required API key to search an engine is missing."""
    pass

class NotAValidEngineException(Exception):
    """Raised if the passed in engine does not exist."""

class NotAvailableSearchException(Exception):
    """This engine is not capable of searching this option."""

class EngineCooldownException(Exception):
    """This engine is on cooldown.
    
    :ivar datetime.datetime until: The period for which this engine is on cooldown."""

    def __init__(self, until):
        self.until = until