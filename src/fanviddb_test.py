import datetime

from .factories_test import FanvidFactory
from .factories_test import MockMetadata
from .fanviddb import fanvid_to_search_result
from .fanviddb import get_search_filename
from .fanviddb import update_metadata_from_fanvid


def test_get_search_filename():
    filename = "%2FUsers%2Fusername%2Fpath%2Fto%2Ffanvid%2Ffanvid%20name.mkv"
    expected = "fanvid name.mkv"
    assert get_search_filename(filename) == expected


def test_fanvid_to_search_result():
    fanvid = FanvidFactory()
    search_result = fanvid_to_search_result(fanvid)
    assert search_result.id == fanvid["uuid"]
    assert search_result.guid == "com.fanviddb.agents.fanvids://{}?lang=xn".format(
        fanvid["uuid"]
    )
    assert search_result.name == fanvid["title"]
    assert search_result.year == int(fanvid["premiere_date"].split("-")[0])
    assert search_result.thumb == fanvid["thumbnail_url"]


def test_update_metadata_from_fanvid():
    fanvid = FanvidFactory(premiere_date="2019-08-24")
    # This creates an object that allows setting of arbitrary attributes.
    metadata = MockMetadata()
    update_metadata_from_fanvid(metadata, fanvid)
    assert metadata.title == fanvid["title"]
    assert metadata.summary == fanvid["summary"]
    assert metadata.content_rating == fanvid["rating"]
    assert metadata.originally_available_at == datetime.date(2019, 8, 24)
    assert metadata.year == 2019
    assert metadata.art[fanvid["thumbnail_url"]] == fanvid["thumbnail_url"]
    assert metadata.posters[fanvid["thumbnail_url"]] == fanvid["thumbnail_url"]
    assert metadata.duration == fanvid["length"]


def test_update_metadata_from_fanvid__invalid_date():
    # This shouldn't be possible but just in case.
    fanvid = FanvidFactory(premiere_date="2019-02-29")
    # This creates an object that allows setting of arbitrary attributes.
    metadata = MockMetadata()
    update_metadata_from_fanvid(metadata, fanvid)
    assert metadata.originally_available_at is None
    assert metadata.year == 2019


def test_update_metadata_from_fanvid__completely_wrong_date():
    # This shouldn't be possible but just in case.
    fanvid = FanvidFactory(premiere_date="quick-brown fox")
    # This creates an object that allows setting of arbitrary attributes.
    metadata = MockMetadata()
    update_metadata_from_fanvid(metadata, fanvid)
    assert metadata.originally_available_at is None
    assert metadata.year is None
