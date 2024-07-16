from aiogram import F
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from bot.text.answer_text import AnswerText
from bot.text.button_text import ButtonText

router = Router(name=__name__)


class ImageUploader(StatesGroup):
    all_images = State()
    message = State()
    image = State()
    names = State()
    face_location = State()


@router.message(F.text == ButtonText.UPLOAD)
async def upload_photo(message: types.Message, state: FSMContext):
    await message.answer(AnswerText.UPLOAD_PHOTO)
    await state.set_state(ImageUploader.image)

