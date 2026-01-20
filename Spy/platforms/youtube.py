import asyncio
import os
import re
from typing import Union

import yt_dlp
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message
from youtubesearchpython.__future__ import VideosSearch

from Spy.utils.database import is_on_off
from Spy.utils.formatters import time_to_seconds

cookies_file = "cookies.txt"

YTDLP_BASE_OPTS = {
    "quiet": True,
    "nocheckcertificate": True,
    "ignoreerrors": True,
    "no_warnings": True,
    "geo_bypass": True,
    "cookiefile": cookies_file,
    "cachedir": False,
    "noplaylist": True,
    "extractor_args": {
        "youtube": {
            "player_client": ["android"],
            "skip": ["dash", "hls"],
        }
    },
}


class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:youtube\.com|youtu\.be)"
        self.listbase = "https://youtube.com/playlist?list="

    async def exists(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        return bool(re.search(self.regex, link))

    async def url(self, message_1: Message) -> Union[str, None]:
        messages = [message_1]
        if message_1.reply_to_message:
            messages.append(message_1.reply_to_message)

        for message in messages:
            entities = message.entities or message.caption_entities
            if not entities:
                continue
            for entity in entities:
                if entity.type in [
                    MessageEntityType.URL,
                    MessageEntityType.TEXT_LINK,
                ]:
                    return entity.url or (
                        message.text or message.caption
                    )[entity.offset : entity.offset + entity.length]
        return None

    async def details(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        link = link.split("&")[0]

        results = VideosSearch(link, limit=1)
        result = (await results.next())["result"][0]

        title = result["title"]
        duration_min = result["duration"]
        thumbnail = result["thumbnails"][0]["url"].split("?")[0]
        vidid = result["id"]
        duration_sec = (
            0 if duration_min is None else int(time_to_seconds(duration_min))
        )

        return title, duration_min, duration_sec, thumbnail, vidid

    async def video(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        link = link.split("&")[0]

        ydl_opts = {
            **YTDLP_BASE_OPTS,
            "format": "best[height<=720]/best",
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(link, download=False)
                return 1, info["url"]
        except Exception as e:
            return 0, str(e)

    async def playlist(self, link, limit, user_id, videoid: Union[bool, str] = None):
        if videoid:
            link = self.listbase + link
        link = link.split("&")[0]

        ydl_opts = {
            **YTDLP_BASE_OPTS,
            "extract_flat": True,
            "playlistend": limit,
        }

        ids = []
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=False)
            for entry in info.get("entries", []):
                ids.append(entry["id"])

        return ids

    async def formats(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        link = link.split("&")[0]

        ydl_opts = {**YTDLP_BASE_OPTS}

        formats_available = []
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            r = ydl.extract_info(link, download=False)
            for f in r.get("formats", []):
                if f.get("filesize") and f.get("format_id"):
                    formats_available.append(
                        {
                            "format": f.get("format"),
                            "filesize": f.get("filesize"),
                            "format_id": f.get("format_id"),
                            "ext": f.get("ext"),
                            "format_note": f.get("format_note"),
                            "yturl": link,
                        }
                    )

        return formats_available, link

    async def download(
        self,
        link: str,
        mystic,
        video: Union[bool, str] = None,
        videoid: Union[bool, str] = None,
        songaudio: Union[bool, str] = None,
        songvideo: Union[bool, str] = None,
        format_id: Union[bool, str] = None,
        title: Union[bool, str] = None,
    ):

        if videoid:
            link = self.base + link

        loop = asyncio.get_running_loop()

        def audio_dl():
            ydl_opts = {
                **YTDLP_BASE_OPTS,
                "format": "bestaudio/best",
                "outtmpl": "downloads/%(id)s.%(ext)s",
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(link, download=True)
                return os.path.join("downloads", f"{info['id']}.{info['ext']}")

        def video_dl():
            ydl_opts = {
                **YTDLP_BASE_OPTS,
                "format": "bv*[height<=720]+ba/b",
                "outtmpl": "downloads/%(id)s.%(ext)s",
                "merge_output_format": "mp4",
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(link, download=True)
                return os.path.join("downloads", f"{info['id']}.mp4")

        if video:
            if await is_on_off(1):
                file = await loop.run_in_executor(None, video_dl)
                return file, True
            else:
                return await self.video(link)

        file = await loop.run_in_executor(None, audio_dl)
        return file, True
