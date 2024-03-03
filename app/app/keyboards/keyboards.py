from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


yes_button = InlineKeyboardButton(text="Да", callback_data="yes")
no_button = InlineKeyboardButton(text="Нет", callback_data="no")

cancel_button = InlineKeyboardButton(text="Отменить", callback_data="cancel")
send_message_button = InlineKeyboardButton(text="Отправить глагол", callback_data="send_word")


send_word_keyboard = InlineKeyboardMarkup(inline_keyboard=[[send_message_button]])
