from aiogram import Router, types
from aiogram import F

from bot.text.answer_text import AnswerText
from bot.text.button_text import ButtonText
from bot.keyboard.web_app_keyboard import build_web_app_kb

router = Router(name=__name__)


@router.message(F.text == ButtonText.MY_FILES)
async def my_photo(message: types.Message):
    await message.answer(AnswerText.GROUPS,
                         reply_markup=await build_web_app_kb(message.from_user.id))
