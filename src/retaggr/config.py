class ReverseSearchConfig:
    """
    Configuration object for :class:`ReverseSearch`

    All parameters are prefixed with the specific type needed for reverse searching.

    Check the relevant class for the engine for details on the engine.

    :param danbooru_username: Username on :class:`Danbooru`
    :type danbooru_username: str
    :param danbooru_api_key: API key on :class:`Danbooru`
    :type danbooru_api_key: 
    :param e621_username: Your :class:`E621` username
    :type e621_username: str

    :param app_name: The name of your application (required for the e621 handler in :class:`SauceNao`).
    :type app_name: str
    :param version: The version of your application (required for the e621 handler in :class:`SauceNao`).
    :type version: float

    :param saucenao_api_key: An API key for :class:`SauceNao`.
    :type saucenao_api_key: str

    :param min_score: Minimum search match percentage needed (required for ALL boorus except :class:`Paheal` and :class:`SauceNao`).
    :type min_score: float

    :param skip_iqdb: Don't instantiate the :class:`IQDB` class.
    :type skip_iqdb: bool
    """
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)