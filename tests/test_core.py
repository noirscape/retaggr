import pytest
import retaggr
import os

danbooru_username = os.environ.get('DANBOORU_USERNAME', None)
danbooru_api_key = os.environ.get('DANBOORU_API_KEY', None)
e621_username = os.environ.get('E621_USERNAME', None)
app_name = os.environ.get('APP_NAME', None)
version = os.environ.get('APP_VERSION', None)
if not all([danbooru_username, danbooru_api_key, e621_username, app_name, version]):
    raise ValueError("Missing Environment variables")
config = retaggr.ReverseSearchConfig(danbooru_username=danbooru_username, danbooru_api_key=danbooru_api_key, e621_username=e621_username, app_name=app_name, version=version)

def test_core_creation():
    core = retaggr.ReverseSearch(config)
    assert core.config == config