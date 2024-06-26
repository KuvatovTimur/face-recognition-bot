from aiogram import Router, types
from aiogram.filters import CommandStart

from bot.keyboard.base_keyboard import build_base_kb
from bot.text.answer_text import AnswerText

router = Router(name=__name__)


@router.message(CommandStart())
async def start(message: types.Message):
    await message.answer(AnswerText.MENU,
                         reply_markup=build_base_kb())
