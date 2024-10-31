import asyncio
from aiogram import Bot, Dispatcher, F ,types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile, CallbackQuery
from config import TOKEN, NASA_API_KEY
import random
import requests
from  datetime import datetime, timedelta

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer('Этот бот умеет показывать картинки с сайта NASA\n')
@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f'Привет ! Набери название породы кошки на английском языке и я пришлю фото и описание\n')

def get_random_apod():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    random_date = start_date + (end_date - start_date) * random.random()
    random_date_str = random_date.strftime('%Y-%m-%d')
    url = f'https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}&date={random_date_str}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
@dp.message(Command('random_apod'))
async def random_apod(message: Message):
    apod = get_random_apod()
    if apod:
        photo_url = apod['url']
        title = apod['title']
        await message.answer_photo(apod['url'], caption=apod['title'])
    else:
        await message.answer('Что то пошло не так ')
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())