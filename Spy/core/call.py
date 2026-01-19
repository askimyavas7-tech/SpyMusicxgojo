import asyncio
from typing import Union, Dict, List

from pytgcalls import PyTgCalls, StreamType
from pytgcalls.types import Update
from pytgcalls.types.stream import StreamAudioEnded
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio, MediumQualityVideo
from pytgcalls.exceptions import (
    AlreadyJoinedError,
    NoActiveGroupCall,
    TelegramServerError,
)

import config
from Spy import app, LOGGER
from Spy.misc import db
from Spy.utils.database import (
    group_assistant,
    add_active_chat,
    add_active_video_chat,
    remove_active_chat,
    remove_active_video_chat,
)
from Spy.utils.exceptions import AssistantErr


# === GLOBAL STATES (IMPORT HATALARINI ÖNLEMEK İÇİN) ===
autoend: Dict[int, bool] = {}
counter: Dict[int, int] = {}


async def _clear_(chat_id: int):
    db[chat_id] = []
    await remove_active_video_chat(chat_id)
    await remove_active_chat(chat_id)
    autoend.pop(chat_id, None)
    counter.pop(chat_id, None)


class Call(PyTgCalls):
    def __init__(self):
        self.clients: List[PyTgCalls] = []

        for i in range(1, 6):
            string = getattr(config, f"STRING{i}", None)
            if not string:
                continue

            from pyrogram import Client  # lazy import

            user = Client(
                name=f"Assistant{i}",
                api_id=config.API_ID,
                api_hash=config.API_HASH,
                session_string=str(string),
            )

            call = PyTgCalls(user, cache_duration=100)
            self.clients.append(call)

        if not self.clients:
            raise RuntimeError("Hiçbir assistant string tanımlı değil!")


    async def start(self):
        LOGGER(__name__).info("Starting PyTgCalls Clients...")
        for client in self.clients:
            await client.start()
        await self.decorators()


    async def get_client(self, chat_id: int) -> PyTgCalls:
        return await group_assistant(self, chat_id)


    async def join_call(self, chat_id: int, link: str, video: bool = False):
        client = await self.get_client(chat_id)

        stream = (
            AudioVideoPiped(
                link,
                audio_parameters=HighQualityAudio(),
                video_parameters=MediumQualityVideo(),
            )
            if video
            else AudioPiped(link, audio_parameters=HighQualityAudio())
        )

        try:
            await client.join_group_call(
                chat_id,
                stream,
                stream_type=StreamType().pulse_stream,
            )
        except NoActiveGroupCall:
            raise AssistantErr("Önce sesli sohbet başlat.")
        except AlreadyJoinedError:
            raise AssistantErr("Zaten yayındayım.")
        except TelegramServerError:
            raise AssistantErr("Telegram sunucu hatası.")

        autoend[chat_id] = False
        counter[chat_id] = 0

        await add_active_chat(chat_id)
        if video:
            await add_active_video_chat(chat_id)


    async def stop_stream(self, chat_id: int):
        client = await self.get_client(chat_id)
        await _clear_(chat_id)

        try:
            await client.leave_group_call(chat_id)
        except Exception:
            pass


    async def change_stream(self, client: PyTgCalls, chat_id: int):
        queue = db.get(chat_id)

        if not queue:
            await _clear_(chat_id)
            return await client.leave_group_call(chat_id)

        queue.pop(0)

        if not queue:
            await _clear_(chat_id)
            return await client.leave_group_call(chat_id)

        next_track = queue[0]
        link = next_track["file"]
        video = next_track.get("streamtype") == "video"

        stream = (
            AudioVideoPiped(
                link,
                audio_parameters=HighQualityAudio(),
                video_parameters=MediumQualityVideo(),
            )
            if video
            else AudioPiped(link, audio_parameters=HighQualityAudio())
        )

        await client.change_stream(chat_id, stream)


    async def decorators(self):
        for client in self.clients:

            @client.on_stream_end()
            async def stream_end_handler(_, update: Update):
                if isinstance(update, StreamAudioEnded):
                    await self.change_stream(_, update.chat_id)

            @client.on_left()
            @client.on_kicked()
            @client.on_closed_voice_chat()
            async def leave_handler(_, chat_id: int):
                await _clear_(chat_id)


# === GERİYE UYUMLULUK (TÜM BOT BOZULMASIN DİYE) ===
Sagar = Call()

__all__ = ["Call", "Sagar", "autoend", "counter"]
