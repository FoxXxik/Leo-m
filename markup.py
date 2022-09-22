from aiogram import types
from config import req_type, req_IE


def request_Inline(choice: list):
    data = 0
    markup = types.InlineKeyboardMarkup(row_width=1)
    for value in choice:
        button = types.InlineKeyboardButton(value, callback_data=str(data))
        markup.add(button)
        data += 1
    return markup


def request_Inline_dict(choice: dict, IE: str):
    data = 0
    markup = types.InlineKeyboardMarkup(row_width=1)
    for value in choice[IE]:
        button = types.InlineKeyboardButton(value, callback_data=str(data))
        markup.add(button)
        data += 1
    return markup


def checkout():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton("Оформить заявку")
    markup.add(button)
    return markup


