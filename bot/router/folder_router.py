from aiogram import F
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery

from bot.api.recognition_api import rename_person, delete_person, get_all_person_names
from bot.keyboard.delete_folder_or_not_keyboard import build_delete_folder_or_not_keyboard, FolderDeleteCbData
from bot.keyboard.folders_edit_options_keyboard import build_folders_edit_options_keyboard, FolderEditOptionCbData, \
    FoldersEditOption
from bot.keyboard.web_app_keyboard import build_web_app_kb, FolderCbData
from bot.text.answer_text import AnswerText
from bot.text.button_text import ButtonText

router = Router(name=__name__)


class FolderEdit(StatesGroup):
    person_name: str
    callback_query: CallbackQuery
    new_person_name = State()
    deleted_person_name = State()


@router.message(F.text == ButtonText.MY_FILES)
async def my_photo(message: types.Message, user_id: int | None = None):
    person_names = await get_all_person_names(message.from_user.id if not user_id else user_id)
    if len(person_names) == 0:
        await message.answer(AnswerText.PHOTOS_NOT_FOUND),
    else:
        web_app_cb = await build_web_app_kb(person_names)
        await message.answer(AnswerText.GROUPS,
                             reply_markup=web_app_cb)




@router.callback_query(FolderCbData.filter())
async def show_edit_folder_options(callback_query: CallbackQuery, callback_data: FolderCbData, ):
    await callback_query.message.edit_text(callback_data.person_name,
                                           reply_markup=build_folders_edit_options_keyboard(callback_data.person_name))


@router.callback_query(FolderEditOptionCbData.filter(F.action == FoldersEditOption.EDIT_NAME))
async def rename_folder(callback_query: CallbackQuery, callback_data: FolderEditOptionCbData, state: FSMContext):
    await state.set_state(FolderEdit.new_person_name)
    await state.update_data(person_name=callback_data.person_name)
    await state.update_data(callback_query=callback_query)
    await callback_query.message.answer(AnswerText.INPUT_NEW_FOLDER_NAME)


@router.message(FolderEdit.new_person_name, F.text)
async def handle_rename_person(message: types.Message, state: FSMContext):
    response = await rename_person(message.from_user.id, (await state.get_data())["person_name"], message.text)
    if response.status == 400:
        await ((await state.get_data())["callback_query"]).answer(AnswerText.FOLDER_ALREADY_EXISTS)
    await state.clear()
    await my_photo(message)


@router.callback_query(FolderEditOptionCbData.filter(F.action == FoldersEditOption.DELETE_FOLDER))
async def delete_folder(callback_query: CallbackQuery, callback_data: FolderEditOptionCbData):
    await callback_query.message.answer(AnswerText.DELETE_OR_NOT_FOLDER,
                                        reply_markup=build_delete_folder_or_not_keyboard(callback_data.person_name))


@router.callback_query(FolderDeleteCbData.filter())
async def handle_delete_folder(callback_query: CallbackQuery, callback_data: FolderDeleteCbData):
    if callback_data.is_deleted:
        await delete_person(callback_query.from_user.id, callback_data.person_name)
    await my_photo(callback_query.message, user_id=callback_query.from_user.id)
