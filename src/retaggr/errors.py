class MissingAPIKeysException(Exception):
    """Raised if a required API key to search a booru is missing."""
    pass

class NotAValidBooruException(Exception):
    """Raised if the passed in booru does not exist."""