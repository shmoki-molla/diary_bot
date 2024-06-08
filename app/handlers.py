from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
import app.keyboard as kb
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import app.database.requests as rq
from app.database.models import User, Case
from datetime import datetime

router = Router()

class Case(StatesGroup):
    date = State()
    time = State()
    case = State()

@router.message(CommandStart())
async def start(message: Message):
    await rq.set_user(message.from_user.id, message.from_user.full_name)
    await message.answer('хз привет', reply_markup=kb.main)

@router.message(Command('help'))
async def help(message: Message):
    await message.answer('Сам себе помогай')

@router.message((F.text == 'Записать дело') or (Command('case')))
async def input(message: Message, state: FSMContext):
    await state.set_state(Case.date)
    await message.answer('Введите дату в формате "ГГГГ:ММ:ДД"')
@router.message(Case.date)
async def input_date(message: Message, state: FSMContext):
    await state.update_data(date=message.text)
    await state.set_state(Case.time)
    await message.answer('Введите время в формате "ЧЧ:ММ:СС"')
@router.message(Case.time)
async def input_time(message: Message, state: FSMContext):
    await state.update_data(time=message.text)
    await state.set_state(Case.case)
    await message.answer('Введите запланированное дело')
@router.message(Case.case)
async def input_case(message: Message, state: FSMContext):
    await state.update_data(case=message.text)
    data = await state.get_data()
    await rq.set_case(message.from_user.id, datetime.strptime(data["date"], '%Y:%m:%d').date(), datetime.strptime(data["time"], '%H:%M:%S'), data["case"])
    await message.answer(f'Дело успешно записано!\n{data["date"]}\n{data["time"]}\n{data["case"]}')
    await state.clear()
@router.message(F.text == 'Список дел' or Command('get_todays'))
async def get_today(message: Message):
    today = await rq.get_today_plans(message.from_user.id)
    await message.answer(f'Ваш список дел на сегодня:\n{today}')
