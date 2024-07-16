import urllib.parse
from typing import List

from aiogram import types
from aiogram.filters.callback_data import CallbackData
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, WebAppInfo, InlineKeyboardButton

from bot.api.recognition_api import get_all_person_names
from bot.config import settings


class FolderCbData(CallbackData, prefix="folder_data"):
    person_name: str


async def build_web_app_kb(person_names: List[str]) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=person_name,
                                               web_app=WebAppInfo(
                                                   url=settings.web_app.base_url + '?' +
                                                       urllib.parse.urlencode(
                                                           {'person_name': person_name,
                                                            'API_TOKEN': settings.api.token,
                                                            'API_BASE_URL': settings.api.base_url,
                                                            'API_RECOGNITION_PREFIX': settings.api.face_recognition_prefix,
                                                            'S3_KEY_ID': settings.s3.key_id,
                                                            'S3_ACCESS_KEY': settings.s3.access_key,
                                                            'S3_REGION_NAME': settings.s3.region_name,
                                                            'S3_ENDPOINT': settings.s3.endpoint,
                                                            'S3_BASKET_NAME': settings.s3.basket_name
                                                            }))),
                          InlineKeyboardButton(text='✏️ Edit',
                                               callback_data=FolderCbData(person_name=person_name).pack())] for
                         person_name in
                         person_names],
    )
    return markup
