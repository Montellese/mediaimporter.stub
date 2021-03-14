#!/usr/bin/python
# -*- coding: utf-8 -*-
#  Copyright (C) 2021 Sascha Montellese <montellese@kodi.tv>
#
#  SPDX-License-Identifier: GPL-2.0-or-later
#  See LICENSES/README.md for more information.
#

import json
from typing import Dict, List

from dateutil import parser
from six.moves.urllib.parse import urlparse, urlunparse

import xbmc  # pylint: disable=import-error
from xbmcgui import InfoTagVideo, ListItem  # pylint: disable=import-error
import xbmcmediaimport  # pylint: disable=import-error


class Api:
    @staticmethod
    def convert_datetime2db_datetime(datetime_str: str) -> str:
        if not datetime_str:
            return ""

        datetime = parser.parse(datetime_str)
        try:
            return datetime.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            return ""

    @staticmethod
    def get_id_from_item(local_item: ListItem) -> str:
        if not local_item:
            raise ValueError("invalid localItem")

        video_info_tag = local_item.getVideoInfoTag()
        if not video_info_tag:
            return None

        return Api.get_id_from_video_info_tag(video_info_tag)

    @staticmethod
    # pylint: disable=too-many-return-statements
    def get_id_from_video_info_tag(video_info_tag: InfoTagVideo) -> str:
        UNIQUE_ID = "stub"

        if not video_info_tag:
            raise ValueError("invalid videoInfoTag")

        # TODO(stub): try to get the specific identifier
        item_id = video_info_tag.getUniqueID(UNIQUE_ID)
        if item_id:
            return item_id

        # try to get the database Identifier
        db_id = video_info_tag.getDbId()
        if not db_id:
            return None

        media_type = video_info_tag.getMediaType()
        if media_type == xbmcmediaimport.MediaTypeMovie:
            method = "Movie"
        elif media_type == xbmcmediaimport.MediaTypeTvShow:
            method = "TVShow"
        elif media_type == xbmcmediaimport.MediaTypeEpisode:
            method = "Episode"
        elif media_type == xbmcmediaimport.MediaTypeMusicVideo:
            method = "MusicVideo"
        else:
            return None

        # use JSON-RPC to retrieve all unique IDs
        json_response = json.loads(
            xbmc.executeJSONRPC(
                json.dumps(
                    {
                        "jsonrpc": "2.0",
                        "method": f"VideoLibrary.Get{method}Details",
                        "params": {
                            f"{media_type}id": db_id,
                            "properties": ["uniqueid"],
                        },
                        "id": 0,
                    }
                )
            )
        )
        if not json_response or "result" not in json_response:
            return None

        json_result = json_response["result"]
        details_key = f"{media_type}details"
        if details_key not in json_result:
            return None

        json_details = json_result[details_key]
        if "uniqueid" not in json_details:
            return None

        json_unique_ids = json_details["uniqueid"]
        if UNIQUE_ID not in json_unique_ids:
            return None

        return json_unique_ids[UNIQUE_ID]

    @staticmethod
    def match_imported_item_ids_to_local_items(local_items: List[ListItem], *imported_item_id_lists):
        matched_item_lists = []
        item_ids_to_process_lists = []
        for imported_item_ids in imported_item_id_lists:
            matched_item_lists.append([])
            item_ids_to_process_lists.append(imported_item_ids.copy())

        for local_item in local_items:
            # abort if there are no more items to process
            if all(len(item_ids_to_process) == 0 for item_ids_to_process in item_ids_to_process_lists):
                break

            # retrieve the local item"s ID
            local_item_id = Api.get_id_from_item(local_item)
            if not local_item_id:
                continue

            # check if it matches one of the imported item IDs
            for index, imported_item_ids in enumerate(imported_item_id_lists):
                if local_item_id not in item_ids_to_process_lists[index]:
                    continue

                matched_item_lists[index].append(local_item)
                item_ids_to_process_lists[index].remove(local_item_id)

        return tuple(matched_item_lists)

    @staticmethod
    # pylint: disable=too-many-arguments
    def to_file_item(item_obj: Dict, media_type: str = "", allow_direct_play: bool = True) -> ListItem:
        # TODO(stub): check if the media type is supported

        # TODO(stub): parse the item's title / label
        label = None

        # determine the item's playback URL
        item_path = "TODO(stub)"
        if not item_path:
            return None

        item = ListItem(path=item_path, label=label, offscreen=True)

        # TODO(stub): specify whether the item is a folder or not
        #             item.setIsFolder(item_obj.get(constants.PROPERTY_ITEM_IS_FOLDER))

        # TODO(stub): set the item's datetime
        #             item.setDateTime(premiereDate)

        # fill video details
        Api.fill_video_infos(item_obj, media_type, item, allow_direct_play=allow_direct_play)

        # TODO(stub): handle artwork as a dict
        artwork = None
        if artwork:
            item.setArt(artwork)

        return item

    @staticmethod
    def fill_video_infos(item_obj: Dict, media_type: str, item: ListItem, allow_direct_play: bool = True):
        info = {
            "mediatype": media_type,
            "path": "TODO(stub)",
            "filenameandpath": item.getPath(),
            "title": item.getLabel() or "",
            "sorttitle": "TODO(stub)",
            "originaltitle": "TODO(stub)",
            "plot": Api._map_overview("TODO(stub)"),
            "plotoutline": "TODO(stub)",
            "dateadded": Api.convert_datetime2db_datetime("2021-03-14 14:08:00"),  # TODO(stub)
            "year": 2021,  # TODO(stub)
            "rating": 0.0,  # TODO(stub)
            "mpaa": "TODO(stub)",
            "duration": 0,  # TODO(stub)
            "playcount": 0,  # TODO(stub)
            "lastplayed": Api.convert_datetime2db_datetime("2021-03-14 14:08:00"),  # TODO(stub)
            "director": ["TODO(stub)"],
            "writer": ["TODO(stub)"],
            "artist": ["TODO(stub)"],
            "album": "TODO(stub)",
            "genre": ["TODO(stub)"],
            "country": ["TODO(stub)"],
            "studio": ["TODO(stub)"],
            "tag": ["TODO(stub)"],
            "trailer": "TODO(stub)",
            "tagline": "TODO(stub)",
        }

        # handle aired / premiered
        date = item.getDateTime()
        if date:
            pos = date.find("T")
            if pos >= 0:
                date = date[:pos]

            if media_type == xbmcmediaimport.MediaTypeEpisode:
                info["aired"] = date
            else:
                info["premiered"] = date

        # handle tvshow, season and episode specific properties
        if media_type == xbmcmediaimport.MediaTypeTvShow:
            info["tvshowtitle"] = item.getLabel()
            info["status"] = "TODO(stub)"
        elif media_type in (
            xbmcmediaimport.MediaTypeSeason,
            xbmcmediaimport.MediaTypeEpisode,
        ):
            info["tvshowtitle"] = "TODO(stub)"
            index = 0  # TODO(stub)
            if media_type == xbmcmediaimport.MediaTypeSeason:
                info["season"] = index

                # ATTENTION
                # something is wrong with the SortName property for seasons which interfers with Kodi
                # abusing sorttitle for custom season titles
                del info["sorttitle"]
            else:
                info["season"] = 0  # TODO(stub)
                info["episode"] = index

        # handle actors / cast
        cast = []
        for index, _ in enumerate("TODO(stub)"):  # TODO(stub)
            cast.append(
                {
                    "name": "TODO(stub)",
                    "role": "TODO(stub)",
                    "order": index,
                    "thumbnail": "TODO(stub)",
                }
            )

        # store the collected information in the ListItem
        item.setInfo("video", info)
        item.setCast(cast)

        # handle unique / provider IDs
        unique_ids = {"TODO(stub)": "TODO(stub)"}
        default_unique_id = Api._map_default_unique_id(unique_ids, media_type)
        # add the item"s ID as a unique ID
        unique_ids["TODO(stub)"] = "TODO(stub)"
        item.getVideoInfoTag().setUniqueIDs(unique_ids, default_unique_id)

        # handle resume point
        item.setProperties(
            {
                "totaltime": info["duration"],
                "resumetime": 0,  # TODO(stub)
            }
        )

        # stream details
        for _ in ["TODO(stub)"]:
            stream_type = "TODO(stub)"
            if stream_type == "Video":
                item.addStreamInfo(
                    "video",
                    {
                        "codec": "TODO(stub)",
                        "profile": "TODO(stub)",
                        "language": "TODO(stub)",
                        "width": 0,  # TODO(stub)
                        "height": 0,  # TODO(stub)
                        "aspect": "TODO(stub)",
                        "stereomode": "TODO(stub)",
                        "duration": info["duration"],
                    },
                )
            elif stream_type == "Audio":
                item.addStreamInfo(
                    "audio",
                    {
                        "codec": "TODO(stub)",
                        "profile": "TODO(stub)",
                        "language": "TODO(stub)",
                        "channels": 2,  # TODO(stub)
                    },
                )
            elif stream_type == "Subtitle":
                item.addStreamInfo(
                    "subtitle",
                    {
                        "language": "TODO(stub)",
                    },
                )

    @staticmethod
    def _map_path(path: str, container: str = None) -> str:
        if not path:
            return ""

        # turn UNC paths into Kodi-specific Samba paths
        if path.startswith("\\\\"):
            path = path.replace("\\\\", "smb://", 1).replace("\\\\", "\\").replace("\\", "/")

        # for DVDs and Blue-Ray try to directly access the main playback item
        if container == "dvd":
            path = f"{path}/VIDEO_TS/VIDEO_TS.IFO"
        elif container == "bluray":
            path = f"{path}/BDMV/index.bdmv"

        # get rid of any double backslashes
        path = path.replace("\\\\", "\\")

        # make sure paths are consistent
        if "\\" in path:
            path.replace("/", "\\")

        # Kodi expects protocols in lower case
        path_parts = urlparse(path)
        if path_parts.scheme:
            path = urlunparse(path_parts._replace(scheme=path_parts.scheme.lower()))

        return path

    @staticmethod
    def _map_overview(overview: str) -> str:
        if not overview:
            return ""

        return overview.replace("\n", "[CR]").replace("\r", "").replace("<br>", "[CR]")

    UNIQUE_ID_IMDB = "imdb"
    UNIQUE_ID_TMDB = "tmdb"
    UNIQUE_ID_TVDB = "tvdb"

    @staticmethod
    def _map_default_unique_id(unique_ids: List[str], media_type: str) -> str:
        if not unique_ids or not media_type:
            return ""

        unique_id_keys = unique_ids.keys()

        # for tvshows, seasons and episodes prefer TVDB
        if media_type in (
            xbmcmediaimport.MediaTypeTvShow,
            xbmcmediaimport.MediaTypeSeason,
            xbmcmediaimport.MediaTypeEpisode,
        ):
            if Api.UNIQUE_ID_TVDB in unique_id_keys:
                return Api.UNIQUE_ID_TVDB

        # otherwise prefer IMDd over TMDd
        if Api.UNIQUE_ID_IMDB in unique_id_keys:
            return Api.UNIQUE_ID_IMDB
        if Api.UNIQUE_ID_TMDB in unique_id_keys:
            return Api.UNIQUE_ID_TMDB

        # last but not least fall back to the first key
        return next(iter(unique_id_keys))
