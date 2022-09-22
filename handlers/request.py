from aiogram import types
from config import dp, bot, req_type, req_IE, req_name, group_id, data
import markup
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
import pickle


class FSM_request(StatesGroup):
    type_state = State()
    IE_state = State()
    name_state = State()
    text_state = State()
    contact_state = State()


async def submit_request(message: types.Message, state: FSMContext):
    async with state.proxy() as base:
        await bot.send_message(group_id, f"Заявка #{list(await data.get_request_id(message.from_user.id))[0]} \n"
                                         f"Пользователь: @{message.from_user.username} \n"
                                         f"Тип заявки: {base['req_type']} \n"
                                         f"Название организации: {base['req_IE']} \n"
                                         f"Название заведения: {base['req_name']} \n"
                                         f"Контакты: {base['contact']} \n")
        try:
            text_amount = base['txt_amount']
        except KeyError:
            text_amount = 0
        try:
            photo_amount = base['photo_amount']
        except KeyError:
            photo_amount = 0
        try:
            doc_amount = base['doc_amount']
        except KeyError:
            doc_amount = 0

        if bool(text_amount):
            text = ' '
            for amount in range(1, text_amount + 1):
                text += base['text' + str(amount)] + ' '
            await bot.send_message(group_id, f"Текст заявки: {text}")
        if bool(photo_amount):
            for amount in range(1, photo_amount + 1):
                await bot.send_photo(group_id, base['photo' + str(amount)])
        if bool(doc_amount):
            for amount in range(1, doc_amount + 1):
                await bot.send_document(group_id, base['doc' + str(amount)])
        await data.disable_checker(message.from_user.id)


# @dp.message_handler(lambda message: message.text == 'Оформить заявку')
async def start_getting(message: types.Message):
    await bot.send_message(message.from_user.id, "Ответьте на следующие вопросы: ")
    await bot.send_message(message.from_user.id, "Выберите тип заявки ", reply_markup=markup.request_Inline(req_type))
    await FSM_request.type_state.set()


# @dp.callback_query_handlers(state=FSM_request.type_state)
async def choose_IE(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as base:
        base['req_type'] = req_type[int(callback_query.data)]
    await bot.send_message(callback_query.from_user.id, "Принял")
    await bot.send_message(callback_query.from_user.id, "Выберите название вашей организации: ",
                           reply_markup=markup.request_Inline(req_IE))
    await FSM_request.next()


# @dp.callback_query_handlers(state=FSM_request.IE_state)
async def choose_name(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as base:
        base['req_IE'] = req_IE[int(callback_query.data)]
        await bot.send_message(callback_query.from_user.id, "Принял")
        await bot.send_message(callback_query.from_user.id, "Выберите название вашего заведения: ",
                               reply_markup=markup.request_Inline_dict(req_name, base['req_IE']))
    await FSM_request.next()


# @dp.callback_query_handlers(state=FSM_request.name_state)
async def submit_text(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as base:
        base['req_name'] = req_name[base['req_IE']][int(callback_query.data)]
    await bot.send_message(callback_query.from_user.id, "Принял")
    await bot.send_message(callback_query.from_user.id, "Опишите запрос в текстовой форме, при надобности отправьте "
                                                        "фото или документы. Когда всё отправите введите команду "
                                                        "/submit")
    await FSM_request.next()


# @dp.message_handler(state=FSM_request.text_state, content_types=['document'])
async def get_document(message: types.Message, state: FSMContext):
    async with state.proxy() as base:
        try:
            base['doc_amount'] += 1
        except KeyError:
            base['doc_amount'] = 1
        base['doc' + str(base['doc_amount'])] = message.document.file_id


# @dp.message_handler(state=FSM_request.text_state, content_types=['photo'])
async def get_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as base:
        try:
            base['photo_amount'] += 1
        except KeyError:
            base['photo_amount'] = 1
        base['photo' + str(base['photo_amount'])] = message.photo[0].file_id


# @dp.message_handler(state=FSM_request.text_state, content_types=['text'])
async def get_text(message: types.Message, state: FSMContext):
    async with state.proxy() as base:
        try:
            base['txt_amount'] += 1
        except KeyError:
            base['txt_amount'] = 1
        base['text' + str(base['txt_amount'])] = message.text


# @dp.message_handler(state=FSM_request.text_state, commands=['submit'])
async def command_submit(message: types.Message):
    await bot.send_message(message.from_user.id, "Принял")
    await bot.send_message(message.from_user.id, "Укажите данные для связи, если вдруг у нас останутся вопросы")
    await FSM_request.next()


# @dp.message_handler(state=FSM_request.contact_state)
async def get_contact(message: types.Message, state: FSMContext):
    async with state.proxy() as base:
        base['contact'] = message.text
        try:
            text_amount = base['txt_amount']
        except KeyError:
            text_amount = 0
        try:
            photo_amount = base['photo_amount']
        except KeyError:
            photo_amount = 0
        try:
            doc_amount = base['doc_amount']
        except KeyError:
            doc_amount = 0

        name = base['req_name']
        IE = base['req_IE']
        r_type = base['req_type']

    text = ''
    photos = []
    docs = []

    if bool(text_amount):
        text = ' '
        for amount in range(1, text_amount + 1):
            text += base['text' + str(amount)] + ' '
    if bool(photo_amount):
        for amount in range(1, photo_amount + 1):
            photos.append(base['photo' + str(amount)])
    if bool(doc_amount):
        for amount in range(1, doc_amount + 1):
            docs.append(base['doc' + str(amount)])

    await data.add_request(message.from_user.id, pickle.dumps(text), pickle.dumps(docs), pickle.dumps(photos), pickle.dumps(message.text), pickle.dumps(IE), pickle.dumps(name), pickle.dumps(r_type))
    await bot.send_message(message.from_user.id, f"Ваша заявка отправлена в работу. Как всё будет готово сообщим! "
                                                 f"Заявка #{list(await data.get_request_id(message.from_user.id))[0]}",
                           reply_markup=markup.checkout())
    await submit_request(message, state)
    await state.finish()


def register_handlers_request(dp: Dispatcher):
    dp.register_message_handler(start_getting, lambda message: message.text == 'Оформить заявку')
    dp.register_callback_query_handler(choose_IE, state=FSM_request.type_state)
    dp.register_callback_query_handler(choose_name, state=FSM_request.IE_state)
    dp.register_callback_query_handler(submit_text, state=FSM_request.name_state)
    dp.register_message_handler(command_submit, state=FSM_request.text_state, commands=['submit'])
    dp.register_message_handler(get_document, state=FSM_request.text_state, content_types=['document'])
    dp.register_message_handler(get_photo, state=FSM_request.text_state, content_types=['photo'])
    dp.register_message_handler(get_text, state=FSM_request.text_state, content_types=['text'])
    dp.register_message_handler(get_contact, state=FSM_request.contact_state)
