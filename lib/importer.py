#!/usr/bin/python
# -*- coding: utf-8 -*-
#  Copyright (C) 2021 Sascha Montellese <montellese@kodi.tv>
#
#  SPDX-License-Identifier: GPL-2.0-or-later
#  See LICENSES/README.md for more information.
#

import sys
from typing import Dict, List

from six.moves.urllib.parse import parse_qs, unquote, urlparse

import xbmc  # pylint: disable=import-error
import xbmcmediaimport  # pylint: disable=import-error

from lib.kodi import Api  # noqa F401
from lib.utils import localize, log, provider2str


def media_types_from_options(options: Dict) -> List[str]:
    if "mediatypes" not in options and "mediatypes[]" not in options:
        return None

    media_types = None
    if "mediatypes" in options:
        media_types = options["mediatypes"]
    elif "mediatypes[]" in options:
        media_types = options["mediatypes[]"]

    return media_types


def test_authentication(handle, _):
    # retrieve the media provider
    media_provider = xbmcmediaimport.getProvider(handle)
    if not media_provider:
        log("cannot retrieve media provider", xbmc.LOGERROR)
        return

    log(f"testing authentication with {provider2str(media_provider)}...")

    # TODO(stub): check if authentication with the media provider works
    #             feel free to use a dialog to report success / failure


def force_sync(handle, _):
    # TODO(stub): provide custom action setting handlers / callbacks

    pass


def setting_options_filler_views(handle, _):
    # retrieve the media provider
    media_provider = xbmcmediaimport.getProvider(handle)
    if not media_provider:
        log("cannot retrieve media provider", xbmc.LOGERROR)
        return

    # retrieve the media import
    media_import = xbmcmediaimport.getImport(handle)
    if not media_import:
        log("cannot retrieve media import", xbmc.LOGERROR)
        return

    # prepare the media provider settings
    if not media_provider.prepareSettings():
        log("cannot prepare media provider settings", xbmc.LOGERROR)
        return

    # TODO(stub): collect information and provide it as a list of options to the user
    #             each option is a tuple(label, key)
    options = [("Foo", "foo"), ("Bar", "bar")]

    # get the import"s settings
    settings = media_import.getSettings()

    # pass the list of views back to Kodi
    settings.setStringOptions("stub.importviews", options)


def discover_provider(handle, options):
    # TODO(stub): help the user finding a media provider
    #             feel free to use input dialogs etc. to guide the user in the process

    # TODO(stub): put together a xbmcmediaimport.MediaProvider
    provider = None  # TODO(stub): xbmcmediaimport.MediaProvider(...)

    xbmcmediaimport.setDiscoveredProvider(handle, True, provider)


def lookup_provider(handle, _):
    # retrieve the media provider
    media_provider = xbmcmediaimport.getProvider(handle)
    if not media_provider:
        log("cannot retrieve media provider", xbmc.LOGERROR)
        return

    settings = media_provider.prepareSettings()
    if not settings:
        log("cannot prepare media provider settings", xbmc.LOGERROR)
        return

    # TODO(stub): check if the media provider is active

    xbmcmediaimport.setProviderFound(handle, True)


def can_import(handle, options):
    if "path" not in options:
        log('cannot execute "canimport" without path')
        return

    path = unquote(options["path"][0])  # noqa F841 # pylint: disable=unused-variable

    # TODO(stub): check if the given path can be imported

    xbmcmediaimport.setCanImport(handle, True)


def is_provider_ready(handle, _):
    # retrieve the media provider
    media_provider = xbmcmediaimport.getProvider(handle)
    if not media_provider:
        log("cannot retrieve media provider", xbmc.LOGERROR)
        return

    # prepare the media provider settings
    if not media_provider.prepareSettings():
        log("cannot prepare media provider settings", xbmc.LOGERROR)
        return

    # TODO(stub): check if the configuration of the media provider is valid / complete

    xbmcmediaimport.setProviderReady(handle, True)


def is_import_ready(handle, _):
    # retrieve the media import
    media_import = xbmcmediaimport.getImport(handle)
    if not media_import:
        log("cannot retrieve media import", xbmc.LOGERROR)
        return
    # prepare and get the media import settings
    import_settings = media_import.prepareSettings()
    if not import_settings:
        log("cannot prepare media import settings", xbmc.LOGERROR)
        return

    # retrieve the media provider
    media_provider = xbmcmediaimport.getProvider(handle)
    if not media_provider:
        log("cannot retrieve media provider", xbmc.LOGERROR)
        return

    # prepare the media provider settings
    if not media_provider.prepareSettings():
        log("cannot prepare media provider settings", xbmc.LOGERROR)
        return

    # TODO(stub): check if the configuration of the media import is valid / complete

    xbmcmediaimport.setImportReady(handle, True)


def load_provider_settings(handle, _):
    # retrieve the media provider
    media_provider = xbmcmediaimport.getProvider(handle)
    if not media_provider:
        log("cannot retrieve media provider", xbmc.LOGERROR)
        return

    settings = media_provider.getSettings()
    if not settings:
        log("cannot retrieve media provider settings", xbmc.LOGERROR)
        return

    # TODO(stub): register action callbacks
    settings.registerActionCallback("stub.testauthentication", "testauthentication")

    # TODO(stub): register setting options fillers

    settings.setLoaded()


def load_import_settings(handle, _):
    # retrieve the media import
    media_import = xbmcmediaimport.getImport(handle)
    if not media_import:
        log("cannot retrieve media import", xbmc.LOGERROR)
        return

    settings = media_import.getSettings()
    if not settings:
        log("cannot retrieve media import settings", xbmc.LOGERROR)
        return

    # TODO(stub): register action callbacks
    settings.registerActionCallback("stub.forcesync", "forcesync")

    # TODO(stub): register a setting options fillers
    settings.registerOptionsFillerCallback(
        "stub.importviews", "settingoptionsfillerviews"
    )

    settings.setLoaded()


def can_update_metadata_on_provider(handle, options):  # pylint: disable=unused-argument
    # TODO(stub): specify whether updating metadata on the media provider is supported
    xbmcmediaimport.setCanUpdateMetadataOnProvider(True)


def can_update_playcount_on_provider(
    handle, options
):  # pylint: disable=unused-argument
    # TODO(stub): specify whether updating the playcount on the media provider is supported
    xbmcmediaimport.setCanUpdatePlaycountOnProvider(True)


def can_update_last_played_on_provider(
    handle, options
):  # pylint: disable=unused-argument
    # TODO(stub): specify whether updating last played on the media provider is supported
    xbmcmediaimport.setCanUpdateLastPlayedOnProvider(True)


def can_update_resume_position_on_provider(
    handle, options
):  # pylint: disable=unused-argument
    # TODO(stub): specify whether updating the resume point on the media provider is supported
    xbmcmediaimport.setCanUpdateResumePositionOnProvider(True)


# noqa pylint: disable=too-many-locals, too-many-statements, too-many-nested-blocks, too-many-branches, too-many-return-statements
def exec_import(handle, options):
    # parse all necessary options
    media_types = media_types_from_options(options)
    if not media_types:
        log('cannot execute "import" without media types', xbmc.LOGERROR)
        return

    # retrieve the media import
    media_import = xbmcmediaimport.getImport(handle)
    if not media_import:
        log("cannot retrieve media import", xbmc.LOGERROR)
        return

    # prepare and get the media import settings
    import_settings = media_import.prepareSettings()
    if not import_settings:
        log("cannot prepare media import settings", xbmc.LOGERROR)
        return

    # retrieve the media provider
    media_provider = media_import.getProvider()
    if not media_provider:
        log("cannot retrieve media provider", xbmc.LOGERROR)
        return

    log(f"importing {media_types} items from { provider2str(media_provider)}...")

    # TODO(stub): prepare collecting ListItems

    # loop over all media types to be imported
    progress = 0
    progress_total = len(media_types)
    for media_type in media_types:
        # check if we need to cancel importing items
        if xbmcmediaimport.shouldCancel(handle, progress, progress_total):
            return
        progress += 1

        log(f"importing {media_type} items from {provider2str(media_provider)}...")

        # report the progress status
        xbmcmediaimport.setProgressStatus(handle, localize(32001).format(media_type))

        items = []

        # TODO(stub): collect ListItems to import
        #             adjust and use lib.kodi.Api.to_file_item()

        if items:
            # pass the imported items back to Kodi
            log(
                f"{len(items)} {media_type} items imported from {provider2str(media_provider)}"
            )

            # TODO(stub): for partial imports use the following constants as an optional fourth argument:
            #     xbmcmediaimport.MediaImportChangesetTypeNone: let Kodi decide
            #     xbmcmediaimport.MediaImportChangesetTypeAdded: the item is new and should be added
            #     xbmcmediaimport.MediaImportChangesetTypeChanged: the item has been imported before and has changed
            #     xbmcmediaimport.MediaImportChangesetTypeRemoved: the item has to be removed
            xbmcmediaimport.addImportItems(handle, items, media_type)

    # TODO(stub): tell Kodi whether the provided items is a full or partial import
    partial_import = False

    # finish the import
    xbmcmediaimport.finishImport(handle, partial_import)


# pylint: disable=too-many-return-statements
def update_on_provider(handle, _):
    # retrieve the media import
    media_import = xbmcmediaimport.getImport(handle)
    if not media_import:
        log("cannot retrieve media import", xbmc.LOGERROR)
        return

    # retrieve the media provider
    media_provider = media_import.getProvider()
    if not media_provider:
        log("cannot retrieve media provider", xbmc.LOGERROR)
        return

    # prepare and get the media import settings
    import_settings = media_import.prepareSettings()
    if not import_settings:
        log("cannot prepare media import settings", xbmc.LOGERROR)
        return

    # prepare the media provider settings
    if not media_provider.prepareSettings():
        log("cannot prepare media provider settings", xbmc.LOGERROR)
        return

    # get the updated item
    item = xbmcmediaimport.getUpdatedItem(handle)
    if not item:
        log("cannot retrieve updated item", xbmc.LOGERROR)
        return

    log(
        f'updating "{item.getLabel()}" ({item.getPath()}) on {provider2str(media_provider)}...'
    )

    video_info_tag = item.getVideoInfoTag()
    if not video_info_tag:
        log("updated item is not a video item", xbmc.LOGERROR)
        return

    # TODO(stub): update playback related metadata (playcount, last played, resume point)

    xbmcmediaimport.finishUpdate_on_provider(handle)


ACTIONS = {
    # official media import callbacks
    # mandatory
    "canimport": can_import,
    "isproviderready": is_provider_ready,
    "isimportready": is_import_ready,
    "loadprovidersettings": load_provider_settings,
    "loadimportsettings": load_import_settings,
    "canupdatemetadataonprovider": can_update_metadata_on_provider,
    "canupdateplaycountonprovider": can_update_playcount_on_provider,
    "canupdatelastplayedonprovider": can_update_last_played_on_provider,
    "canupdateresumepositiononprovider": can_update_resume_position_on_provider,
    "import": exec_import,
    "updateonprovider": update_on_provider,
    # optional depending on <canlookupprovider> from addon.xml
    "discoverprovider": discover_provider,
    "lookupprovider": lookup_provider,
    # custom setting callbacks
    "testauthentication": test_authentication,
    "forcesync": force_sync,
    # custom setting options fillers
    "settingoptionsfillerviews": setting_options_filler_views,
}


def run(argv):
    path = argv[0]
    handle = int(argv[1])

    options = None
    if len(argv) > 2:
        # get the options but remove the leading ?
        params = argv[2][1:]
        if params:
            options = parse_qs(params)

    log(f"path = {path}, handle = {handle}, options = {params}", xbmc.LOGDEBUG)

    url = urlparse(path)
    action = url.path
    if action[0] == "/":
        action = action[1:]

    if action not in ACTIONS:
        log(f"cannot process unknown action: {action}", xbmc.LOGERROR)
        sys.exit(0)

    action_method = ACTIONS[action]
    if not action_method:
        log(f"action not implemented: {action}", xbmc.LOGWARNING)
        sys.exit(0)

    log(f'executing action "{action}"...', xbmc.LOGDEBUG)
    action_method(handle, options)
