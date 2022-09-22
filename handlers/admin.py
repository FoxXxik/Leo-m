import aiogram.utils.exceptions
from aiogram.dispatcher import Dispatcher
from config import dp, bot, data
from aiogram import types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
import pickle


# @dp.message_handler(commands=['admin'], is_chat_admin=True)
async def admin_activated(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, "Для того что-бы узнать список команд администратора пропишите "
                                                     "/help")
        if await data.is_user_exists(message.from_user.id):
            await data.set_admin(message.from_user.id)
    except aiogram.utils.exceptions.BotBlocked:
        await bot.send_message(message.chat.id, "Сначала активируйте бота, написав ему в личных сообщениях команду "
                                                "/start, после чего введите ещё раз команду /admin в этом чате")


# @dp.message_handler(commands=['help'])
async def command_help(message: types.Message):
    if await data.is_admin(message.from_user.id):
        await bot.send_message(message.from_user.id, "Команда /message отправляет сообщение пользователю \n"
                                                     "Команда /finish завершает заявку и оповещает пользователя \n"
                                                     "Команда /archive возращает весь архив заявок")


class FSM_message(StatesGroup):
    id = State()
    send = State()


# @dp.message_handler(commands=['message'])
async def command_message(message: types.Message):
    if await data.is_admin(message.from_user.id):
        await bot.send_message(message.from_user.id, "Введите номер заявки")
        await FSM_message.id.set()


# @dp.message_handler(state=FSM_message.id)
async def id_req(message: types.Message, state: FSMContext):
    if await data.is_admin(message.from_user.id):
        if await data.is_request_exists(message.text):
            async with state.proxy() as base:
                base['id'] = message.text
            await bot.send_message(message.from_user.id, "Введите текст который хотите отправить пользователю")
            await FSM_message.next()
        else:
            await bot.send_message(message.from_user.id, "Заявка не найдена или уже завершена. Попробуйте ещё раз. "
                                                         "Ввод должен осуществляться без #")


# @dp.message_handler(state=FSM_message.send)
async def submit_message(message: types.Message, state: FSMContext):
    if await data.is_admin(message.from_user.id):
        try:
            async with state.proxy() as base:
                await bot.send_message(await data.get_tele_id(base['id']), "Сообщение от администратора "
                                                                           f"по заявке #{base['id']}: {message.text}")
                await bot.send_message(message.from_user.id, "Отправил")
        except aiogram.utils.exceptions.BotBlocked:
            await bot.send_message(message.from_user.id, "Пользователь приостановил работу боту. Отправка не возможна!")
        await state.finish()


class FSM_finish(StatesGroup):
    finish = State()


@dp.message_handler(commands=['finish'])
async def command_finish(message: types.Message):
    if await data.is_admin(message.from_user.id):
        await bot.send_message(message.from_user.id, "Введите номер заявки")
        await FSM_finish.finish.set()


@dp.message_handler(state=FSM_finish.finish)
async def finishing_req(message: types.Message, state: FSMContext):
    if await data.is_admin(message.from_user.id):
        if await data.is_request_exists(message.text):
            await bot.send_message(message.from_user.id, "Заявка отмечена законченной. Работа с ней больше не "
                                                         "возможна. Пользователь будет оповещен")
            try:
                await bot.send_message(await data.get_tele_id(message.text), f"Ваша заявка #{message.text} окончена")
            except aiogram.utils.exceptions.BotBlocked:
                await bot.send_message(message.from_user.id, "Пользователь приостановил работу бота. Оповещение не "
                                                             "возможно!")
            await data.finish_req(message.text)
            await state.finish()
        else:
            await bot.send_message(message.from_user.id, "Заявка не найдена или уже завершена. Попробуйте ещё раз. "
                                                         "Ввод должен осуществляться без #")


class FSM_archive(StatesGroup):
    archive = State()


async def command_archive(message: types.Message):
    if await data.is_admin(message.from_user.id):
        await bot.send_message(message.from_user.id, "Введите номер заявки")
        await FSM_archive.archive.set()


async def archive_req(message: types.Message, state: FSMContext):
    if await data.is_admin(message.from_user.id):
        if await data.is_archive_req(message.text):
            rid = message.text
            status = bool(int(await data.get_status(rid)))
            if status:
                status = 'Завершена'
            else:
                status = 'Активна'
            text = pickle.loads(await data.get_text(rid))
            req_type = pickle.loads(await data.get_type(rid))
            IE = pickle.loads(await data.get_IE(rid))
            name = pickle.loads(await data.get_name(rid))
            photos = pickle.loads(await data.get_photos(rid))
            docs = pickle.loads(await data.get_docs(rid))
            contact = pickle.loads(await data.get_contact(rid))

            await bot.send_message(message.from_user.id, f"Заявка #{rid} \n"
                                                         f"Статус: {status} \n"
                                                         f"Тип заявки: {req_type} \n"
                                                         f"Название организации: {IE} \n"
                                                         f"Название заведения: {name} \n"
                                                         f"Контакты: {contact} \n"
                                                         f"Текст: {text}")
            if bool(photos):
                for value in photos:
                    await bot.send_photo(message.from_user.id, value)
            if bool(docs):
                for value in docs:
                    await bot.send_document(message.from_user.id, value)
            await state.finish()
        else:
            await bot.send_message(message.from_user.id, "Заявка не найдена. Попробуйте ещё раз. "
                                                         "Ввод должен осуществляться без #")

def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(admin_activated, commands=['admin'], is_chat_admin=True)
    dp.register_message_handler(command_help, commands=['help'])
    dp.register_message_handler(command_message, commands=['message'])
    dp.register_message_handler(id_req, state=FSM_message.id)
    dp.register_message_handler(submit_message, state=FSM_message.send)
    dp.register_message_handler(command_archive, commands=['archive'])
    dp.register_message_handler(archive_req, state=FSM_archive.archive)
