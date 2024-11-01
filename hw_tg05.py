import asyncio
from aiogram import Bot, Dispatcher, F ,types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile, CallbackQuery
from config import TOKEN
import random
import requests
from googletrans import Translator , LANGUAGES
import keyboards as kb

bot = Bot(token=TOKEN)
dp = Dispatcher()
translator = Translator()

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer('Этот бот умеет выполнять команды:\n'
                         '/start - приветствие \n'
                         '/help - помощь \n \n'
                         'Основной функционал - показ случайной картинки в зависимости от нажатой кнопки и ответа Да или Нет\n\n'
                         'Также введя любое слово русском языке вы получите его перевод на французский')
@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f'Привет ! Это забавный бот для подбора картинок для ответов Да или Нет ',reply_markup=kb.main)

@dp.message(F.text == "Да")
async def hitext(message: Message):
    url = get_image('yes')
    await bot.send_animation(chat_id=message.chat.id, animation=url)
@dp.message(F.text == "Нет")
async def hitext(message: Message):
    url = get_image('no')
    await bot.send_animation(chat_id=message.chat.id, animation=url)

def get_image(answer):
    url = f"https://yesno.wtf/api?force={answer}"
    response = requests.get(url).json()
    image_url = response['image']
    return image_url

@dp.message()
async def any(message: Message):
    user_text = message.text
    trans = translator.translate(user_text, dest='fr')
    print(trans.text)
    await message.reply(trans.text)
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())