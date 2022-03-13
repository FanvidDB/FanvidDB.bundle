from .plex import Agent
from .plex import Locale
from .plex import Log
from .plex import MetadataSearchResult
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

    def search(self, results, media, lang, manual=False):
        # Trigger with "Match" from video context menu.
        api_key = Prefs[API_KEY_PREF]
        Log.Info("asdf - api key is {}".format(api_key))
        for a in dir(media):
            if not a.startswith("_"):
                Log.Info("%s: %s", a, getattr(media, a))
        Log.Info("fdsa")
        results.Append(
            MetadataSearchResult(
                id="youtube-dl|{}|{}".format(media.filename, media.openSubtitlesHash),
                name=media.title,
                year=None,
                lang=lang,
                score=100,
            )
        )

        results.Sort("score", descending=True)

    def update(self, metadata, media, lang):
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
