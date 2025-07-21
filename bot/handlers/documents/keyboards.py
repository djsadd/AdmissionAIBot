from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


keyboard_doc_submenu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🎓 Бакалавриат (школа)", callback_data="docs_school")],
        [InlineKeyboardButton(text="🏫 Бакалавриат (колледж)", callback_data="docs_college")],
        [InlineKeyboardButton(text="🎓 Магистратура", callback_data="docs_magistr")],
        [InlineKeyboardButton(text="📚 Докторантура", callback_data="docs_phd")],
    ]
)