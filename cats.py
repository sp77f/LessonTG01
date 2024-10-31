import asyncio
from aiogram import Bot, Dispatcher, F ,types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile, CallbackQuery
from config import TOKEN, THE_CAT_API
import random
import requests

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer('Этот бот умеет выполнять команды:\n'
                         '/start - приветствие \n'
                         '/help - помощь  \n'
                         '/links - список ссылок \n'
                         '/dynamic - динамическая клавиатура'   )
@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f'Привет ! Набери название породы кошки на английском языке и я пришлю фото и описание\n')

@dp.message()
async def get_text(message: Message):
    breed_name = message.text
    breed_info = get_breed_info(breed_name)
    if breed_info != None:
        image_url = get_cat_image(breed_info['id'])
        info = (f'Порода: {breed_info["name"]}\n'
                f'Описание: {breed_info["description"]}\n'
                f'Продолжительность жизни: {breed_info["life_span"]} лет\n')
        await message.answer_photo(photo=image_url, caption=info)
    else:
        await message.answer('Порода не нашлась , попробуйте ещё раз')

def get_cat_breeds():
    url = 'https://api.thecatapi.com/v1/breeds'
    headers = {'x-api-key': THE_CAT_API}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None
def get_cat_image(breed_id):
    url = f'https://api.thecatapi.com/v1/images/search?breed_id={breed_id}'
    headers = {'x-api-key': THE_CAT_API}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()[0]['url']
    else:
        return None
def get_breed_info(breed_name):
    breeds = get_cat_breeds()
    if breeds != None:
        for breed in breeds:
            if breed['name'] == breed_name:
                return breed
    else:
        return None


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())