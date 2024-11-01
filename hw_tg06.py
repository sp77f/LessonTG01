import asyncio
from aiogram import Bot, Dispatcher, F ,types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from aiogram. fsm. context import FSMContext
from aiogram. fsm.state import State, StatesGroup
from aiogram. fsm. storage. memory import MemoryStorage
from config import TOKEN
import random
import requests
import sqlite3
import aiohttp
import logging
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

bot = Bot(token=TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)
button_exchange_rates = KeyboardButton(text='Курс валют')
button_registr = KeyboardButton(text='Регистрация в ТГ боте')
button_tips = KeyboardButton(text="Советы по экономии")
button_finances = KeyboardButton(text="Личные финансы")
keyboard = ReplyKeyboardMarkup(keyboard=[
    [button_registr, button_exchange_rates],
    [button_tips, button_finances]
], resize_keyboard=True)

conn = sqlite3.connect('users.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER UNIQUE,
    name TEXT,
    category1 TEXT,
    category2 TEXT,
    category3 TEXT,    
    expenses1 REAL,
    expenses2 REAL,
    expenses3 REAL)
    """)
conn.commit()


class FinancesForm(StatesGroup):
    category1 = State()
    expenses1 = State()
    category2 = State()
    expenses2 = State()
    category3 = State()
    expenses3 = State()
@dp.message(Command('help'))
async def help(message: Message):
    await message.answer('Этот бот умеет выполнять команды:\n'
                         '/start - приветствие \n'
                         '/help - помощь \n \n'
                         'Основной функционал - показ случайной картинки в зависимости от нажатой кнопки и ответа Да или Нет\n\n'
                         'Также введя любое слово русском языке вы получите его перевод на французский')
@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f'Привет ! Я ваш личный финансовый бот. Выберите одну из опций в меню ',reply_markup=keyboard)

@dp.message(F.text == "Регистрация в ТГ боте")
async def registration(message: Message):
    telegram_id= message.from_user.id
    name = message.from_user.full_name
    cur.execute('''SELECT * FROM users WHERE telegram_id = ?''', (telegram_id, ))
    user = cur.fetchone()
    if user:
        await message.answer('Вы уже зарегистрированы')
    else:
        cur.execute('''INSERT INTO users(telegram_id, name) VALUES(?, ?)''', (telegram_id, name))
        conn.commit()
        await message.answer('Вы успешно зарегистрированы!')
@dp.message(F.text == "Курс валют")
async def exchange_rates(message: Message):
    url = "https://v6.exchangerate-api.com/v6/09edf8b2bb246e1f801cbfba/latest/USD"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code != 200:
            await message.answer(f"Не удалось получить курс валют")
            return
        usd_to_rub = data["conversion_rates"]["RUB"]
        eur_to_usd = data["conversion_rates"]["EUR"]
        eur_to_rub = eur_to_usd * usd_to_rub
        await message.answer(f"1 USD = {usd_to_rub:.2f} RUB\n"
                             f"1 EUR = {eur_to_rub:.2f} RUB")
    except Exception as e:
        await message.answer(f"произошла ошибка {e}")
@dp.message(F.text == "Советы по экономии")
async def see_tips(message: Message):
    tips = [
        "Совет 1: Ведите бюджет и следите за своими расходами.",
        "Совет 2: Откладывайте часть доходов на сбережения.",
        "Совет 3: Покупайте товары по скидкам и распродажам."
    ]
    tip = random.choice(tips)
    await message.answer(tip)
@dp.message(F.text == "Личные финансы")
async def finances(message: Message, state: FSMContext):
    await state.set_state(FinancesForm.category1)
    await message.answer("Введите первую категорию расходов:")
@dp.message(FinancesForm.category1)
async def finances(message: Message, state: FSMContext):
    await state.update_data(category1=message.text)
    await state.set_state(FinancesForm.expenses1)
    await message.answer("Введите расходы для этой категории:")
@dp.message(FinancesForm.expenses1)
async def finances(message: Message, state: FSMContext):
    await state.update_data(expenses1=float(message.text))
    await state.set_state(FinancesForm.category2)
    await message.answer("Введите вторую категорию расходов:")

@dp.message(FinancesForm.category2)
async def finances(message: Message, state: FSMContext):
    await state.update_data(category2=message.text)
    await state.set_state(FinancesForm.expenses2)
    await message.answer("Введите расходы для этой категории:")
@dp.message(FinancesForm.expenses2)
async def finances(message: Message, state: FSMContext):
    await state.update_data(expenses2=float(message.text))
    await state.set_state(FinancesForm.category3)
    await message.answer("Введите третью категорию расходов:")


@dp.message(FinancesForm.category3)
async def finances(message: Message, state: FSMContext):
    await state.update_data(category3=message.text)
    await state.set_state(FinancesForm.expenses3)
    await message.answer("Введите расходы для этой категории:")
@dp.message(FinancesForm.expenses3)
async def finances(message: Message, state: FSMContext):
    data = await state.get_data()
    telegram_id = message.from_user.id
    cur.execute('''UPDATE users SET category1 = ?, expenses1 = ?, category2 = ?, expenses2 = ?, category3 = ?, expenses3 = ? WHERE telegram_id = ?''',(
        data['category1'], data['expenses1'], data['category2'], data['expenses2'], data['category3'], float(message.text), telegram_id))
    conn.commit()
    await message.answer("Данные сохранены")
    await state.clear()
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())