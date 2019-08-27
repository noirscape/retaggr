import retaggr
import retaggr.boorus as boorus
import os
import pytest

# Grab the relevant keys from the environment
danbooru_username = os.environ.get('DANBOORU_USERNAME', None)
danbooru_api_key = os.environ.get('DANBOORU_API_KEY', None)
e621_username = os.environ.get('E621_USERNAME', None)
app_name = os.environ.get('APP_NAME', None)
version = os.environ.get('APP_VERSION', None)
saucenao_api_key = os.environ.get('SAUCENAO_API_KEY', None)
if not all([danbooru_username, danbooru_api_key, e621_username, app_name, version, saucenao_api_key]):
    raise ValueError("Missing Environment variables")

@pytest.mark.asyncio
async def test_danbooru():
    booru = boorus.danbooru.Danbooru(danbooru_username, danbooru_api_key, 80.0)
    tags = await booru.search_image("https://danbooru.donmai.us/data/__tsukumo_benben_touhou_drawn_by_elise_piclic__6e6da59922b923391f02ba1ce78f9b42.jpg")
    assert 'tsukumo_benben' in tags

@pytest.mark.asyncio
async def test_e621():
    booru = boorus.e621.E621(e621_username, app_name, version, 80.0)
    tags = await booru.search_image("https://static1.e621.net/data/2c/1f/2c1f78fb44f50de8fa5d167757953d57.png")
    assert 'hornet_(hollow_knight)' in tags

@pytest.mark.asyncio
async def test_iqdb():
    booru = boorus.iqdb.Iqdb(80.0)
    tags = await booru.search_image("https://danbooru.donmai.us/data/__tsukumo_benben_touhou_drawn_by_elise_piclic__6e6da59922b923391f02ba1ce78f9b42.jpg")
    assert 'biwa_lute' in tags

@pytest.mark.asyncio
async def test_paheal():
    booru = boorus.paheal.Paheal()
    tags = await booru.search_image("https://iris.paheal.net/_images/f0a277f7c4e80330b843f8002daf627e/1876780%20-%20Dancer_of_the_Boreal_Valley%20Dark_Souls%20Dark_Souls_3%20Sinensian.jpg")
    assert 'dancer_of_the_boreal_valley' in tags

@pytest.mark.asyncio
async def test_saucenao():
    booru = boorus.saucenao.SauceNao(saucenao_api_key)
    tags = await booru.search_image("https://danbooru.donmai.us/data/__priscilla_the_crossbreed_souls_from_software_and_etc_drawn_by_setz__a3ed9fbb7e972145dfe98269e0be1ace.jpg")
    assert 'priscilla_the_crossbreed' in tags