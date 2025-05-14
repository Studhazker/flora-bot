# main.py
from aiogram import Bot, Dispatcher
from handlers import user, admin
from database import init_db
import config
import logging

# Логирование
logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()

init_db()
dp.include_router(user.router)
dp.include_router(admin.router)

if __name__ == '__main__':
    dp.run_polling(bot)