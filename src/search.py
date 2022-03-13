"""All code related to interacting with the API."""

import requests
from requests.exceptions import JSONDecodeError as RequestsJSONDecodeError

from .plex import Log


def build_search_query(filename):
    return "whatever"


def search(api_key, query):
    response = requests.get(
        "https://fanviddb.com/api/fanvids", headers={"X-Api-Key": api_key}
    )
    try:
        results = response.json()
    except RequestsJSONDecodeError:
        Log.Error("Could not decode response json: %s", response.text)
        raise
    return results
