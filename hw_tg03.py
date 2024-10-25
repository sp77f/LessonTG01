import asyncio
from aiogram import Bot, Dispatcher, F ,types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import logging
from config import TOKEN
import sqlite3

logging.basicConfig(level=logging.INFO)
class Form(StatesGroup):
    name = State()
    age = State()
    grade = State()


bot = Bot(token=TOKEN)
dp = Dispatcher()
def init_db():
    conn = sqlite3.connect('school_data.db')
    cur = conn.cursor()
    print('База данных подключена')
    cur.execute("""CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        grade TEXT NOT NULL)
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
    await message.answer('В каком классе ты учишься ?')
    await state.set_state(Form.grade)

@dp.message(Form.grade)
async def grade(message: Message, state: FSMContext):
    await state.update_data(grade=message.text)
    user_data = await state.get_data()
    conn = sqlite3.connect('school_data.db')
    cur = conn.cursor()
    cur.execute("""
                        INSERT INTO students(name, age, grade) VALUES(?, ?, ?)""", (user_data['name'], user_data['age'], user_data['grade']))
    conn.commit()
    conn.close()
    await message.answer('Запись добавлена')
    conn = sqlite3.connect('school_data.db')
    cur = conn.cursor()
    cur.execute("""SELECT name, age FROM students WHERE grade = ?""", (user_data['grade'],))
    rows = cur.fetchall()
    conn.close()
    if rows:
        await message.answer('Список учеников в вашем классе:')
        for row in rows:
            await message.answer(f'Имя: {row[0]}, возраст: {row[1]}')
    else:
        await message.answer('Список пуст')
    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())