from aiogram import Router, types
from pathlib import Path

router = Router()

TEXTS_DIR = Path(__file__).resolve().parent.parent / "texts"

mapping = {
    # Русский
    "📌 Как поступить?": "ru/how_to_apply.txt",
    # "📄 Документы": "ru/documents.txt",
    # "🎯 ЕНТ баллы": "ru/ent_scores.txt",
    "🕓 Сроки подачи": "ru/deadlines.txt",
    "📨 Подача заявления": "ru/submission.txt",
    "📞 Контакты": "ru/contacts.txt",

    # Қазақша
    "📌 Қалай оқуға түсуге болады?": "kz/how_to_apply.txt",
    # "🎯 ҰБТ балдары": "kz/ent_scores.txt",
    "🕓 Құжат тапсыру мерзімдері": "kz/deadlines.txt",
    "📨 Өтініш беру": "kz/submission.txt",
    "📞 Байланыс": "kz/contacts.txt",
}


@router.message(lambda msg: msg.text in mapping)
async def handle_menu_selection(message: types.Message):
    filename = mapping[message.text]
    text_path = TEXTS_DIR / filename
    content = text_path.read_text(encoding="utf-8")
    await message.answer(content, parse_mode="HTML")
