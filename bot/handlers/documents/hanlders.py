from aiogram import Router, types, F
from .keyboards import keyboard_doc_submenu
from .texts.text import MESSAGE_DOC_RU, MESSAGE_DOC_SHORT_RU_TIPO, MESSAGE_DOC_SHORT_RU_MAG, MESSAGE_DOC_SHORT_RU_DOC
from aiogram.fsm.context import FSMContext
router = Router()


@router.message(lambda message: message.text in ["📄 Документы", "📄 Құжаттар"])
async def documents_handler(message: types.Message):
    await message.answer("Выберите категорию документов:", reply_markup=keyboard_doc_submenu)


@router.callback_query(F.data == "docs_school")
async def handle_school_docs(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    print(lang)
    await callback.message.answer(MESSAGE_DOC_RU, parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "docs_college")
async def handle_college_docs(callback: types.CallbackQuery):
    await callback.message.answer(MESSAGE_DOC_SHORT_RU_TIPO, parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "docs_magistr")
async def handle_college_docs(callback: types.CallbackQuery):
    await callback.message.answer(MESSAGE_DOC_SHORT_RU_MAG, parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "docs_phd")
async def handle_college_docs(callback: types.CallbackQuery):
    await callback.message.answer(MESSAGE_DOC_SHORT_RU_MAG, parse_mode="HTML")
    await callback.answer()
