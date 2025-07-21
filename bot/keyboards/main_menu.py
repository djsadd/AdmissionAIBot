from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_menu_ru = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📌 Как поступить?"), KeyboardButton(text="📄 Документы")],
        [KeyboardButton(text="🎯 Пороговые баллы ЕНТ"), KeyboardButton(text="🕓 Сроки подачи")],
        [KeyboardButton(text="📞 Контакты"), KeyboardButton(text="💬 Спросить ИИ")],
    ],
    resize_keyboard=True
)

main_menu_ru_exit_bot = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📌 Как поступить?"), KeyboardButton(text="📄 Документы")],
        [KeyboardButton(text="🎯 Пороговые баллы ЕНТ"), KeyboardButton(text="🕓 Сроки подачи")],
        [KeyboardButton(text="📞 Контакты"), KeyboardButton(text="💬 Выход с режима ИИ")],
    ],
    resize_keyboard=True
)


main_menu_kz = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📌 Қалай оқуға түсуге болады?"), KeyboardButton(text="📄 Құжаттар")],
        [KeyboardButton(text="🎯 ҰБТ балдары"), KeyboardButton(text="🕓 Құжат тапсыру мерзімдері")],
        [KeyboardButton(text="📞 Байланыс")],
        [KeyboardButton(text="💬 ЖИ-дан сұрау")],
    ],
    resize_keyboard=True
)

keyboard_lang = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🇷🇺 Русский")]
        ],
        resize_keyboard=True
    )

# , KeyboardButton(text="🇰🇿 Қазақша")