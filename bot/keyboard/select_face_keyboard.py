from enum import Enum
import urllib.parse

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

from bot.config import settings
from bot.text.answer_text import AnswerText
from bot.text.button_text import ButtonText


class SkipCbData(CallbackData, prefix="image_skip"):
    pass


def build_select_face_keyboard(key: str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=ButtonText.SELECT_FACE,
                                  web_app=WebAppInfo(
                                      url=settings.edit_photo_web_page.base_url + '?' +
                                          urllib.parse.urlencode({
                                              'key': key,
                                              'API_TOKEN': settings.api.token,
                                              'API_BASE_URL': settings.api.base_url,
                                              'API_RECOGNITION_PREFIX': settings.api.face_recognition_prefix,
                                              'S3_KEY_ID': settings.s3.key_id,
                                              'S3_ACCESS_KEY': settings.s3.access_key,
                                              'S3_REGION_NAME': settings.s3.region_name,
                                              'S3_ENDPOINT': settings.s3.endpoint,
                                              'S3_BASKET_NAME': settings.s3.basket_name
                                          })))],
            [InlineKeyboardButton(text=ButtonText.SKIP,
                                  callback_data=SkipCbData().pack())]
        ]
    )
    return markup
