from aiogram import Router, types, F
from aiogram.filters import CommandStart
from keyboards.main_menu import main_menu_ru, keyboard_lang, main_menu_kz
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from texts import text

router = Router()


class Form(StatesGroup):
    choosing_language = State()


@router.message(Form.choosing_language)
async def language_chosen(message: types.Message, state: FSMContext):
    if message.text == "🇷🇺 Русский":
        await state.update_data(lang="ru")
        await message.answer("Вы выбрали русский язык.")
    elif message.text == "🇰🇿 Қазақша":
        await state.update_data(lang="kz")
        await message.answer("Сіз қазақ тілін таңдадыңыз.")
    else:
        await message.answer("Пожалуйста, выберите язык с помощью кнопок.")
        return

    data = await state.get_data()
    lang = data.get("lang", "ru")
    if lang == "ru":
        await message.answer(text.WELCOME_MESSAGE_RU, reply_markup=main_menu_ru)
    elif lang == "kz":
        await message.answer(text.WELCOME_MESSAGE_KZ, reply_markup=main_menu_kz)
    else:
        await message.answer("Язык не выбран. Пожалуйста, выберите язык.")
    await state.clear()


@router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer("Пожалуйста, выберите язык / Тілді таңдаңыз:", reply_markup=keyboard_lang)
    await state.set_state(Form.choosing_language)