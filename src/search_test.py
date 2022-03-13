from .search import fanvid_to_search_result
from .search import get_search_filename


def test_get_search_filename():
    filename = "%2FUsers%2Fusername%2Fpath%2Fto%2Ffanvid%2Ffanvid%20name.mkv"
    expected = "fanvid name.mkv"
    assert get_search_filename(filename) == expected


def test_fanvid_to_search_result():
    fanvid = {
        "uuid": "12345",
        "title": "Title",
        "premiere_date": "2019-08-24",
        "thumbnail_url": "http://example.com",
    }
    search_result = fanvid_to_search_result(fanvid)
    assert search_result.id == "12345"
    assert search_result.guid == "12345"
    assert search_result.name == "Title"
    assert search_result.year == "2019"
    assert search_result.thumb == "http://example.com"
