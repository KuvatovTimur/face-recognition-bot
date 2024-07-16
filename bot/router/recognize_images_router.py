import json

import aiohttp
import exif
from aiofiles import tempfile
from aiogram import F, types, Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from exif import Image

from bot.api.recognition_api import recognize_image, set_image
from bot.config import settings
from bot.filter.face_location_filter import FaceLocationFilter
from bot.keyboard.base_keyboard import build_base_kb
from bot.keyboard.select_face_keyboard import build_select_face_keyboard, SkipCbData
from bot.middleware.image_album_middleware import AlbumMiddleware
from bot.model.face_location import FaceLocation
from bot.repository.s3_repository import s3_put_image
from bot.router.upload_router import ImageUploader
from bot.text.answer_text import AnswerText

router = Router(name=__name__)
router.message.middleware(AlbumMiddleware())


def get_key(photo_info: types.Message):
    return photo_info.photo[-1].file_id + '.jpg'


async def set_photo(photo_info: types.Message, name):
    await set_image(str(photo_info.from_user.id), name, get_key(photo_info))


async def handle_photo(user_id: str, photo_message: types.Message):
    key = get_key(photo_message)
    await s3_put_image(photo_message.photo[-1], key, 'image/jpg')
    return await recognize_image(user_id, key)


async def process_photos(state):
    photo_messages = (await state.get_data())["all_images"]
    is_ok_status = True
    for i in range(len(photo_messages)):
        response = await handle_photo(str(photo_messages[i].from_user.id), photo_messages[i])
        if response.status != 200:
            is_ok_status = False
            await state.update_data(all_images=photo_messages[i:])
            await state.update_data(image=(photo_messages[i]))
        if response.status == 400:
            await state.set_state(ImageUploader.names)
            await photo_messages[i].reply(AnswerText.UNKNOWN_PERSON)
            break
        elif response.status == 422:
            await state.set_state(ImageUploader.face_location)
            await photo_messages[i].reply(AnswerText.FACE_NOT_FOUND,
                                          reply_markup=build_select_face_keyboard(get_key(photo_messages[i])))
            break
    if is_ok_status:
        await ((await state.get_data())["message"]).reply(AnswerText.IMAGES_UPLOAD_SUCCESSFULLY,
                                                          reply_markup=build_base_kb())


bot = Bot(
    token=settings.bot.token,
)


@router.message(ImageUploader.image, F.photo)
async def recognize_images(message: types.Message, album, state: FSMContext):
    photos_messages = album
    await state.update_data(message=message)
    await state.update_data(all_images=photos_messages)
    await process_photos(state)


async def check_all_photos_processed(state: FSMContext):
    photo_messages = (await state.get_data())["all_images"]
    if len(photo_messages) == 0:
        await state.set_state(ImageUploader.image)
        await ((await state.get_data())["message"]).reply(AnswerText.IMAGES_UPLOAD_SUCCESSFULLY,
                                                          reply_markup=build_base_kb())
        await state.clear()
    else:
        await process_photos(state)


@router.message(ImageUploader.names, F.text)
async def handle_set_names(message: types.Message, state: FSMContext):
    for name in [name.strip() for name in message.text.split(',')]:
        await set_photo((await state.get_data())["image"], name)
    await state.update_data(all_images=((await state.get_data())["all_images"][1:]))
    await check_all_photos_processed(state)


@router.message(ImageUploader.face_location, FaceLocationFilter())
async def handle_set_face_location(message: types.Message, state: FSMContext):
    data = json.loads(message.text)
    face_location = FaceLocation(**data)
    response = await recognize_image((await state.get_data())["image"].from_user.id,
                                     get_key((await state.get_data())["image"]),
                                     [face_location])
    if response.status == 400:
        await state.set_state(ImageUploader.names)
        await (await state.get_data())["image"].reply(AnswerText.UNKNOWN_PERSON)
    else:
        await state.update_data(all_images=((await state.get_data())["all_images"][1:]))
        await check_all_photos_processed(state)


@router.callback_query(SkipCbData.filter())
async def handle_skip_photo(callback_query: CallbackQuery, callback_data: SkipCbData, state: FSMContext):
    await state.update_data(all_images=((await state.get_data())["all_images"][1:]))
    await check_all_photos_processed(state)
