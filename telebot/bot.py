from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, message
import PIL.Image as Image
import io
from io import BytesIO
import os
from base64 import b64encode as enc64
from base64 import b64decode as dec64
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

@dp.message_handler(content_types=['photo'])
async def process_get_photo(message: types.Message):
    photo_name = str(message.message_id) + '.jpg'
    await message.photo[-1].download(photo_name)
    try:
        with open(photo_name, "rb") as image:
            binary = enc64(image.read()) #encoding image to base64
            os.remove(photo_name)
            await bot.send_message(message.chat.id, text="I've converted this image to Base64")
            img = BytesIO(dec64(binary)) #decoding image from base64
            img.name = "image.jpeg"
            img.seek(0)
            await bot.send_photo(chat_id=message.chat.id, photo=img, caption="Decoded image") #sending image
    except:
        await bot.send_message(message.chat.id, text="Error while converting or decoding")
        return

@dp.message_handler()
async def echo_message(message: types.Message):
    await bot.send_message(message.chat.id, text=message.text, reply_markup=main_kb)

if __name__ == '__main__':
    executor.start_polling(dp)