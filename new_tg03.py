import asyncio
from aiogram import Bot, Dispatcher, F ,types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import aiohttp
import logging
from config import TOKEN, WEATHER_TOKEN
import sqlite3

logging.basicConfig(level=logging.INFO)
class Form(StatesGroup):
    name = State()
    age = State()
    city = State()


bot = Bot(token=TOKEN)
dp = Dispatcher()
def init_db():
    conn = sqlite3.connect('bot.db')
    cur = conn.cursor()
    print('База данных подключена')
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        city TEXT NOT NULL)
        """)
    conn.commit()
    conn.close()

init_db()
@dp.message(Command('help'))
async def help(message: Message):
    await message.answer('Этот бот умеет выполнять команды:\n/start - приветствие \n/help - помощь ')
@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.answer('Привет! Как тебя зовут ?')
    await state.set_state(Form.name)

@dp.message(Form.name)
async def name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Сколько тебе лет ?')
    await state.set_state(Form.age)

@dp.message(Form.age)
async def age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer('В каком городе живете ?')
    await state.set_state(Form.city)

@dp.message(Form.city)
async def city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    user_data = await state.get_data()
    conn = sqlite3.connect('bot.db')
    cur = conn.cursor()
    cur.execute("""
                        INSERT INTO users(name, age, city) VALUES(?, ?, ?)""", (user_data['name'], user_data['age'], user_data['city']))
    conn.commit()
    conn.close()
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.openweathermap.org/data/2.5/weather?q={user_data["city"]}&appid={WEATHER_TOKEN}&units=metric&lang=ru') as response:
            if response.status == 200:
                data = await response.json()
                main = data['main']
                weather = data['weather'][0]
                temp = main['temp']
                humidity = main['humidity']
                description = weather['description']
                weaher_report = (f'Температура в городе {user_data["city"]} {temp} C \n влажность воздуха {humidity} % \n погода : {description}')
                await message.answer(weaher_report)
            else:
                await message.answer('Не получилось обработать запрос, попробуй еще раз!')

    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())