import asyncio
from aiogram import Bot, Dispatcher, F ,types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile, CallbackQuery
from config import TOKEN
import keyboards as kb

bot = Bot(token=TOKEN)
dp = Dispatcher()



@dp.callback_query(F.data == 'Опция1')
async def hi_txt(call: types.CallbackQuery):
    await call.message.answer('Опция 1')

@dp.callback_query(F.data == 'Опция2')
async def bye_txt(call: types.CallbackQuery):
    await call.message.answer('Опция 2')
@dp.message(Command('help'))
async def help(message: Message):
    await message.answer('Этот бот умеет выполнять команды:\n'
                         '/start - приветствие \n'
                         '/help - помощь  \n'
                         '/links - список ссылок \n'
                         '/dynamic - динамическая клавиатура'   )
@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f'Выберите команду ! ',reply_markup=kb.main)

@dp.message(F.text == "Привет")
async def hitext(message: Message):
    await message.answer(f'Привет, {message.from_user.first_name} !')
@dp.message(F.text == "Пока")
async def byetext(message: Message):
    await message.answer(f'Пока, {message.from_user.first_name} !')

@dp.message(Command('links'))
async def cmd_start(message: Message):
    await message.answer(f'Выберите команду ! ',reply_markup=kb.inline_kb1)

@dp.message(Command('dynamic'))
async def cmd_start(message: Message):
    await message.answer(f'Выберите команду ! ',reply_markup=kb.inline_kb2)

@dp.callback_query(F.data == 'more_news')
async def more_news(call: types.CallbackQuery):
    await call.answer("Новости подгружаются")
    await call.message.edit_text('Вот свежие новости!', reply_markup=await kb.testbtn_keyboard())

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())