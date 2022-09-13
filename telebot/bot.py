from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, message
from config import TOKEN


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

button_help = KeyboardButton('Help')
button_send = KeyboardButton('Send photo')

main_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
main_kb.row(button_help, button_send)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Echo bot", reply_markup=main_kb)

@dp.message_handler(lambda message: message.text == 'Help')
@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await bot.send_message(message.chat.id, text="I\'ll repeat everything you say", reply_markup=main_kb)

@dp.message_handler(lambda message: message.text == 'Send photo')
@dp.message_handler(commands=['send'])
async def process_help_command(message: types.Message):
    await bot.send_message(message.chat.id, text="Later..", reply_markup=main_kb)

@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.chat.id, text=msg.text, reply_markup=main_kb)

if __name__ == '__main__':
    executor.start_polling(dp)