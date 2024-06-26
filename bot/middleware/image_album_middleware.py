import asyncio
from typing import Union, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import Message


class AlbumMiddleware(BaseMiddleware):
    def __init__(self, latency: Union[int, float] = 0.1):
        self.latency = latency
        self.album_data = {}

    def collect_album_messages(self, event: Message):
        if event.media_group_id not in self.album_data:
            self.album_data[event.media_group_id] = {"messages": []}
        self.album_data[event.media_group_id]["messages"].append(event)
        return len(self.album_data[event.media_group_id]["messages"])

    #
    async def __call__(self, handler, event: Message, data: Dict[str, Any]) -> Any:
        if not event.media_group_id:
            data["album"] = [event]
            return await handler(event, data)

        if event.media_group_id not in self.album_data:
            self.album_data[event.media_group_id] = {"messages": []}

        self.album_data[event.media_group_id]["messages"].append(event)
        total_after = len(self.album_data[event.media_group_id]["messages"])

        await asyncio.sleep(self.latency)

        if event.media_group_id in self.album_data and "messages" in self.album_data[event.media_group_id] and total_after == len(self.album_data[event.media_group_id]["messages"]):
            album_messages = self.album_data[event.media_group_id]["messages"]
            album_messages.sort(key=lambda x: x.message_id)
            data["album"] = album_messages
            del self.album_data[event.media_group_id]
            return await handler(event, data)
