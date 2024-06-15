from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Записать дело')],
                                     [KeyboardButton(text='Список дел')],
                                     [KeyboardButton(text='Мой прогресс')]],
                           resize_keyboard=True, input_field_placeholder='Выберите пункт меню...')
async def plans_list():
    list_plans = InlineKeyboardBuilder()
    list_plans.add(InlineKeyboardButton(text='На сегодня', callback_data='today'))
    list_plans.add(InlineKeyboardButton(text='На другой день', callback_data='another'))
    return list_plans.adjust(1).as_markup()

async def change_list():
    changed_list = InlineKeyboardBuilder()
    changed_list.add(InlineKeyboardButton(text='Удалить дело', callback_data='delete'))
    changed_list.add(InlineKeyboardButton(text='Отметить выполненное', callback_data='execute'))
    return changed_list.adjust(1).as_markup()