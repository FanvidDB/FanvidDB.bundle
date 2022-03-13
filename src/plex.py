# Plex provides a number of "superglobal" variables that are available
# directly within the global namespace without needing to be explicitly
# imported. This file provides some shims so that we can run tests and
# then strip out the imports during the build process.
from typing import Dict

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
        def Info(message):
            pass


try:
    Prefs = Prefs
except NameError:
    Prefs = {}  # type: Dict[str, str]

try:
    MetadataSearchResult = MetadataSearchResult
except NameError:

    class MetadataSearchResult:
        def __init__(self, id, name, year, lang, score):
            pass
