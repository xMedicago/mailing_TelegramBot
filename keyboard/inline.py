from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

btn_cmd_start = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Начать рассылку ✉️", callback_data="mailing")
        ],
        [
            InlineKeyboardButton(text="Информация о юзерботе", callback_data="userbot_info")
        ]
    ])

btn_state_users = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Подтвердить ✅", callback_data="confirm"),
            InlineKeyboardButton(text="Отмена ❌", callback_data="cancel")
        ]
    ])