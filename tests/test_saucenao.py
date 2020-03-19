import os
import pytest
import retaggr
import retaggr.engines.saucenao.handlers as handlers
from retaggr.engines import SauceNao

e621_username = os.environ.get('E621_USERNAME', None)
app_name = os.environ.get('APP_NAME', None)
version = os.environ.get('APP_VERSION', None)
if not all([e621_username, app_name, version]):
    raise ValueError("Missing Environment variables")

@pytest.mark.asyncio
async def test_saucenao():
    engine = SauceNao(None, True)
    engine.enable_e621(e621_username, app_name, version)
    answer = await engine.search_image(None)
    assert "touhou" in answer.tags

@pytest.mark.asyncio
async def test_danbooru():
    handler = handlers.DanbooruHandler()
    data = {"danbooru_id": 3820633}
    answer = await handler.get_tag_data(data)
    assert "persona" in answer

@pytest.mark.asyncio
async def test_e621_tags():
    handler = handlers.E621Handler(e621_username, app_name, version)
    data = {"e621_id": 2174881}
    answer = await handler.get_tag_data(data)
    assert "hornet_(hollow_knight)" in answer

@pytest.mark.asyncio
async def test_e621_source():
    handler = handlers.E621Handler(e621_username, app_name, version)
    data = {"e621_id": 2174881}
    answer = await handler.get_source_data(data)
    assert "https://twitter.com/kililewd/status/1237068755521462273?s=19" in answer

@pytest.mark.asyncio
async def test_konachan():
    handler = handlers.KonachanHandler()
    data = {"konachan_id": 303016}
    answer = await handler.get_tag_data(data)
    assert "no-kan" in answer

@pytest.mark.asyncio
async def test_yandere():
    handler = handlers.YandereHandler()
    data = {"yandere_id": 618735}
    answer = await handler.get_tag_data(data)
    assert "pantsu" in answer

@pytest.mark.asyncio
async def test_saucenao_tag():
    engine = SauceNao(None, True)
    with pytest.raises(retaggr.NotAvailableSearchException):
        await engine.search_tag("doesnt matter")
