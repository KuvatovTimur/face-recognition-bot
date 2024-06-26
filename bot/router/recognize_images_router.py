from aiogram import F, types, Router
from aiogram.fsm.context import FSMContext


from bot.api.recognition_api import recognize_image, set_image
from bot.keyboard.base_keyboard import build_base_kb
from bot.middleware.image_album_middleware import AlbumMiddleware
from bot.repository.s3_repository import s3_put_image
from bot.router.upload_router import ImageUploader
from bot.text.answer_text import AnswerText

router = Router(name=__name__)
router.message.middleware(AlbumMiddleware())


def get_key(photo_info: types.Message):
    return photo_info.photo[-1].file_id + '.jpg'


async def set_photo(photo_info: types.Message, name):
    status = await set_image(str(photo_info.from_user.id), name, get_key(photo_info))


async def handle_photo(user_id: str, photo_message: types.Message):
    key = get_key(photo_message)
    await s3_put_image(photo_message.photo[-1], key, 'image/jpg')
    return await recognize_image(user_id, key)


async def process_photos(state):
    photo_messages = (await state.get_data())["all_images"]
    exists_unknown_photo = False
    for i in range(len(photo_messages)):
        response = await handle_photo(str(photo_messages[i].from_user.id), photo_messages[i])
        if response.status == 400:
            await state.update_data(all_images=photo_messages[i:])
            await state.update_data(image=(photo_messages[i]))
            await state.set_state(ImageUploader.names)
            await photo_messages[i].reply(AnswerText.UNKNOWN_PERSON)
            exists_unknown_photo = True
            break
    if not exists_unknown_photo:
        await ((await state.get_data())["message"]).reply(AnswerText.IMAGES_UPLOAD_SUCCESSFULLY, reply_markup=build_base_kb())


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
        await ((await state.get_data())["message"]).reply(AnswerText.IMAGES_UPLOAD_SUCCESSFULLY, reply_markup=build_base_kb())
        await state.clear()
    else:
        await process_photos(state)


@router.message(ImageUploader.names, F.text)
async def handle_set_names(message: types.Message, state: FSMContext):
    for name in [name.strip() for name in message.text.split(',')]:
        await set_photo((await state.get_data())["image"], name)
    await state.update_data(all_images=((await state.get_data())["all_images"][1:]))
    await check_all_photos_processed(state)
