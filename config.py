from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from DataBase import db

storage = MemoryStorage()

#       bot = Bot(token='5737815715:AAED6v1LzFgGkr80FN6f3DL-eM_nVbl8Jfc')
dp = Dispatcher(bot, storage=storage)
data = db.TeleData('DataBase/server.db')

#       group_id = -1001640412647

# Вопросы

req_type = ['Добавить кнопку в кассу liko', 'Изменить продажную стоимость блюда', 'Заявка на оплату счёта',
            'Отправить бланк инвентаризации']
req_IE = ['ИП Редькина Д.В.', 'ИП Редькин В.И.', 'ИП Шахматова А.М.', 'ИП Саблина В.А.', 'ИП Керимов И.',
          'ИП Балашова А.С.', 'ИП Тургумбаева Н.Б', 'ИП Хам В.Л.', 'ИП Новиков А.А.', 'ИП Орлова К.Е.',
          'ИП Цай С.В.']

req_name = {
    'ИП Редькина Д.В.': ['Домодедово Лунная', 'Курыжова', 'Квартал'],
    'ИП Редькин В.И.': ['Подольск Ленина', 'Кузнечики', 'Румянцево'],
    'ИП Шахматова А.М.': ['Ватутинки'],
    'ИП Саблина В.А.': ['Поляны'],
    'ИП Керимов И.': ['Мытищи'],
    'ИП Балашова А.С.': ['Испанские кварталы'],
    'ИП Тургумбаева Н.Б': ['Ясеневая'],
    'ИП Хам В.Л.': ['Александры Монаховой'],
    'ИП Новиков А.А.': ['Саларьево'],
    'ИП Орлова К.Е.': ['Люблино'],
    'ИП Цай С.В.': ['Скандинавия']
}


