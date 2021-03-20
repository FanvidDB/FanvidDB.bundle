AGENT_CACHE_TIME = CACHE_1HOUR * 24
API_KEY = ''


def Start():
    Log.Info('Starting FanvidDB metadata agent!')


def ValidatePrefs():
    Log.Info('Validating FanvidDB metadata agent preferences!')
    global API_KEY
    API_KEY = Prefs.get('fanviddb_api_key')


class FanvidDBAgent(Agent.Movies):
    name = 'FanvidDB'
    primary_provider = True
    fallback_agent = None
    accepts_from = ['com.plexapp.agents.localmedia']
    languages = [Locale.Language.NoLanguage]

    def search(self, results, media, lang):
        Log.Info(media)
        Log.Info(media.__dict__)
        results.Append(MetadataSearchResult(id=media.id, name=media.name, score=86, lang=lang))

    def update(self, metadata, media, lang):
        pass
