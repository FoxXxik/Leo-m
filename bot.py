from config import dp, bot
from aiogram.utils import executor

from handlers import request, commands, admin

request.register_handlers_request(dp)
commands.register_handlers_command(dp)
admin.register_handlers_admin(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
