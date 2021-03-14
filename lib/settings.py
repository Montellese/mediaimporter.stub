#!/usr/bin/python
# -*- coding: utf-8 -*-
#  Copyright (C) 2021 Sascha Montellese <montellese@kodi.tv>
#
#  SPDX-License-Identifier: GPL-2.0-or-later
#  See LICENSES/README.md for more information.
#

import xbmcaddon  # pylint: disable=import-error
import xbmcmediaimport  # pylint: disable=import-error


class ProviderSettings:
    @staticmethod
    def get_url(obj) -> str:
        provider_settings = ProviderSettings._get_provider_settings(obj)

        url = provider_settings.getString("stub.url")
        if not url:
            raise RuntimeError("invalid provider without URL")

        return url

    @staticmethod
    def set_url(obj, url: str):
        if not obj:
            raise ValueError("invalid media provider or media provider settings")
        if not url:
            raise ValueError("invalid url")

        provider_settings = ProviderSettings._get_provider_settings(obj)

        provider_settings.setString("stub.url", url)

    @staticmethod
    def _get_provider_settings(obj) -> xbmcaddon.Settings:
        if not obj:
            raise ValueError("invalid media provider or media provider settings")

        if isinstance(obj, xbmcmediaimport.MediaProvider):
            provider_settings = obj.getSettings()
            if not provider_settings:
                raise ValueError("invalid provider without settings")
            return provider_settings

        return obj
