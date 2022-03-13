"""All code related to interacting with the API."""

import os
from urllib import unquote

import requests
from requests.exceptions import JSONDecodeError as RequestsJSONDecodeError

from .plex import Log
from .plex import SearchResult


def get_search_filename(hints_filename):
    filename = unquote(hints_filename)
    return os.path.basename(filename)


def search(api_key, filename):
    response = requests.get(
        "https://fanviddb.com/api/fanvids", headers={"X-Api-Key": api_key}
    )
    try:
        results = response.json()
    except RequestsJSONDecodeError:
        Log.Error("Could not decode response json: %s", response.text)
        raise
    return results


def fanvid_to_search_result(fanvid):
    return SearchResult(
        id=fanvid["uuid"],
        guid=fanvid["uuid"],
        name=fanvid["title"],
        year=fanvid["premiere_date"].split("-", 1)[0],
        thumb=fanvid["thumbnail_url"],
        score=100,
    )
