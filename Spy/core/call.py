import asyncio
from typing import Dict, List
from pytgcalls import PyTgCalls, StreamType
from pytgcalls.types.stream import StreamAudioEnded
from pytgcalls.types.input_stream import AudioPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio
from pytgcalls.exceptions import AlreadyJoinedError, NoActiveGroupCall, TelegramServerError
from pyrogram import Client

import config
from Spy import LOGGER
from Spy.utils.database import group_assistant, add_active_chat, remove_active_chat
from Spy.utils.exceptions import AssistantErr
from Spy.misc import db

# ===============================================
autoend: Dict[int, bool] = {}
counter: Dict[int, int] = {}

async def _clear_(chat_id: int):
    db[chat_id] = []
    await remove_active_chat(chat_id)
    autoend.pop(chat_id, None)
    counter.pop(chat_id, None)

class Call:
    def __init__(self):
        self.clients: List[PyTgCalls] = []

        for i in range(1, 6):
            string = getattr(config, f"STRING{i}", None)
            if not string:
                continue
            user = Client(
                name=f"Assistant{i}",
                api_id=config.API_ID,
                api_hash=config.API_HASH,
                session_string=str(string)
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

    async def join_call(self, chat_id: int, stream_link: str):
        client = await self.get_client(chat_id)
        audio_stream = AudioPiped(stream_link, audio_parameters=HighQualityAudio())

        try:
            await client.join_group_call(chat_id, audio_stream, stream_type=StreamType().pulse_stream)
        except NoActiveGroupCall:
            raise AssistantErr("Önce sesli sohbet başlat.")
        except AlreadyJoinedError:
            raise AssistantErr("Zaten yayındayım.")
        except TelegramServerError:
            raise AssistantErr("Telegram sunucu hatası.")

        autoend[chat_id] = False
        counter[chat_id] = 0
        await add_active_chat(chat_id)

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
        stream = AudioPiped(link, audio_parameters=HighQualityAudio())
        await client.change_stream(chat_id, stream)

    async def decorators(self):
        for client in self.clients:
            @client.on_stream_end()
            async def stream_end_handler(_, update):
                if isinstance(update, StreamAudioEnded):
                    await self.change_stream(_, update.chat_id)

# ===============================================
Sagar = Call()
__all__ = ["Call", "Sagar", "autoend", "counter"]
