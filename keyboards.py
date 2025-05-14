from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Главное меню
main_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Собрать букет"),
            KeyboardButton(text="Мои заказы")
        ]
    ],
    resize_keyboard=True
)

# Клавиатура для выбора цветов
flower_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Розы"),
            KeyboardButton(text="Хризантемы")
        ],
        [
            KeyboardButton(text="Тюльпаны"),
            KeyboardButton(text="Назад")
        ]
    ],
    resize_keyboard=True
)

# Клавиатура для выбора упаковки
wrapping_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Бумага"),
            KeyboardButton(text="Сетка")
        ],
        [
            KeyboardButton(text="Коробка"),
            KeyboardButton(text="Назад")
        ]
    ],
    resize_keyboard=True
)

# Клавиатура для подтверждения заказа
confirm_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Подтвердить"),
            KeyboardButton(text="Отменить")
        ]
    ],
    resize_keyboard=True
)
admin_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Посмотреть заказы"),
            KeyboardButton(text="Изменить статус")
        ]
    ],
    resize_keyboard=True
)