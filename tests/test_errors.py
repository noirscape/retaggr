import retaggr
import pytest

def test_enginecooldown_exception():
    with pytest.raises(retaggr.EngineCooldownException) as exc_info:
        raise retaggr.EngineCooldownException("a")

    assert exc_info.value.until is "a"
