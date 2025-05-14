# handlers/admin.py
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
import config
from keyboards import admin_kb
from database import SessionLocal, Order
from states import AdminStates
from aiogram.filters import Command

router = Router()

@router.message(Command("admin"))
async def cmd_admin(message: types.Message):
    if message.from_user.id == config.ADMIN_ID:
        await message.answer("Вы вошли в админ-панель.", reply_markup=admin_kb)
    else:
        await message.answer("У вас нет доступа к админ-панели.")

@router.message(lambda message: message.text == "Посмотреть заказы")
async def view_orders(message: types.Message):
    db = SessionLocal()
    orders = db.query(Order).all()
    if not orders:
        await message.answer("Нет активных заказов.")
        return
    for order in orders:
        await message.answer(
            f"Заказ #{order.id} от @{order.user_id}\n"
            f"{order.flower} x {order.quantity}, {order.wrapping}\n"
            f"Цена: {order.total_price} руб\n"
            f"Статус: {order.status}"
        )

@router.message(lambda message: message.text == "Изменить статус")
async def change_status(message: types.Message, state: FSMContext):
    db = SessionLocal()
    orders = db.query(Order).all()
    if not orders:
        await message.answer("Нет заказов для изменения статуса.")
        return
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for order in orders:
        kb.add(types.KeyboardButton(str(order.id)))
    await message.answer("Выберите ID заказа для изменения статуса:", reply_markup=kb)
    await state.set_state(AdminStates.choose_order)

@router.message(AdminStates.choose_order)
async def choose_new_status(message: types.Message, state: FSMContext):
    try:
        order_id = int(message.text)
    except ValueError:
        await message.answer("Введите корректный ID.")
        return
    await state.update_data(order_id=order_id)
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("В обработке", "Готовится", "В пути", "Доставлен")
    await message.answer("Выберите новый статус:", reply_markup=kb)
    await state.set_state(AdminStates.choose_status)

@router.message(AdminStates.choose_status)
async def update_status(message: types.Message, state: FSMContext):
    new_status = message.text
    data = await state.get_data()
    order_id = data['order_id']
    db = SessionLocal()
    order = db.query(Order).get(order_id)
    if order:
        order.status = new_status
        db.commit()
        await message.answer(f"Статус заказа #{order_id} обновлён на '{new_status}'", reply_markup=admin_kb)
    else:
        await message.answer("Не найдено")
    await state.clear()