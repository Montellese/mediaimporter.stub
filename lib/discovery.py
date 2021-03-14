#!/usr/bin/python
# -*- coding: utf-8 -*-/*
#  Copyright (C) 2021 Sascha Montellese <montellese@kodi.tv>
#
#  SPDX-License-Identifier: GPL-2.0-or-later
#  See LICENSES/README.md for more information.
#

import time
from six import iteritems

import xbmc  # pylint: disable=import-error
import xbmcmediaimport  # pylint: disable=import-error

from lib.monitor import Monitor
from lib.utils import log


class DiscoveryService:
    class Server:
        def __init__(self):
            self.id = ""
            self.name = ""
            self.address = ""
            self.registered = False
            self.last_seen = None

        def is_expired(self, timeout_s: int):
            return self.registered and self.last_seen + timeout_s < time.time()

    def __init__(self):
        self._monitor = Monitor()
        self._servers = {}

        # TODO(stub): add additional members

        self._start()

    def _discover(self):
        server = None

        # TODO(stub): execute discovery

        if server:
            self._add_server(server)

    def _add_server(self, server: DiscoveryService.Server):  # noqa F821
        register_server = False

        # check if the server is already known
        if server.id not in self._servers:
            self._servers[server.id] = server
            register_server = True
        else:
            # check if the server has already been registered or if some of its properties have changed
            if (
                not self._servers[server.id].registered
                or self._servers[server.id].name != server.name
                or self._servers[server.id].address != server.address
            ):
                self._servers[server.id] = server
                register_server = True
            else:
                # simply update the server"s last seen property
                self._servers[server.id].last_seen = server.last_seen

        # if the server doesn"t need to be registered there"s nothing else to do
        if not register_server:
            return

        # TODO(stub): create / determine a unique media provider identifier
        provider_id = "stub"
        # TODO(stub): determine the path to an icon for the media provider
        provider_icon_url = "stub-icon.png"
        # TODO(stub): specify which media types can be imported from the media provider
        supported_media_types = set(
            [
                xbmcmediaimport.MediaTypeMovie,
                xbmcmediaimport.MediaTypeVideoCollection,
                xbmcmediaimport.MediaTypeMusicVideo,
                xbmcmediaimport.MediaTypeTvShow,
                xbmcmediaimport.MediaTypeSeason,
                xbmcmediaimport.MediaTypeEpisode,
            ]
        )

        # create the media provider
        media_provider = xbmcmediaimport.MediaProvider(
            provider_id, server.name, provider_icon_url, supported_media_types
        )

        # prepare / get the settings of the media provider
        settings = media_provider.prepareSettings()
        if not settings:
            log("cannot prepare media provider settings", xbmc.LOGERROR)
            return

        # TODO(stub): store the URL to the media provider in the settings
        settings.setString("stub.url", server.address)

        # add the media provider and activate it
        if xbmcmediaimport.addAndActivateProvider(media_provider):
            self._servers[server.id].registered = True
            log(
                f'stub server "{server.name}" ({server.id}) successfully added and activated'
            )
        else:
            self._servers[server.id].registered = False
            log(
                f'failed to add and/or activate stub server "{server.name}" ({server.id})'
            )

    def _expire_servers(self):
        for server_id, server in iteritems(self._servers):
            # expire the server after 10 seconds
            if not server.is_expired(10):
                continue

            server.registered = False
            xbmcmediaimport.deactivateProvider(server_id)
            log(
                f'stub server "{server.name}" ({server.id}) deactivated due to inactivity'
            )

    def _start(self):
        log("Looking for stub servers...")

        # TODO(stub): setup discovery

        while not self._monitor.abortRequested():
            # try to discover servers
            self._discover()

            # expire servers that haven"t responded for a while
            self._expire_servers()

            if self._monitor.waitForAbort(1):
                break

        # TODO(stub): cleanup discovery
