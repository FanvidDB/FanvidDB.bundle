API_KEY = ''

def Start():
    Log.Info('Starting FanvidDB metadata agent!')


def ValidatePrefs():
    Log.Info('Validating metadata against preferences!')
    global API_KEY
    API_KEY = Prefs.get('fanviddb_api_key')
    Log.Info('API Key')
    Log.Info(API_KEY)


class FanvidDBAgent(Agent.Movies):
    name = 'FanvidDB'
    primary_provider = True
    fallback_agent = False
    contributes_to = None
    accepts_from = None
    languages = [Locale.Language.NoLanguage]

    def search(self, results, media, lang, manual=False):
        Log.Info('asdf')
        for a in dir(media):
            if not a.startswith('_'):
                Log.Info('%s: %s', a, getattr(media, a))
        Log.Info('fdsa')
        results.Append(MetadataSearchResult(
            id='youtube-dl|{}|{}'.format(media.filename, media.openSubtitlesHash),
            name=media.title,
            year=None,
            lang=lang,
            score=100
        ))

        results.Sort('score', descending=True)

    def update(self, metadata, media, lang):
        metadata.rating = 4.2  # out of 10 lmao
        metadata.content_rating = 'mature rating'
        #metadata.art
        #metadata.chapters
        metadata.themes = ['theme a', 'theme b']
        metadata.quotes = ['quote me once', 'quote me twice']
        metadata.year = 2222
        #metadata.duration
        metadata.rating_count = 5
        metadata.genres = ['genre a', 'genre b']
        #metadata.title
        metadata.tagline = 'tagline believe it'
        metadata.content_rating_age = 55
        #metadata.writers
        #metadata.collections
        metadata.trivia = 'sounds trivial to me'
        #metadata.tags
        #metadata.audience_rating_image
        #metadata.rating_image
        #metadata.producers = ['producer a', 'producer b']
        metadata.audience_rating = 6.9
        metadata.studio = 'Studio 60'
        #metadata.posters
        #metadata.countries
        #metadata.roles
        #metadata.originally_available_at
        #metadata.title_sort
        #metadata.original_title
        metadata.summary = 'summarize but good'
        #metadata.reviews
        #metadata.directors
        #metadata.extras
        #metadata.banners
        #metadata.similar
