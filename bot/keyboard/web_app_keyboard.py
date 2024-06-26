import urllib.parse

from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, WebAppInfo, InlineKeyboardButton

from bot.api.recognition_api import get_all_person_names
from bot.config import settings


async def build_web_app_kb(user_id: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=person_name,
                                               web_app=WebAppInfo(
                                                   url=settings.web_app.base_url + '?' +
                                                       urllib.parse.urlencode({'person_name': person_name})))] for
                         person_name in
                         await get_all_person_names(user_id)],
    )
    return markup
