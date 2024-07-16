from aiogram import F
from aiogram import Router, types
from aiogram.enums import ParseMode
from aiogram.utils.markdown import text

from bot.keyboard.base_keyboard import build_base_kb
from bot.text.button_text import ButtonText

router = Router(name=__name__)


@router.message(F.text == ButtonText.GET_TELEGRAM_ID)
async def get_user_id(message: types.Message):
    await message.answer(text(f"\n```\n{message.from_user.id}\n```"),
                         parse_mode=ParseMode.MARKDOWN_V2, keyboard=build_base_kb())
