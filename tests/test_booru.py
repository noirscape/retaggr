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
if not all([danbooru_username, danbooru_api_key, e621_username, app_name, version]):
    raise ValueError("Missing Environment variables")

@pytest.mark.asyncio
async def test_danbooru():
    booru = boorus.danbooru.Danbooru(danbooru_username, danbooru_api_key, 80.0)
    tags = await booru.search_image("https://danbooru.donmai.us/data/__tsukumo_benben_touhou_drawn_by_elise_piclic__6e6da59922b923391f02ba1ce78f9b42.jpg")
    assert tags == ['1girl', 'alternate_eye_color', 'bangs', 'bare_legs', 'bare_tree', 'barefoot', 'biwa_lute', 'blood', 'bloody_knife', 'bloody_weapon', 'commentary', 'cross-laced_clothes', 'dress', 'elise_(piclic)', 'flower', 'frilled_shirt_collar', 'frilled_sleeves', 'frills', 'grey_dress', 'hair_between_eyes', 'hair_flower', 'hair_ornament', 'holding', 'holding_knife', 'holding_weapon', 'instrument', 'knife', 'left-handed', 'light_particles', 'long_hair', 'long_sleeves', 'looking_at_viewer', 'low_twintails', 'lute_(instrument)', 'night', 'night_sky', 'outdoors', 'purple_hair', 'red_eyes', 'sky', 'solo', 'staff_(music)', 'standing', 'thighs', 'touhou', 'tree', 'tsukumo_benben', 'twintails', 'very_long_hair', 'weapon', 'white_flower', 'wide_sleeves']

@pytest.mark.asyncio
async def test_e621():
    booru = boorus.e621.E621(e621_username, app_name, version, 80.0)
    tags = await booru.search_image("https://static1.e621.net/data/2c/1f/2c1f78fb44f50de8fa5d167757953d57.png")
    assert tags == ['2017', '<3', 'arthropod', 'black_skin', 'blush', 'bottomless', 'breasts', 'clothed', 'clothing', 'featureless', 'female', 'hi_res', 'hollow_knight', 'hornet_(hollow_knight)', 'insect', 'kilinah', 'looking_at_viewer', 'melee_weapon', 'mostly_nude', 'non-mammal_breasts', 'signature', 'solo', 'thick_thighs', 'video_games', 'weapon', 'wide_hips']

@pytest.mark.asyncio
async def test_iqdb():
    booru = boorus.iqdb.Iqdb(80.0)
    tags = await booru.search_image("https://danbooru.donmai.us/data/__tsukumo_benben_touhou_drawn_by_elise_piclic__6e6da59922b923391f02ba1ce78f9b42.jpg")
    assert tags == ['1girl', 'alternate_eye_color', 'bangs', 'bare_legs', 'bare_tree', 'barefoot', 'biwa_lute', 'blood', 'bloody_knife', 'bloody_weapon', 'commentary', 'cross-laced_clothes', 'dress', 'elise_(piclic)', 'flower', 'frilled_shirt_collar', 'frilled_sleeves', 'frills', 'grey_dress', 'hair_between_eyes', 'hair_flower', 'hair_ornament', 'holding', 'holding_knife', 'holding_weapon', 'instrument', 'knife', 'left-handed', 'light_particles', 'long_hair', 'long_sleeves', 'looking_at_viewer', 'low_twintails', 'lute_(instrument)', 'night', 'night_sky', 'outdoors', 'purple_hair', 'red_eyes', 'sky', 'solo', 'staff_(music)', 'standing', 'thighs', 'touhou', 'tree', 'tsukumo_benben', 'twintails', 'very_long_hair', 'weapon', 'white_flower', 'wide_sleeves']

@pytest.mark.asyncio
async def test_paheal():
    booru = boorus.paheal.Paheal()
    tags = await booru.search_image("https://iris.paheal.net/_images/f0a277f7c4e80330b843f8002daf627e/1876780%20-%20Dancer_of_the_Boreal_Valley%20Dark_Souls%20Dark_Souls_3%20Sinensian.jpg")
    assert tags == ['dancer_of_the_boreal_valley', 'dark_souls', 'dark_souls_3', 'sinensian']
