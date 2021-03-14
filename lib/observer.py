#!/usr/bin/python
# -*- coding: utf-8 -*-
#  Copyright (C) 2021 Sascha Montellese <montellese@kodi.tv>
#
#  SPDX-License-Identifier: GPL-2.0-or-later
#  See LICENSES/README.md for more information.
#

import xbmcmediaimport  # pylint: disable=import-error

from lib.monitor import Monitor
from lib.provider_observer import ProviderObserver
from lib.utils import log, import2str


class ObserverService(xbmcmediaimport.Observer):
    def __init__(self):
        super(xbmcmediaimport.Observer, self).__init__()

        self._monitor = Monitor()
        self._observers = {}

        # TODO(stub): add additional members

        self._run()

    def _run(self):
        log("Observing stub media providers...")

        while not self._monitor.abortRequested():
            # process all observers
            for observer in self._observers.values():
                observer.Process()

            # TODO(stub): perform additional processing (e.g. player interaction / callbacks)

            if self._monitor.waitForAbort(1):
                break

        # stop all observers
        for observer in self._observers.values():
            observer.Stop()

    def _add_observer(self, media_provider: xbmcmediaimport.MediaProvider):
        if not media_provider:
            raise ValueError("cannot add invalid media provider")

        self._player.AddProvider(media_provider)

        # check if we already know about the media provider
        media_provider_id = media_provider.getIdentifier()
        if media_provider_id in self._observers:
            return

        # create the observer
        self._observers[media_provider_id] = ProviderObserver()

    def _remove_observer(self, media_provider: xbmcmediaimport.MediaProvider):
        if not media_provider:
            raise ValueError("cannot remove invalid media provider")

        self._player.RemoveProvider(media_provider)

        media_provider_id = media_provider.getIdentifier()
        if media_provider_id not in self._observers:
            return

        del self._observers[media_provider_id]

    def _start_observer(self, media_provider: xbmcmediaimport.MediaProvider):
        if not media_provider:
            raise ValueError("cannot start invalid media provider")

        # make sure the media provider has been added
        self._add_observer(media_provider)

        # start observing the media provider
        self._observers[media_provider.getIdentifier()].start(media_provider)

    def _stop_observer(self, media_provider: xbmcmediaimport.MediaProvider):
        if not media_provider:
            raise ValueError("cannot stop invalid media provider")

        media_provider_id = media_provider.getIdentifier()
        if media_provider_id not in self._observers:
            return

        self._observers[media_provider_id].stop()

    def _add_import(self, media_import: xbmcmediaimport.MediaImport):
        if not media_import:
            raise ValueError("cannot add invalid media import")

        media_provider = media_import.getProvider()
        if not media_provider:
            raise ValueError(f"cannot add media import {import2str(media_import)} with invalid media provider")

        media_provider_id = media_provider.getIdentifier()
        if media_provider_id not in self._observers:
            return

        self._observers[media_provider_id].add_import(media_import)

    def _remove_import(self, media_import: xbmcmediaimport.MediaImport):
        if not media_import:
            raise ValueError("cannot remove invalid media import")

        media_provider = media_import.getProvider()
        if not media_provider:
            raise ValueError(f"cannot remove media import {import2str(media_import)} with invalid media provider")

        media_provider_id = media_provider.getIdentifier()
        if media_provider_id not in self._observers:
            return

        self._observers[media_provider_id].remove_import(media_import)

    def onProviderAdded(self, media_provider: xbmcmediaimport.MediaProvider):
        self._add_observer(media_provider)

    def onProviderUpdated(self, media_provider: xbmcmediaimport.MediaProvider):
        self._add_observer(media_provider)

        # make sure the media provider is being observed
        if media_provider.isActive():
            self._start_observer(media_provider)
        else:
            self._stop_observer(media_provider)

    def onProviderRemoved(self, media_provider: xbmcmediaimport.MediaProvider):
        self._remove_observer(media_provider)

    def onProviderActivated(self, media_provider: xbmcmediaimport.MediaProvider):
        self._start_observer(media_provider)

    def onProviderDeactivated(self, media_provider: xbmcmediaimport.MediaProvider):
        self._stop_observer(media_provider)

    def onImportAdded(self, media_import: xbmcmediaimport.MediaImport):
        self._add_import(media_import)

    def onImportUpdated(self, media_import: xbmcmediaimport.MediaImport):
        self._add_import(media_import)

    def onImportRemoved(self, media_import: xbmcmediaimport.MediaImport):
        self._remove_import(media_import)
