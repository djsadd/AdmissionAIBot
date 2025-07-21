from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from .keyboards import inline_ent_programs

ENT_SCORES = {
    "6В02101": {"title": "Дизайн", "grant": 55, "paid": 55},
    "6В02102": {"title": "Декоративное искусство и этнодизайн", "grant": 55, "paid": 55},
    "6B02103": {"title": "Режиссура", "grant": 55, "paid": 55},
    "6В02301": {"title": "Переводческое дело", "grant": 55, "paid": 55},
    "6В02302": {"title": "Филология", "grant": 55, "paid": 55},
    "6В03101": {"title": "Психология", "grant": 55, "paid": 55},
    "6В04101": {"title": "Экономика", "grant": 55, "paid": 55},
    "6В04102": {"title": "Менеджмент", "grant": 55, "paid": 55},
    "6В04103": {"title": "Учет и аудит", "grant": 55, "paid": 55},
    "6В04104": {"title": "Финансы", "grant": 55, "paid": 55},
    "6В04105": {"title": "Государственное и местное управление", "grant": 55, "paid": 55},
    "6В04107": {"title": "Аудит", "grant": 55, "paid": 55},
    "6В04117": {"title": "Финансы бизнеса", "grant": 55, "paid": 55},
    "6В04201": {"title": "Юриспруденция", "grant": 75, "paid": 75},
    "6В04202": {"title": "Международное право", "grant": 75, "paid": 75},
    "6B04203": {"title": "Цифровая юриспруденция", "grant": 55, "paid": 55},
    "6В04204": {"title": "Правовое регулирование экономики", "grant": 75, "paid": 75},
    "6В06101": {"title": "Информационные системы", "grant": 55, "paid": 55},
    "6В06102": {"title": "Вычислительная техника и программное обеспечение", "grant": 55, "paid": 55},
    "6B06103": {"title": "Digital marketing", "grant": 55, "paid": 55},
    "6В11101": {"title": "Туризм", "grant": 55, "paid": 55},
    "6В11102": {"title": "Ресторанный и гостиничный бизнес", "grant": 55, "paid": 55},
}



router = Router()


@router.message(lambda message: message.text in ["🎯 Пороговые баллы ЕНТ", "📄 Пороговые баллы ЕНТ"])
async def ent_scores_handler(message: types.Message):
    await message.answer(
        "📌 <b>Выберите образовательную программу для просмотра пороговых баллов:</b>",
        reply_markup=inline_ent_programs,
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("ent_"))
async def ent_program_callback(callback: types.CallbackQuery):
    code = callback.data.split("_")[1]
    data = ENT_SCORES.get(code)
    if data:
        grant = data['grant']
        paid = data['paid']
        message = f"🎓 <b>{data['title']}</b>\n\n"
        message += f"📌 Пороговый балл на грант: <b>{grant}</b>\n"
        message += f"💼 Пороговый балл на платное отделение: <b>{paid}</b>\n"

        await callback.message.answer(message, parse_mode="HTML")
    else:
        await callback.message.answer("Программа не найдена.")
    await callback.answer()
