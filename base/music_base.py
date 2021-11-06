from asyncio import sleep
from typing import Union

from pyrogram import types
from pyrogram.errors import FloodWait
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioPiped

from dB.database import db
from dB.lang_utils import get_message as gm
from utils.functions.yt_utils import get_audio_direct_link
from .call_base import CallBase

add_chat = db.add_chat


class MusicPlayer(CallBase):
    def __init__(self):
        super().__init__()

    async def _set_play(
            self,
            chat_id: int,
            user_id: int,
            audio_url: str,
            title: str,
            duration: Union[str, int],
            yt_url: str,
            yt_id: str
    ):
        playlist = self._playlist
        call = self._call
        playlist[chat_id] = [
            {
                "user_id": user_id,
                "title": title,
                "duration": duration,
                "yt_url": yt_url,
                "yt_id": yt_id,
                "stream_type": "music"
            }
        ]
        await self.check_call(chat_id)
        return await call.join_group_call(
            chat_id, AudioPiped(audio_url), stream_type=StreamType().pulse_stream
        )

    async def _play(
            self,
            cb: types.CallbackQuery,
            user_id: int,
            title: str,
            duration: Union[str, int],
            yt_url: str,
            yt_id: str,
    ):
        playlist = self._playlist
        chat_id = cb.message.chat.id
        bot_username, _, _ = await self._bot.get_my()
        mention = await self._bot.get_user_mention(chat_id, user_id)
        if playlist:
            if len(playlist[chat_id]) >= 1:
                self.extend_playlist(user_id, chat_id, title, duration, yt_url, yt_id, "music")
                mess = await cb.edit_message_text(gm(chat_id, "track_queued"))
                await sleep(5)
                return await mess.delete()
        messy = await cb.edit_message_text(gm(chat_id, "process"))
        audio_url = get_audio_direct_link(yt_url)
        try:
            await self._set_play(
                chat_id, user_id, audio_url, title, duration, yt_url, yt_id
            )
            await messy.edit(
                f"""
{gm(chat_id, 'now_playing')}
📌 {gm(chat_id, 'yt_title')}: [{title}](https://t.me/{bot_username}?start=ytinfo_{yt_id})
🕰 {gm(chat_id, 'duration')}: {duration}
✨ {gm(chat_id, 'req_by')}: {mention}
📽 {gm(chat_id, 'stream_type_title')}: {gm(chat_id, 'stream_type')}
""",
                disable_web_page_preview=True
            )
        except FloodWait as e:
            await messy.edit(gm(chat_id, "error_flood").format(e.x))
            await sleep(e.x)
            await self._set_play(
                chat_id, user_id, audio_url, title, duration, yt_url, yt_id
            )
            return await messy.edit(
                f"""
{gm(chat_id, 'now_playing')}
📌 {gm(chat_id, 'yt_title')}: [{title}](https://t.me/{bot_username}?start=ytinfo_{yt_id})
🕰 {gm(chat_id, 'duration')}: {duration}
✨ {gm(chat_id, 'req_by')}: {mention}""",
                disable_web_page_preview=True
            )
