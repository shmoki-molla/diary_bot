from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
import app.keyboard as kb
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import app.database.requests as rq
from app.database.models import User, Case
from datetime import datetime
from app.classes import Case, Number, Number1, Day
from app.functions import convert_date

router = Router()



@router.message(CommandStart())
async def start(message: Message):
    await rq.set_user(message.from_user.id, message.from_user.full_name)
    await message.answer(f'Привет, {message.from_user.username}', reply_markup=kb.main)

@router.message(Command('help'))
async def help(message: Message):
    await message.answer(f'Это Бот-Ежедневник!\nС помощью кнопок на появившейся клавиатуре ты можешь управлять ботом)\n'
                         f'Главное вводи данные в том формате, в каком он просит!')

@router.message((F.text == 'Записать дело') or (Command('case')))
async def input(message: Message, state: FSMContext):
    await state.set_state(Case.date)
    await message.answer('Введите дату в формате "23 февраля"')
@router.message(Case.date)
async def input_date(message: Message, state: FSMContext):
    await state.update_data(date=convert_date(message.text))
    await state.set_state(Case.time)
    await message.answer('Введите время в формате "15:30"')
@router.message(Case.time)
async def input_time(message: Message, state: FSMContext):
    await state.update_data(time=f'{message.text}:00')
    await state.set_state(Case.case)
    await message.answer('Введите запланированное дело')
@router.message(Case.case)
async def input_case(message: Message, state: FSMContext):
    try:
        await state.update_data(case=message.text)
        data = await state.get_data()
        await rq.set_case(message.from_user.id, datetime.strptime(data["date"], '%Y:%m:%d').date(), datetime.strptime(data["time"], '%H:%M:%S'), data["case"])
        await message.answer(f'Дело успешно записано!\n{data["date"]}\n{data["time"]}\n{data["case"]}')
    except Exception:
        await message.answer('Некорректный ввод')
    await state.clear()
@router.message(F.text == 'Список дел' or Command('get_todays'))
async def day_choice(message: Message):
    await message.answer(f'Выберите день', reply_markup=await kb.plans_list())

@router.callback_query(F.data == 'today')
async def get_todays(callback: CallbackQuery):
    today = await rq.get_today_plans(callback.from_user.id)
    await callback.message.answer(f'Ваш список дел на сегодня:\n{today}', reply_markup= await kb.change_list())
@router.callback_query(F.data == 'another')
async def get_today(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Day.date)
    await callback.message.answer('Введите дату в формате "23 февраля"')

@router.message(Day.date)
async def set_day(message: Message, state: FSMContext):
    try:
        await state.update_data(date=convert_date(message.text))
        data = await state.get_data()
        today = await rq.get_plans(message.from_user.id, datetime.strptime(data["date"], '%Y:%m:%d').date())
        await message.answer(f'Ваш список дел на {data["date"]}:\n{today}', reply_markup= await kb.change_list())
    except Exception:
        await message.answer('Некорректный ввод')
    await state.clear()

@router.callback_query(F.data == 'delete')
async def delete1(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Number.number)
    await callback.message.answer('Напишите номер дела из списка без []')


@router.message(Number.number)
async def delete2(message: Message, state: FSMContext):
    try:
        await state.update_data(number=message.text)
        data = await state.get_data()
        success = await rq.delete_case(message.from_user.id, data["number"])
        await message.answer(success)
    except Exception:
        await message.answer('Некорректный ввод')
    await state.clear()

@router.callback_query(F.data == 'execute')
async def execute1(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Number1.number)
    await callback.message.answer('Напишите номер дела из списка без []')

@router.message(Number1.number)
async def execute2(message: Message, state: FSMContext):
    try:
        await state.update_data(number=message.text)
        data = await state.get_data()
        success = await rq.execute_case(message.from_user.id, data["number"])
        await message.answer(success)
    except Exception:
        await message.answer('Некорректный ввод')
    await state.clear()

@router.message(F.text == 'Мой прогресс')
async def progress(message: Message):
    data = await rq.get_successed(message.from_user.id)
    await message.answer(f'Вы уже выполнили немало дел!:\n{data}')

@router.message()
async def notify():
    await router.message.answer(f'Работает!!')


