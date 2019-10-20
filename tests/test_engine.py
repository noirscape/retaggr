import retaggr
import retaggr.engines as engines
import os
import pytest
import time

# Logging
import logging
logging.basicConfig(level=logging.DEBUG)

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
    engine = engines.danbooru.Danbooru(danbooru_username, danbooru_api_key, 80.0)
    result = await engine.search_image("https://danbooru.donmai.us/data/__tsukumo_benben_touhou_drawn_by_elise_piclic__6e6da59922b923391f02ba1ce78f9b42.jpg")
    assert 'tsukumo_benben' in result.tags

@pytest.mark.asyncio
async def test_e621():
    time.sleep(1) # We have to do this, otherwise e621 API blocks us. It's only an issue for testing this here.
    engine = engines.e621.E621(e621_username, app_name, version, 80.0)
    try:
        result = await engine.search_image("https://static1.e621.net/data/2c/1f/2c1f78fb44f50de8fa5d167757953d57.png")
    except retaggr.BooruIsDown as e:
        pytest.xfail(f"E621 failed with the following exception: {repr(e)}")
    assert 'hornet_(hollow_knight)' in result.tags


@pytest.mark.asyncio
async def test_iqdb():
    engine = engines.iqdb.Iqdb(80.0)
    result = await engine.search_image("https://danbooru.donmai.us/data/__tsukumo_benben_touhou_drawn_by_elise_piclic__6e6da59922b923391f02ba1ce78f9b42.jpg")
    assert 'biwa_lute' in result.tags

@pytest.mark.asyncio
async def test_iqdb_tag():
    engine = engines.iqdb.Iqdb(80.0)
    with pytest.raises(retaggr.NotAvailableSearchException):
        await engine.search_tag("doesnt matter")

@pytest.mark.asyncio
async def test_paheal():
    engine = engines.paheal.Paheal()
    result = await engine.search_image("https://iris.paheal.net/_images/f0a277f7c4e80330b843f8002daf627e/1876780%20-%20Dancer_of_the_Boreal_Valley%20Dark_Souls%20Dark_Souls_3%20Sinensian.jpg")
    assert 'dancer_of_the_boreal_valley' in result.tags

@pytest.mark.asyncio
async def test_paheal_tag():
    engine = engines.paheal.Paheal()
    with pytest.raises(retaggr.NotAvailableSearchException):
        await engine.search_tag("doesnt matter")

@pytest.mark.asyncio
async def test_saucenao():
    engine = engines.saucenao.SauceNao(saucenao_api_key)
    result = await engine.search_image("https://danbooru.donmai.us/data/__priscilla_the_crossbreed_souls_from_software_and_etc_drawn_by_setz__a3ed9fbb7e972145dfe98269e0be1ace.jpg")
    assert 'priscilla_the_crossbreed' in result.tags

@pytest.mark.asyncio
async def test_saucenao_tag():
    engine = engines.saucenao.SauceNao(saucenao_api_key)
    with pytest.raises(retaggr.NotAvailableSearchException):
        await engine.search_tag("doesnt matter")
