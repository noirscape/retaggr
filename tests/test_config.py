import pytest
import retaggr

def test_create_empty_config():
    config = retaggr.ReverseSearchConfig()
    assert config.__dict__ == {}

def test_create_config_with_variable():
    config = retaggr.ReverseSearchConfig(app_name="py.test")
    assert config.__dict__ == {"app_name": "py.test"}