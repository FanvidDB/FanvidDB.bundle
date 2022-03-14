from typing import Optional

from .fanviddb import fanvid_to_search_result
from .fanviddb import get_fanvid
from .fanviddb import get_search_filename
from .fanviddb import list_fanvids
from .fanviddb import update_metadata_from_fanvid
from .plex import Agent
from .plex import Locale
from .plex import Log
from .plex import Prefs
from .validate_prefs import is_valid_api_key

API_KEY_PREF = "fanviddb_api_key"


def Start():
    Log.Info("Starting FanvidDB metadata agent!")
    # Call ValidatePrefs so that if there are any issues it shows up in the logs.
    ValidatePrefs()


def ValidatePrefs():
    """
    Called when a user changes their preferences for this plugin. Unfortunately there
    doesn't seem to actually be a way to _return_ a validation error, but we can at least
    log it.
    """
    Log.Info("Validating API key")
    api_key = Prefs[API_KEY_PREF]  # type: Optional[str]

    if api_key:
        if is_valid_api_key(api_key):
            Log.Info("API key is valid")
        else:
            Log.Info("Invalid API key: {}".format(Prefs[API_KEY_PREF]))
    else:
        Log.Info("API key is not set")


class FanvidDBAgent(Agent.Movies):  # type: ignore
    name = "FanvidDB"
    primary_provider = True
    fallback_agent = False
    contributes_to = None
    accepts_from = None
    languages = [Locale.Language.NoLanguage]  # type: ignore
    # version is used to change some functionality within a single Framework version.
    # However, metadata management for Movie objects only works in version `0`.
    version = 0

    def search(self, results, media, lang, tree=None):
        """
        Triggered by the "Match" action from the video context menu. Queries fanviddb.com
        to get a list of potential matches (with scores) for a given fanvid. Only requires
        a subset of data to be able to display the matching interface.

        Called from agentkit.AgentKit._search. The results should be modified in-place.
        They will be sorted by score by the caller.

        results: Empty object container to fill with potential matches.
        media: agentkit.Movie object (subclass of agentkit.MediaObject)
        lang: selected language?
        tree: MediaTree object - should have metadata about the parent objects in the current database.

        This could support some additional args but it's not clear what they're for.
        """
        Log.Debug("results: %s", results)
        Log.Debug("media: %s", media)
        Log.Debug("lang: %s", lang)
        Log.Debug("tree: %s", tree)

        for attr in dir(media):
            if attr.startswith("_"):
                continue
            Log.Debug("media.%s: %s", attr, getattr(media, attr))

        api_key = Prefs[API_KEY_PREF]
        if not api_key:
            Log.Info("API Key is not set. Not able to list fanvids from fanviddb.com.")
            return

        search_results = list_fanvids(
            api_key=Prefs[API_KEY_PREF],
            filename=get_search_filename(media.filename),
        )

        for fanvid in search_results["fanvids"]:
            results.add(fanvid_to_search_result(fanvid))

    def update(self, metadata, media, lang):
        """
        Given a single fanvid id, fetch the full record from fanviddb.com. This is triggered
        at various times, including after a match. However, there are a number of non-obvious
        reasons the caller might short-circuit.

        metadata: the metadata object. Manipulate this object in-place; after return it will be written to the database.
        media: the object from the database.
        lang: selected language?

        This could support some additional args but it's not clear what they're for.
        """
        Log.Info("Updating metadata for %s", metadata)
        api_key = Prefs[API_KEY_PREF]
        if not api_key:
            Log.Info("API Key is not set. Not able to get fanvids from fanviddb.com.")
            return
        fanvid = get_fanvid(api_key, metadata.id)
        update_metadata_from_fanvid(metadata, fanvid)
