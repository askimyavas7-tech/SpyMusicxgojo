import asyncio
import os
from datetime import datetime, timedelta
from typing import Union

from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup
from pytgcalls import PyTgCalls, StreamType
from pytgcalls.exceptions import AlreadyJoinedError, NoActiveGroupCall, TelegramServerError
from pytgcalls.types import Update
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio, MediumQualityVideo
from pytgcalls.types.stream import StreamAudioEnded

import config

from Spy.logging import LOGGER
from Spy.core.bot import app
from Spy.platforms.youtube import YouTubeAPI
from Spy.misc import db
from Spy.utils.database import (
    add_active_chat,
    add_active_video_chat,
    get_lang,
    get_loop,
    group_assistant,
    is_autoend,
    music_on,
    remove_active_chat,
    remove_active_video_chat,
    set_loop,
)
from Spy.utils.exceptions import AssistantErr
from Spy.utils.formatters import check_duration, seconds_to_min, speed_converter
from Spy.utils.inline.play import stream_markup
from Spy.utils.stream.autoclear import auto_clean
from Spy.utils.thumbnails import get_thumb
from strings import get_string

YouTube = YouTubeAPI()

autoend = {}
counter = {}


async def _clear_(chat_id: int):
    db[chat_id] = []
    await remove_active_video_chat(chat_id)
    await remove_active_chat(chat_id)


class Call(PyTgCalls):
    def __init__(self):
        self.userbot1 = Client("SpyAss1", api_id=config.API_ID, api_hash=config.API_HASH, session_string=str(config.STRING1))
        self.one = PyTgCalls(self.userbot1)

        self.userbot2 = Client("SpyAss2", api_id=config.API_ID, api_hash=config.API_HASH, session_string=str(config.STRING2))
        self.two = PyTgCalls(self.userbot2)

        self.userbot3 = Client("SpyAss3", api_id=config.API_ID, api_hash=config.API_HASH, session_string=str(config.STRING3))
        self.three = PyTgCalls(self.userbot3)

        self.userbot4 = Client("SpyAss4", api_id=config.API_ID, api_hash=config.API_HASH, session_string=str(config.STRING4))
        self.four = PyTgCalls(self.userbot4)

        self.userbot5 = Client("SpyAss5", api_id=config.API_ID, api_hash=config.API_HASH, session_string=str(config.STRING5))
        self.five = PyTgCalls(self.userbot5)

    async def pause_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        await assistant.pause_stream(chat_id)

    async def resume_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        await assistant.resume_stream(chat_id)

    async def stop_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        try:
            await _clear_(chat_id)
            await assistant.leave_group_call(chat_id)
        except Exception as e:
            LOGGER(__name__).error(f"stop_stream error: {e}")

    async def join_call(self, chat_id: int, original_chat_id: int, link, video=False):
        assistant = await group_assistant(self, chat_id)
        language = await get_lang(chat_id)
        _ = get_string(language)

        stream = (
            AudioVideoPiped(link, audio_parameters=HighQualityAudio(), video_parameters=MediumQualityVideo())
            if video
            else AudioPiped(link, audio_parameters=HighQualityAudio())
        )

        try:
            await assistant.join_group_call(chat_id, stream, stream_type=StreamType().pulse_stream)
        except NoActiveGroupCall:
            raise AssistantErr(_["call_8"])
        except AlreadyJoinedError:
            raise AssistantErr(_["call_9"])
        except TelegramServerError:
            raise AssistantErr(_["call_10"])

        await add_active_chat(chat_id)
        await music_on(chat_id)

        if video:
            await add_active_video_chat(chat_id)

        if await is_autoend():
            users = len(await assistant.get_participants(chat_id))
            if users == 1:
                autoend[chat_id] = datetime.now() + timedelta(minutes=1)

    async def change_stream(self, client, chat_id: int):
        check = db.get(chat_id)
        if not check:
            return

        try:
            loop = await get_loop(chat_id)
            if loop == 0:
                popped = check.pop(0)
                await auto_clean(popped)
            else:
                await set_loop(chat_id, loop - 1)

            if not check:
                await _clear_(chat_id)
                return await client.leave_group_call(chat_id)
        except Exception as e:
            LOGGER(__name__).error(f"Queue error: {e}")
            await _clear_(chat_id)
            return await client.leave_group_call(chat_id)

        queued = check[0]["file"]
        videoid = check[0]["vidid"]
        streamtype = check[0]["streamtype"]
        original_chat_id = check[0]["chat_id"]
        language = await get_lang(chat_id)
        _ = get_string(language)

        video = streamtype == "video"

        if "live_" in queued:
            try:
                n, link = await YouTube.video(videoid, True)
            except Exception as e:
                LOGGER(__name__).error(f"YouTube.video failed: {e}")
                return await app.send_message(original_chat_id, _["call_6"])

            stream = (
                AudioVideoPiped(link, audio_parameters=HighQualityAudio(), video_parameters=MediumQualityVideo())
                if video
                else AudioPiped(link, audio_parameters=HighQualityAudio())
            )

            await client.change_stream(chat_id, stream)

    async def ping(self):
        pings = []
        if config.STRING1:
            pings.append(await self.one.ping)
        if config.STRING2:
            pings.append(await self.two.ping)
        if config.STRING3:
            pings.append(await self.three.ping)
        if config.STRING4:
            pings.append(await self.four.ping)
        if config.STRING5:
            pings.append(await self.five.ping)
        return str(round(sum(pings) / len(pings), 3))

    async def start(self):
        LOGGER(__name__).info("Starting PyTgCalls Client...")
        if config.STRING1:
            await self.one.start()
        if config.STRING2:
            await self.two.start()
        if config.STRING3:
            await self.three.start()
        if config.STRING4:
            await self.four.start()
        if config.STRING5:
            await self.five.start()

    async def decorators(self):
        @self.one.on_stream_end()
        @self.two.on_stream_end()
        @self.three.on_stream_end()
        @self.four.on_stream_end()
        @self.five.on_stream_end()
        async def stream_end_handler(client, update: Update):
            if isinstance(update, StreamAudioEnded):
                await self.change_stream(client, update.chat_id)


Sagar = Call()
