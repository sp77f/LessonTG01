from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Да'), KeyboardButton(text='Нет')]],
    resize_keyboard=True)

inline_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Привет ', callback_data='hi_text')],
    [InlineKeyboardButton(text='Пока', callback_data='bye_text')]
])

inline_kb1 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Новости ', url='https://www.rbc.ru/')],
    [InlineKeyboardButton(text='Музыка', url='https://music.yandex.ru/home')],
    [InlineKeyboardButton(text='Видео', url='https://www.rutube.ru/')],
])
inline_kb2 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Показать больше ', callback_data='more_news')]
])

test = ["кнопка1","кнопка2","кнопка3","кнопка4"]

async def test_keyboard():
    keyboard = ReplyKeyboardBuilder()
    for key in test:
        keyboard.add(KeyboardButton(text=key))
    return keyboard.adjust(2).as_markup()

test_btn = ["Опция1","Опция2"]
async def testbtn_keyboard():
    keyboard = InlineKeyboardBuilder()
    for key in test_btn:
        keyboard.add(InlineKeyboardButton(text=key, callback_data=key))
    return keyboard.adjust(2).as_markup()