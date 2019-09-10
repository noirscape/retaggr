## booru-reverse-search
[![Coverage Status](https://coveralls.io/repos/github/booru-utils/retaggr/badge.svg?branch=master)](https://coveralls.io/github/booru-utils/retaggr?branch=master) [![GitHub license](https://img.shields.io/github/license/booru-utils/retaggr)](https://github.com/booru-utils/retaggr/blob/master/LICENSE) [![Build Status](https://travis-ci.org/booru-utils/retaggr.svg?branch=master)](https://travis-ci.org/booru-utils/retaggr)

Library to reverse search various boorus.

See the documentation for details.

## Example

```py
from retaggr import ReverseSearch, ReverseSearchConfig
config = ReverseSearchConfig(min_score=80.0)
rsearch = ReverseSearch(config)
result = asyncio.run(rsearch.reverse_search("https://danbooru.donmai.us/data/__tsukumo_benben_touhou_drawn_by_elise_piclic__6e6da59922b923391f02ba1ce78f9b42.jpg"))
```