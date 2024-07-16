from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.text.button_text import ButtonText


def build_base_kb() -> ReplyKeyboardMarkup:
    upload_button = KeyboardButton(text=ButtonText.UPLOAD)
    my_files_btn = KeyboardButton(text=ButtonText.MY_FILES)
    register_btn = KeyboardButton(text=ButtonText.GET_TELEGRAM_ID)
    markup = ReplyKeyboardMarkup(
        keyboard=[[upload_button, my_files_btn, register_btn]],
        resize_keyboard=True
    )
    return markup
