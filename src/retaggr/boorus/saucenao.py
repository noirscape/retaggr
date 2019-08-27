from retaggr.boorus.base import Booru

class SauceNao(Booru):
    """Reverse searches the SauceNao API and then does additional matching.

    This booru does not require images to be downloaded before searching.

    This API is subject to rate limits.
    :param api_key: SauceNao API key. You can get this by registering an account on saucenao.com
    :type api_key: str
    """
    host = "https://saucenao.com"
    download_required = False

    def __init__(self, api_key):
        self.api_key = api_key