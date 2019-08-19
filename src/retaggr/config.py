class ReverseSearchConfig:
    """
    Configuration object for :class:`ReverseSearch`

    All parameters are prefixed with the specific type needed for reverse searching.

    Check the relevant classes on the booru for details on the boorus.

    :param danbooru_username: Username on :class:`Danbooru`
    :type danbooru_username: str
    :param danbooru_api_key: API key on :class:`Danbooru`
    :type danbooru_api_key: 
    :param e621_username: Your :class:`E621` username
    :type e621_username: str

    :param app_name: The name of your application (required for :class:`E621`).
    :type app_name: str
    :param version: The version of your application (required for :class:`E621`).
    :type version: float

    :param min_score: Minimum search match percentage needed (required for ALL boorus except :class:`Paheal`).
    :type min_score: float
    """
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)