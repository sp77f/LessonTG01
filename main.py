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

@dp.message(F.photo)
async def react_photo(message: Message):
    list = ['Непонятно, что это такое, но я сохраню','Ого, какая фотка! Я сохраню!','Не отправляй мне такое больше, но я сохраню']
    rand_answ = random.choice(list)
    await message.answer(rand_answ)
    await bot.download(message.photo[-1], destination=f'img/{message.photo[-1].file_id}.jpg')

@dp.message(Command('photo'))
async def photo(message: Message):
    list = ['https://avatars.mds.yandex.net/i?id=b0ba90823baf23828cb69a435ab6e0c9bfeb2060-5576459-images-thumbs&n=13',
            'https://avatars.mds.yandex.net/i?id=37c77790bf6456e39343eb63d6ad5ffe97b39d2e-12143639-images-thumbs&n=13',
            'https://avatars.mds.yandex.net/i?id=6fd8bbedaddc3bb13b627d2227782496a597b26b94575119-12421722-images-thumbs&n=13'
            ]
    rand_photo = random.choice(list)
    await message.answer_photo(photo=rand_photo, caption='Это супер крутая картинка')

@dp.message(F.text == "Помощь")
async def test_b(message: Message):
    await message.answer('Обработка кнопки Помощь')

@dp.callback_query(F.data == 'hi_text')
async def news(call: types.CallbackQuery):
    await call.message.answer('Привет, ' + call.from_user.first_name+ '!')

@dp.callback_query(F.data == 'bye_text')
async def news(call: types.CallbackQuery):
    await call.message.answer('Пока, ' + call.from_user.first_name + '!')
@dp.message(Command('help'))
async def help(message: Message):
    await message.answer('Этот бот умеет выполнять команды:\n/start - приветствие \n/help - помощь  \n/weather - погода в Москве')
@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f'Выберите команду ! ',reply_markup=kb.main)

@dp.message(F.text == "Привет")
async def hitext(message: Message):
    await message.answer(f'Привет, {message.from_user.first_name} !')
@dp.message(F.text == "Пока")
async def hitext(message: Message):
    await message.answer(f'Пока, {message.from_user.first_name} !')
@dp.message(F.text == "что такое ИИ?")
async def aitext(message: Message):
    await message.answer('Искусственный интеллект — это свойство искусственных интеллектуальных систем выполнять творческие функции, которые традиционно считаются прерогативой человека; наука и технология создания интеллектуальных машин, особенно интеллектуальных компьютерных программ')

@dp.message(Command('weather'))
async def get_weather(message: Message):
    api_key = "dd343a5a6aac6ea5f3e12424decba11c"
    city = 'Moscow'
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&lang=ru&appid={api_key}"
    response = requests.get(url).json()
    await message.answer(f'Температура в городе {city} {response["main"]["temp"]} C \n погода : {response["weather"][0]["description"]}')

@dp.message(Command('voice'))
async def voice(message: Message):
    voice = FSInputFile('woman.ogg')
    await message.answer_voice(voice)
@dp.message()
async def any(message: Message):
    user_text = message.text
    trans = translator.translate(user_text, dest='en')
    print(trans.text)
    await message.reply(trans.text)
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())