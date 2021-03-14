#!/usr/bin/python
# -*- coding: utf-8 -*-
#  Copyright (C) 2017-2019 Sascha Montellese <montellese@kodi.tv>
#
#  SPDX-License-Identifier: GPL-2.0-or-later
#  See LICENSES/README.md for more information.
#

from typing import List, Tuple

import xbmc  # pylint: disable=import-error
import xbmcgui  # pylint: disable=import-error
import xbmcmediaimport  # pylint: disable=import-error

from lib.utils import log, import2str, provider2str


class ProviderObserver:
    class Action:
        START = 0
        STOP = 1

    def __init__(self):
        # default values
        self._actions = []
        self._connected = False
        self._imports = []
        self._media_provider = None
        self._settings = None

    def __del__(self):
        self._stop_action()

    def add_import(self, media_import: xbmcmediaimport.MediaImport):
        if not media_import:
            raise ValueError("invalid media_import")

        # look for a matching import
        matching_import_indices = self._find_import_indices(media_import)
        # if a matching import has been found update it
        if matching_import_indices:
            self._imports[matching_import_indices[0]] = media_import
            ProviderObserver.log(
                f"media import {import2str(media_import)} from {provider2str(self._media_provider)} updated"
            )
        else:
            # otherwise add the import to the list
            self._imports.append(media_import)
            ProviderObserver.log(
                f"media import {import2str(media_import)} from {provider2str(self._media_provider)} added"
            )

    def remove_import(self, media_import: xbmcmediaimport.MediaImport):
        if not media_import:
            raise ValueError("invalid media_import")

        # look for a matching import
        matching_import_indices = self._find_import_indices(media_import)
        if not matching_import_indices:
            return

        # remove the media import from the list
        del self._imports[matching_import_indices[0]]
        ProviderObserver.log(
            f"media import {import2str(media_import)} from {provider2str(self._media_provider)} removed"
        )

    def start(self, media_provider: xbmcmediaimport.MediaProvider):
        if not media_provider:
            raise ValueError("invalid media_provider")

        self._actions.append((ProviderObserver.Action.START, media_provider))

    def stop(self):
        self._actions.append((ProviderObserver.Action.STOP, None))

    def process(self):
        # process any open actions
        self._process_actions()

        # TODO(stub): perform additional processing
        # TODO(stub): call self._change_items(items) to pass changed items to Kodi

    def _find_import_indices(self, media_import: xbmcmediaimport.MediaImport) -> List[int]:
        if not media_import:
            raise ValueError("invalid media_import")

        return [
            i
            for i, localImport in enumerate(self._imports)
            if localImport.getProvider().getIdentifier() == media_import.getProvider().getIdentifier()
            and localImport.getMediaTypes() == media_import.getMediaTypes()
        ]

    def _process_actions(self):
        for (action, data) in self._actions:
            if action == ProviderObserver.Action.START:
                self._start_action(data)
            elif action == ProviderObserver.Action.STOP:
                self._stop_action()
            else:
                ProviderObserver.log(f"unknown action {action} to process", xbmc.LOGWARNING)

        self._actions = []

    def _change_items(self, items: Tuple[int, xbmcgui.ListItem, str]):
        # map the changed items to their media import
        changed_items_map = {}
        for (changeset_type, item, item_id) in items:
            if not item:
                continue

            # find a matching import for the changed item
            media_import = self._find_import_for_item(item)
            if not media_import:
                ProviderObserver.log(
                    (
                        f'failed to determine media import for changed item with id "{item_id}" '
                        f"from {provider2str(self._media_provider)}"
                    ),
                    xbmc.LOGWARNING,
                )
                continue

            if media_import not in changed_items_map:
                changed_items_map[media_import] = []

            changed_items_map[media_import].append((changeset_type, item))

        # finally pass the changed items grouped by their media import to Kodi
        for (media_import, changedItems) in changed_items_map.items():
            if xbmcmediaimport.changeImportedItems(media_import, changedItems):
                ProviderObserver.log(
                    (
                        f"changed {len(changedItems)} imported items for media import {import2str(media_import)} "
                        f"from {provider2str(self._media_provider)}"
                    )
                )
            else:
                ProviderObserver.log(
                    (
                        f"failed to change {len(changedItems)} imported items for media import "
                        f"{import2str(media_import)} from {provider2str(self._media_provider)}"
                    ),
                    xbmc.LOGWARNING,
                )

    def _find_import_for_item(self, item: xbmcgui.ListItem) -> xbmcmediaimport.MediaImport:
        video_info_tag = item.getVideoInfoTag()
        if not video_info_tag:
            return None

        item_media_type = video_info_tag.getMediaType()

        matching_imports = [
            media_import for media_import in self._imports if item_media_type in media_import.getMediaTypes()
        ]
        if not matching_imports:
            return None

        return matching_imports[0]

    def _start_action(self, media_provider: xbmcmediaimport.MediaProvider):
        if not media_provider:
            raise RuntimeError("invalid media_provider")

        if self._connected:
            # TODO(stub): abort early if the observer is already running
            return True

        # make sure the observer is stopped but indicate that it is being restarted
        self._stop_action(restart=True)

        # initialize members
        self._media_provider = media_provider
        self._settings = self._media_provider.prepareSettings()
        if not self._settings:
            raise RuntimeError("cannot prepare media provider settings")

        # TODO(stub): start observing the media provider

        ProviderObserver.log(
            f"successfully connected to {provider2str(self._media_provider)} to observe media imports"
        )
        self.connected = True
        return True

    def _stop_action(self, restart: bool = False):
        if not self._connected:
            return

        if not restart:
            ProviderObserver.log(f"stopped observing media imports from {provider2str(self._media_provider)}")

        # TODO(stub): stop observing the media provider

        self._reset()

    def _reset(self):
        # TODO(stub): reset internal members

        self._connected = False
        self._media_provider = None

    @staticmethod
    def log(message: str, level: int = xbmc.LOGINFO):
        log(f"[observer] {message}", level)
