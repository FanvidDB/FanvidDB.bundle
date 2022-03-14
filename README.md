# FanvidDB.bundle

## Installation (Mac)

_Installation requires Plex Media Server._

1. Clone this repository anywhere on your computer.
2. Build the plugin and symlink it from your Plex Media Server plugin directory:
   ```bash
   # Run this command from your FanvidDB.bundle directory.
   make build
   ln -s "$PWD/build/" "$HOME/Library/Application Support/Plex Media Server/Plug-ins/FanvidDB.bundle"
   ```
3. Restart your Plex server.

## Why build the plugin instead of just developing the code directly?

Plex uses Python 2.7. Plugins can have the following structure:

```
-Contents
 |-Code
 | |-# python code lives here
 |-Libraries
 | |-Shared
 | | |-# additional python dependencies for the plugin can live here.
 |-DefaultPrefs.json
 |-Info.plist
```

It also runs a special embedded version of python that has some unusual properties, like additional superglobal variables (which are defined in the Framework.bundle that is included in the base Plex Media Server installation).

Treating the final plugin as a built artifact allows developers to use modern python development practices, and the build process can take any necessary steps to ensure that the resulting code will also run inside Plex.

## Testing

### Setup

1. Set up pyenv and install python 2.7.18 (to match Plex's internal version) and python 3.5+ (for additional dependencies)
2. Set up a python 2.7 virtualenv and install requirements.txt
3. Run `pip3 install mypy black`. (They require python 3 to run, but can run on python 2 code.) 

### Running

```
make lint
pytest
```

## Troubleshooting (Mac)

Assuming you are developing on a machine that is also running plex media server, you can find the latest [logs](https://support.plex.tv/articles/200250417-plex-media-server-log-files/) at `~/Library/Logs/Plex Media Server/PMS Plugin Logs/com.fanviddb.agents.fanvids.log`

