class MissingAPIKeysException(Exception):
    """Raised if a required API key to search an engine is missing."""
    pass

class NotAValidEngineException(Exception):
    """Raised if the passed in engine does not exist."""

class NotAvailableSearchException(Exception):
    """This engine is not capable of searching this option."""

class EngineCooldownException(Exception):
    """This engine is on cooldown."""

class EngineIsDown(Exception):
    """The engine is currently not available (eg. Database issues)."""
