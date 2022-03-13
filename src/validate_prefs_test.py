import pytest

from .validate_prefs import is_valid_api_key


@pytest.mark.parametrize(
    "api_key,valid",
    [
        ("abc_def", True),
        ("Ab2_zZ3", True),
        ("1je_a", False),
        ("Aje_a-", False),
        ("https://google.com", False),
    ],
)
def test_is_valid_api_key(api_key, valid):
    assert is_valid_api_key(api_key) == valid
