#!/usr/bin/python
# -*- coding: utf-8 -*-
#  Copyright (C) 2021 Sascha Montellese <montellese@kodi.tv>
#
#  SPDX-License-Identifier: GPL-2.0-or-later
#  See LICENSES/README.md for more information.
#

from six import PY3
import unicodedata

import xbmc  # pylint: disable=import-error
import xbmcaddon  # pylint: disable=import-error
import xbmcmediaimport  # pylint: disable=import-error

__addon__ = xbmcaddon.Addon()
__addonid__ = __addon__.getAddonInfo("id")


def log(message: str, level: int = xbmc.LOGINFO):
    if not PY3:
        try:
            message = message.encode("utf-8")
        except UnicodeDecodeError:
            message = message.decode("utf-8").encode("utf-8", "ignore")
    xbmc.log(f"[{__addonid__}] {message}", level)


# fixes unicode problems
def string2unicode(text, encoding="utf-8") -> str:
    try:
        if PY3:
            text = str(text)
        else:
            text = unicode(text, encoding)  # noqa: F821
    except:  # noqa: E722  # nosec
        pass

    return text


def normalize_string(text: str) -> str:
    try:
        text = unicodedata.normalize("NFKD", string2unicode(text)).encode("ascii", "ignore")  # noqa: F821
    except:  # noqa: E722  # nosec
        pass

    return text


def localize(identifier: int) -> str:
    return normalize_string(__addon__.getLocalizedString(identifier))


def provider2str(media_provider: xbmcmediaimport.MediaProvider) -> str:
    if not media_provider:
        return "unknown media provider"

    return f'"{media_provider.getFriendlyName()}" ({media_provider.getIdentifier()})'


def import2str(media_import: xbmcmediaimport.MediaImport) -> str:
    if not media_import:
        return "unknown media import"

    return f"{provider2str(media_import.getProvider())} {media_import.getMediaTypes()}"


try:
    from datetime import timezone

    utc = timezone.utc
except ImportError:
    from datetime import timedelta, tzinfo

    class UTC(tzinfo):
        """UTC"""

        ZERO = timedelta(0)

        def utcoffset(self, dt):
            return UTC.ZERO

        def tzname(self, dt):
            return "UTC"

        def dst(self, dt):
            return UTC.ZERO

    utc = UTC()
