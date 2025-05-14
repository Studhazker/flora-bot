# main.py
from aiogram import Bot, Dispatcher
from handlers import user, admin
from database import init_db
import config
import logging
import os
from flask import Flask

# Логирование
logging.basicConfig(level=logging.INFO)

# Создаем бота и диспетчера
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()

# Инициализируем БД
init_db()

# Подключаем роутеры
dp.include_router(user.router)
dp.include_router(admin.router)

# Создаем Flask-приложение
app = Flask(__name__)

@app.route('/')
def health_check():
    return 'Bot is running', 200

if __name__ == '__main__':
    # Запускаем Flask в отдельном потоке
    from threading import Thread
    app_thread = Thread(target=app.run, kwargs={
        'host': '0.0.0.0',
        'port': int(os.environ.get("PORT", 5000)),
    })
    app_thread.daemon = True
    app_thread.start()

    # Запускаем бота
    dp.run_polling(bot, skip_updates=True, allowed_updates=dp.resolve_used_update_types())