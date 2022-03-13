# Plex provides a number of "superglobal" variables that are available
# directly within the global namespace without needing to be explicitly
# imported. This file provides some minimal shims so that tests can run.
try:
    Agent = Agent
except NameError:

    class Agent:
        class Movies:
            pass


try:
    Locale = Locale
except NameError:

    class Locale:
        class Language:
            class NoLanguage:
                pass


try:
    Log = Log
except NameError:

    class Log:
        def Info(self, message):
            pass

        def Debug(self, message):
            pass


try:
    Prefs = Prefs
except NameError:

    class Prefs:
        def __getitem__(self, name):
            pass


try:
    SearchResult = SearchResult
except NameError:

    class SearchResult:
        allowed_attrs = set(
            [
                "type",
                "id",
                "name",
                "guid",
                "index",
                "year",
                "score",
                "thumb",
                "matched",
                "parentName",
                "parentID",
                "parentGUID",
                "parentIndex",
            ]
        )

        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                if k not in allowed_attrs:
                    raise TypeError("Invalid attr for SearchResult: {}".format(k))
                setattr(self, k, v)
