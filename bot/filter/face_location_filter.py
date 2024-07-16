import json

from aiogram import MagicFilter, types

from bot.model.face_location import FaceLocation


class FaceLocationFilter(MagicFilter):
    async def __call__(self, message: types.Message) -> bool:
        try:
            data = json.loads(message.text)
            if not isinstance(data, dict):
                return False
            face_location = FaceLocation(**data)
            return True
        except (json.JSONDecodeError, TypeError, ValueError):
            return False
