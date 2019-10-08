## retaggr
[![Coverage Status](https://coveralls.io/repos/github/noirscape/retaggr/badge.svg?branch=master)](https://coveralls.io/github/noirscape/retaggr?branch=master) [![GitHub license](https://img.shields.io/github/license/noirscape/retaggr)](https://github.com/noirscape/retaggr/blob/master/LICENSE) [![Build Status](https://travis-ci.org/noirscape/retaggr.svg?branch=master)](https://travis-ci.org/noirscape/retaggr)

Library to reverse search various boorus.

See the documentation for details.

## Example

```py
from retaggr import ReverseSearch, ReverseSearchConfig
config = ReverseSearchConfig(min_score=80.0)
rsearch = ReverseSearch(config)
result = asyncio.run(rsearch.reverse_search("https://danbooru.donmai.us/data/__tsukumo_benben_touhou_drawn_by_elise_piclic__6e6da59922b923391f02ba1ce78f9b42.jpg"))
```

## Licensing

This project is under the GNU LGPLv3 license.

In addition, this project contains a local copy of the aiohttp_requests package (this is to resolve a minor dependency pinning problem aiohttp_requests on pip has). This library is under the MIT. Check the header of the init file for the license.