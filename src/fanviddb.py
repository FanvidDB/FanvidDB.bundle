"""All code related to interacting with the API."""

import datetime
import os
from urllib import unquote

import requests
from requests.exceptions import JSONDecodeError as RequestsJSONDecodeError

from .plex import HTTP
from .plex import Log
from .plex import Proxy
from .plex import SearchResult

AGENT_IDENTIFIER = "com.fanviddb.agents.fanvids"


try:
    Proxy
except NameError:

    def proxy_url(url):
        return url

else:

    def proxy_url(url):
        return Proxy.Preview(HTTP.Request(url).content, sort_order=1)


def get_search_filename(hints_filename):
    filename = unquote(hints_filename)
    return os.path.basename(filename)


def list_fanvids(api_key, filename):
    url = "https://fanviddb.com/api/fanvids"
    Log.Info("Searching fanviddb at %s", url)
    response = requests.get(url, {"filename": filename}, headers={"X-Api-Key": api_key})
    try:
        fanvids = response.json()
    except RequestsJSONDecodeError:
        Log.Error("Could not decode response json: %s", response.text)
        raise
    Log.Info("Found %s fanvids", fanvids["total_count"])
    return fanvids


def get_fanvid(api_key, uuid):
    url = "https://fanviddb.com/api/fanvids/{}".format(uuid)
    Log.Info("Getting fanvid data at %s", url)
    response = requests.get(url, headers={"X-Api-Key": api_key})
    try:
        fanvid = response.json()
    except RequestsJSONDecodeError:
        Log.Error("Could not decode response json: %s", response.text)
        raise
    return fanvid


def get_premiere_date(fanvid):
    premiere_date = None
    year = None
    if fanvid["premiere_date"]:
        try:
            premiere_date = datetime.datetime.strptime(
                fanvid["premiere_date"], "%Y-%m-%d"
            ).date()
        except ValueError:
            if "-" in fanvid["premiere_date"]:
                try:
                    year = int(fanvid["premiere_date"].split("-", 1)[0])
                except ValueError:
                    pass
        else:
            year = premiere_date.year
    return premiere_date, year


def fanvid_to_search_result(fanvid):
    # Plex uses a special guid format. The lang key needs to match a language
    # "supported" by the Agent. xn represents "no language".
    guid = "{}://{}?lang=xn".format(AGENT_IDENTIFIER, fanvid["uuid"])
    _, year = get_premiere_date(fanvid)
    return SearchResult(
        id=fanvid["uuid"],
        guid=guid,
        name=fanvid["title"],
        year=year,
        thumb=proxy_url(fanvid["thumbnail_url"]),
        score=str(int(fanvid["relevance"] * 100)),
    )


def update_metadata_from_fanvid(metadata, fanvid):
    metadata.title = fanvid["title"]
    metadata.summary = fanvid["summary"]
    metadata.content_rating = fanvid["rating"]

    if fanvid["premiere_date"]:
        premiere_date, year = get_premiere_date(fanvid)
        metadata.originally_available_at = premiere_date
        metadata.year = year

    thumb_url = fanvid["thumbnail_url"]
    if thumb_url not in metadata.art:
        try:
            metadata.art[thumb_url] = proxy_url(fanvid["thumbnail_url"])
        except Exception as e:
            Log.Error(str(e))
    if thumb_url not in metadata.posters:
        try:
            metadata.posters[thumb_url] = proxy_url(fanvid["thumbnail_url"])
        except Exception as e:
            Log.Error(str(e))

    # Plex stores duration in milliseconds; FanvidDB does as well (but it uses floats to do it).
    metadata.duration = int(fanvid["length"])

    # metadata.roles is a Framework.modelling.attributes.SetObject.
    if fanvid["creators"]:
        metadata.roles.clear()
        for creator in fanvid["creators"]:
            role = metadata.roles.new()
            role.role = "Creator"
            role.name = creator

    if fanvid["content_notes"]:
        metadata.summary = "Content Notes: {}\n\n{}".format(
            ", ".join(fanvid["content_notes"]),
            metadata.summary,
        )
