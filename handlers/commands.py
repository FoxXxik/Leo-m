from aiogram import types
from aiogram.dispatcher import Dispatcher
from config import data, bot
import markup


async def command_start(message: types.Message):
    if message.from_user.username == 'None':
        await message.answer(f"{message.from_user.first_name}, Добро пожаловать!", reply_markup=markup.checkout())
    else:
        await message.answer(f"{message.chat.username}, Добро пожаловать!", reply_markup=markup.checkout())
    if not await data.is_user_exists(message.from_user.id):
        await data.add_user(message.from_user.id)


def register_handlers_command(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])