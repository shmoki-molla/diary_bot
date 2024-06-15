from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
class Case(StatesGroup):
    date = State()
    time = State()
    case = State()

class Day(StatesGroup):
    date = State()

class Number(StatesGroup):
    number = State()

class Number1(StatesGroup):
    number = State()