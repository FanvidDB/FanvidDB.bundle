from .plex import Agent
from .plex import Locale
from .plex import Log
from .plex import Prefs
from .plex import SearchResult
from .search import build_search_query
from .search import search
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
    if is_valid_api_key(Prefs[API_KEY_PREF]):
        Log.Info("API key is valid")
    else:
        Log.Info("Invalid API key: {}".format(Prefs[API_KEY_PREF]))


class FanvidDBAgent(Agent.Movies):  # type: ignore
    name = "FanvidDB"
    primary_provider = True
    fallback_agent = False
    contributes_to = None
    accepts_from = None
    languages = [Locale.Language.NoLanguage]  # type: ignore
    version = 1

    def search(
        self, results, tree, hints, lang, manual=False, partial=False, primary=True
    ):
        """
        Triggered by the "Match" action from the video context menu. Queries fanviddb.com
        to get a list of potential matches (with scores) for a given fanvid. Only requires
        a subset of data to be able to display the matching interface.

        Called from agentkit.AgentKit._search. The results should be modified in-place.
        They will be sorted by score by the caller.

        results: Empty object container to fill with potential matches.
        tree: MediaTree object - should have metadata about the parent objects in the current database.
        hints: agentkit.Movie object (subclass of agentkit.MediaObject)
        lang: selected language?
        manual: ???
        partial: ???
        primary: ???
        """
        Log.Debug("results: %s", results)
        Log.Debug("tree: %s", tree)
        Log.Debug("hints: %s", hints)
        Log.Debug("lang: %s", lang)
        Log.Debug("manual: %s", manual)
        Log.Debug("partial: %s", partial)
        Log.Debug("primary: %s", primary)

        for attr in dir(hints):
            if attr.startswith("_"):
                continue
            Log.Debug("hints.%s: %s", attr, getattr(hints, attr))

        query = build_search_query(hints.filename)
        search_results = search(
            api_key=Prefs[API_KEY_PREF],
            query=query,
        )

        for index, result in enumerate(search_results["fanvids"]):
            # SearchResult also supports:
            # - type
            # - matched (?)
            # - parentName
            # - parentID
            # - parentGUID
            # - parentIndex
            results.add(
                SearchResult(
                    index=index,
                    id=result["uuid"],
                    guid=result["uuid"],
                    name=result["title"],
                    year=result["premiere_date"],
                    thumb=result["thumbnail_url"],
                    score=100,
                )
            )

    def update(self, metadata, media, lang):
        """
        Given a single fanvid id, fetch the full record from fanviddb.com.
        """
        Log.Info("asdf")
        metadata.rating = 4.2  # out of 10 lmao
        metadata.content_rating = "mature rating"
        # metadata.art
        # metadata.chapters
        metadata.themes = ["theme a", "theme b"]
        metadata.quotes = ["quote me once", "quote me twice"]
        metadata.year = 2222
        # metadata.duration
        metadata.rating_count = 5
        metadata.genres = ["genre a", "genre b"]
        # metadata.title
        metadata.tagline = "tagline believe it"
        metadata.content_rating_age = 55
        # metadata.writers
        # metadata.collections
        metadata.trivia = "sounds trivial to me"
        # metadata.tags
        # metadata.audience_rating_image
        # metadata.rating_image
        # metadata.producers = ['producer a', 'producer b']
        metadata.audience_rating = 6.9
        metadata.studio = "Studio 60"
        # metadata.posters
        # metadata.countries
        # metadata.roles
        # metadata.originally_available_at
        # metadata.title_sort
        # metadata.original_title
        metadata.summary = "summarize but good"
        # metadata.reviews
        # metadata.directors
        # metadata.extras
        # metadata.banners
        # metadata.similar
