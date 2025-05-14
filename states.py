# states.py
from aiogram.fsm.state import State, StatesGroup

class BouquetBuilder(StatesGroup):
    flower_type = State()
    quantity = State()
    wrapping = State()
    confirm = State()

class AdminStates(StatesGroup):
    choose_order = State()
    choose_status = State()