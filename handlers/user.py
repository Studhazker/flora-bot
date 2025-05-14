# handlers/user.py
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from states import BouquetBuilder
from keyboards import main_menu_kb, flower_kb, wrapping_kb, confirm_kb
from utils.price_calculator import calculate_price
from database import SessionLocal, User, Order

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Добро пожаловать в цветочный бот! Выберите действие:", reply_markup=main_menu_kb)


@router.message(lambda message: message.text == "Собрать букет")
async def build_bouquet(message: types.Message, state: FSMContext):
    await state.set_state(BouquetBuilder.flower_type)
    await message.answer("Выберите тип цветов:", reply_markup=flower_kb)

@router.message(BouquetBuilder.flower_type)
async def process_flower(message: types.Message, state: FSMContext):
    await state.update_data(flower=message.text)
    await state.set_state(BouquetBuilder.quantity)
    await message.answer("Введите количество цветов:")

@router.message(BouquetBuilder.quantity)
async def process_quantity(message: types.Message, state: FSMContext):
    try:
        quantity = int(message.text)
    except ValueError:
        await message.answer("Пожалуйста, введите число.")
        return
    await state.update_data(quantity=quantity)
    await state.set_state(BouquetBuilder.wrapping)
    await message.answer("Выберите упаковку:", reply_markup=wrapping_kb)

@router.message(BouquetBuilder.wrapping)
async def process_wrapping(message: types.Message, state: FSMContext):
    data = await state.get_data()
    flower = data['flower']
    quantity = data['quantity']
    wrapping = message.text
    total = calculate_price(flower, quantity, wrapping)
    await state.update_data(wrapping=wrapping, total_price=total)
    await message.answer(
        f"Ваш букет:\n"
        f"{flower} x {quantity} шт — {total} руб\n"
        f"Подтвердите заказ.",
        reply_markup=confirm_kb
    )
    await state.set_state(BouquetBuilder.confirm)

@router.message(BouquetBuilder.confirm)
async def confirm_order(message: types.Message, state: FSMContext):
    if message.text != "Подтвердить":
        await message.answer("Заказ отменён.", reply_markup=main_menu_kb)
        await state.clear()
        return

    data = await state.get_data()
    db = SessionLocal()
    order = Order(
        user_id=message.from_user.id,
        flower=data['flower'],
        quantity=data['quantity'],
        wrapping=data['wrapping'],
        total_price=data['total_price']
    )
    db.add(order)
    db.commit()
    await message.answer("Заказ подтверждён! Мы свяжемся с вами.", reply_markup=main_menu_kb)
    await state.clear()

@router.message(lambda message: message.text == "Мои заказы")
async def my_orders(message: types.Message):
    db = SessionLocal()
    orders = db.query(Order).filter(Order.user_id == message.from_user.id).all()
    if not orders:
        await message.answer("У вас пока нет заказов.")
        return
    for order in orders:
        await message.answer(
            f"Заказ #{order.id}\n"
            f"Цветы: {order.flower} x {order.quantity}\n"
            f"Упаковка: {order.wrapping}\n"
            f"Цена: {order.total_price} руб\n"
            f"Статус: {order.status}"
        )