from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Записать дело')],
                                     [KeyboardButton(text='Список дел')],
                                     [KeyboardButton(text='Настроить напоминалку')]],
                           resize_keyboard=True, input_field_placeholder='Выберите пункт меню...')
