# main.py
from aiogram import Bot, Dispatcher
from handlers import user, admin
from database import init_db
import config
import logging
import os

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

if __name__ == '__main__':
    # Получаем PORT из переменных окружения (Render предоставляет его автоматически)
    port = int(os.environ.get("PORT", 5000))
    
    # Запускаем бота с указанием порта
    dp.run_polling(bot, skip_updates=True, allowed_updates=dp.resolve_used_update_types())