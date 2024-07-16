from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.text.button_text import ButtonText

class FolderDeleteCbData(CallbackData, prefix="folders_delete"):
    person_name: str
    is_deleted: bool


def build_delete_folder_or_not_keyboard(person_name: str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=ButtonText.YES,
                                  callback_data=FolderDeleteCbData(is_deleted=True,
                                                                   person_name=person_name).pack())],
            [InlineKeyboardButton(text=ButtonText.NO,
                                  callback_data=FolderDeleteCbData(is_deleted=False,
                                                                   person_name=person_name).pack())]
        ]
    )
    return markup
