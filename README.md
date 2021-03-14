# Stub Media Importer Add-on

This Kodi add-on is only a stub and cannot be executed as-is. It is meant as a starting point for developers interested in implementing a media importer add-on or integrating media importing into their existing add-on(s).

- [Stub Media Importer Add-on](#stub-media-importer-add-on)
  - [Add-on Hierarchy](#add-on-hierarchy)
  - [How To Start](#how-to-start)
    - [Steps](#steps)
    - [Additional Hints](#additional-hints)
      - [Stub Code](#stub-code)
      - [PEP8 Style Guide](#pep8-style-guide)
      - [Additional Kodi Add-on Extension Points](#additional-kodi-add-on-extension-points)

## Add-on Hierarchy

* `addon.xml`
  * change everything in the `<addon>` tag.
  * specify whether the media importer implementation supports manually looking for media providers using the `<canlookupprovider>` tag.
  * adjust everything belonging to `<extension point="xbmc.addon.metadata">`.
  * add any additional `<extension>` tags (e.g. for context menu integration).
* `discovery.py`, `importer.py` and `observer.py` are the three entry points into the media importer logic. They most likely don't need to be changed. `discovery.py` and `observer.py` are optional.
  * `importer.py` is the entry point for performing specific media import related tasks.
  * `discovery.py` (optional) is the entry point for running a service which automatically discovers potential media providers.
  * `observer.py` (optional) is the entry point for running a service which automatically observes configured media providers and imports for changes to the imported media items.
* `resources`
  * `providersettings.xml` contain the setting definitions for a media provider.
  * `importsettings.xml` contain the setting definitions for a media import.
* `lib`
  * `importer.py` contains the main logic for performing specific media import related tasks. It must handle a set of mandatory actions (e.g. `canimport`, `isproviderready` and `import`), can handle a set of optional actions (`discoverprovider` and `lookupprovider`) and can also handle additional custom setting callbacks and / or setting options fillers.
    * Use the various methods from the `xbmcmediaimport` module to interact with Kodi's media imort logic (e.g. `xbmcmediaimport.addImportItems()`).
  * `discovery.py` contains the service which automatically observes configured media providers and imports for changes to the imported media items.
    * Use `xbmcmediaimport.addAndActivateProvider()` and `xbmcmediaimport.deactivateProvider()` to manage detected media providers in Kodi.
  * `observer.py` contains the service which implements `xbmcmediaimport.Observer` and automatically observes configured media providers and imports for changes to the imported media items. `provider_observer.py` is a helper class to track changes of a specific media provider.
    * Use `xbmcmediaimport.changeImportedItems()` to pass changed media items to Kodi for processing.
  * `kodi.py` contains a set of helper functions to prepare `xbmcgui.ListItem` instances for the imported media items which are then passed to Kodi's media import logic.
  * `settings.py` contains a helper class `ProviderSettings` to simplify interacting with media provider related settings stored in a `xbmcaddon.Settings` instance.
  * `utils.py` contains a set of helper methods to use localized strings and for logging.

## How To Start

### Steps

The following steps should be taken when developping a custom media importer add-on based on this stub:
1. modify `addon.xml`
2. implement a way to add new media providers to Kodi either using `lib/discovery.py` or by implementing the `discoverprovider` and `lookupprovider` actions in `lib/importer.py`. If there will only ever be one media provider supported by the add-on just use `xbmcmediaimport.addAndActivateProvider()` in `discovery.py` to create the media provider.
3. implement the mandatory actions in `lib/importer.py`

### Additional Hints

#### Stub Code

In general all places in the code which need to be changed are marked with either `TODO(stub)` or just `stub`. But since this is a minimal stub it is very likely that other places need to be changed as well.

#### PEP8 Style Guide

The code follows the style guides from PEP8. Any method names not following PEP8 are part of Kodi's python interface. This applies to both functions and methods in `xbmcmediaimport` and to callbacks (e.g. in `xbmcmediaimport.Observer`).

#### Additional Kodi Add-on Extension Points

It is possible to combine the media importer logic with other features available to Kodi add-ons like
* providing context menu integration for imported media items
* supporting playback related features like playback progress reporting
* using `plugin://` based playback URLs for imported media items
* browsing media items which can be imported
