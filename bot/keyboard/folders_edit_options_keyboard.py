from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.text.button_text import ButtonText


class FoldersEditOption(Enum):
    EDIT_NAME = "edit_name"
    DELETE_FOLDER = "delete_folder"


class FolderEditOptionCbData(CallbackData, prefix="folders_edit_option"):
    action: FoldersEditOption
    person_name: str


def build_folders_edit_options_keyboard(person_name: str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=ButtonText.EDIT_NAME,
                                  callback_data=FolderEditOptionCbData(action=FoldersEditOption.EDIT_NAME,
                                                                       person_name=person_name).pack())],
            [InlineKeyboardButton(text=ButtonText.DELETE_FOLDER,
                                  callback_data=FolderEditOptionCbData(action=FoldersEditOption.DELETE_FOLDER,
                                                                       person_name=person_name).pack())]
        ]
    )
    return markup
