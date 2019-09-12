export DANBOORU_USERNAME=""
export DANBOORU_API_KEY=""
export E621_USERNAME=""
export APP_NAME=""
export APP_VERSION=""
export SAUCENAO_API_KEY=""
py.test --cov=src -W ignore::DeprecationWarning --omit src/retaggr/aiohttp_requests/__init__.py
