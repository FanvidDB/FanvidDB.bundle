import datetime

from .fanviddb import fanvid_to_search_result
from .fanviddb import get_search_filename
from .fanviddb import update_metadata_from_fanvid


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
    assert search_result.guid == "com.fanviddb.agents.fanvids://12345?lang=xn"
    assert search_result.name == "Title"
    assert search_result.year == 2019
    assert search_result.thumb == "http://example.com"


def test_update_metadata_from_fanvid():
    thumb_url = "http://example.com"
    fanvid = {
        "title": "Title",
        "summary": "summary",
        "rating": "gen",
        "premiere_date": "2019-08-24",
        "thumbnail_url": thumb_url,
        "length": 200,
    }
    # This creates an object that allows setting of arbitrary attributes.
    metadata = type("", (), {})()
    metadata.art = {}
    metadata.posters = {}
    update_metadata_from_fanvid(metadata, fanvid)
    assert metadata.title == "Title"
    assert metadata.summary == "summary"
    assert metadata.content_rating == "gen"
    assert metadata.originally_available_at == datetime.date(2019, 8, 24)
    assert metadata.year == 2019
    assert metadata.art[thumb_url] == thumb_url
    assert metadata.posters[thumb_url] == thumb_url
    assert metadata.duration == 200


def test_update_metadata_from_fanvid__invalid_date():
    # This shouldn't be possible but just in case.
    thumb_url = "http://example.com"
    fanvid = {
        "title": "Title",
        "summary": "summary",
        "rating": "gen",
        "premiere_date": "2019-02-29",
        "thumbnail_url": thumb_url,
        "length": 200,
    }
    # This creates an object that allows setting of arbitrary attributes.
    metadata = type("", (), {})()
    metadata.art = {}
    metadata.posters = {}
    update_metadata_from_fanvid(metadata, fanvid)
    assert metadata.title == "Title"
    assert metadata.summary == "summary"
    assert metadata.content_rating == "gen"
    assert metadata.originally_available_at is None
    assert metadata.year == 2019
    assert metadata.art[thumb_url] == thumb_url
    assert metadata.posters[thumb_url] == thumb_url
    assert metadata.duration == 200


def test_update_metadata_from_fanvid__completely_wrong_date():
    # This shouldn't be possible but just in case.
    thumb_url = "http://example.com"
    fanvid = {
        "title": "Title",
        "summary": "summary",
        "rating": "gen",
        "premiere_date": "quick-brown fox",
        "thumbnail_url": thumb_url,
        "length": 200,
    }
    # This creates an object that allows setting of arbitrary attributes.
    metadata = type("", (), {})()
    metadata.art = {}
    metadata.posters = {}
    update_metadata_from_fanvid(metadata, fanvid)
    assert metadata.title == "Title"
    assert metadata.summary == "summary"
    assert metadata.content_rating == "gen"
    assert metadata.originally_available_at is None
    assert metadata.year is None
    assert metadata.art[thumb_url] == thumb_url
    assert metadata.posters[thumb_url] == thumb_url
    assert metadata.duration == 200
