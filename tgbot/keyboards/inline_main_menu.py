from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Обновить базу", callback_data="users_base"),
        InlineKeyboardButton(text="Вывести всю базу", callback_data="full_base")
    ],
    [InlineKeyboardButton(text="Дни рождения на весь месяц", callback_data="month")

     ],
    [
        InlineKeyboardButton(text="Дни рождения на неделю вперед", callback_data="week")
    ]
    # [
    #     InlineKeyboardButton(text="Данные для входа на сайт", callback_data="log_data")
    # ]
])

Base_file = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Отправить Excel файл", callback_data="send_base_file")
    ],
    [InlineKeyboardButton(text="Главное меню", callback_data="menu")]
])
