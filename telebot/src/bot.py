import uuid
import pika

import logging
import logging.config

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

from ImageMgr import ImageManager
from AsciiRpcClient import AsciiRpcClient
from UserMgr import UserManager


# import ascii-storage

class TgServer:
    def __init__(self):

        self.ascii_client = AsciiRpcClient()
        self.user_mgr = UserManager()

        self.premium_code = 'K27-clowns'

        logging.config.fileConfig(fname='/home/dspitsyn/KNU/ascii-art/telebot/src/logger.conf', disable_existing_loggers=False)
        self.logger = logging.getLogger(__name__)
        # self.accoun_client = AccountClient()

    def verify_premium_code(self, premium_code: str):
        return premium_code == self.premium_code

        

    def start(self, dp: Dispatcher):
        self.ascii_client.start()

        executor.start_polling(dp)
    
    async def process_photo(self, message: types.Message):
        if not (self.user_mgr.is_premium_user(message.from_user.id)):
            self.logger.info(f"User {message.chat.username} with id: {message.from_user.id} is non premium")
            if not self.user_mgr.is_non_premium_user_able_to_send_image(message.from_user.id):
                await bot.send_message(message.chat.id, text="Non premium users has only 1 attemps. We cannot process your image. Click on special button to enter secret code", reply_markup=main_kb)
                return 

        # self.logger.info(f"User {message.chat.username} with id: {message.from_user.id} is premium")

        image_mgr = ImageManager()
        image_mgr.create_photo_name(message)
        await image_mgr.download_image(message)

        await bot.send_document(message.chat.id, document=('text.txt', self.send_photo_to_ascii_server(image_mgr.get_photo_name()).encode('utf-8')))

    def send_photo_to_ascii_server(self, photo_name: str)->bytes:
        return self.ascii_client.call(photo_name)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

tg_server = TgServer()

button_help = KeyboardButton('Help')
# button_send = KeyboardButton('Send photo')
button_premium = KeyboardButton('Enter code to get premium access')

main_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
main_kb.row(button_help, button_premium)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Echo bot", reply_markup=main_kb)

@dp.message_handler(lambda message: message.text == 'Help')
@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await bot.send_message(message.chat.id, text="I\'ll repeat everything you say", reply_markup=main_kb)


# @dp.message_handler(lambda message: message.text == 'Send photo')
# @dp.message_handler(commands=['send'])
# async def process_help_command(message: types.Message):
#     await bot.send_message(message.chat.id, text="Later..", reply_markup=main_kb)



@dp.message_handler(lambda message: message.text == 'Enter code to get premium access')
# @dp.message_handler(commands=['send'])
async def process_code_button(message: types.Message):
    await bot.send_message(message.chat.id, text="Type '/code <code>'special code to get premium rights", reply_markup=main_kb)

@dp.message_handler(commands=['code'])
async def process_premium_code(message: types.Message):
    premium_code = message.get_args()
    tg_server.logger.info(f"User {message.chat.username} with id: {message.from_user.id} sent code: {premium_code=}")
    if not tg_server.verify_premium_code(premium_code):
        await bot.send_message(message.chat.id, text="Incorrectt secret code", reply_markup=main_kb)
        return
    tg_server.user_mgr.add_premium_user(message.from_user.id)
    await bot.send_message(message.chat.id, text="Congratulations! U have become premium user", reply_markup=main_kb)


@dp.message_handler(content_types=['photo'])
async def process_get_photo(message: types.Message):    

    await tg_server.process_photo(message=message)

    


    # photo_name = '/home/dspitsyn/ascii-db/'+ str(message.chat.username)+'/'+ str(message.message_id) + '.jpg'
    # # logger.warning(f"{photo_name=}")

    # tg_server.process_user_account(UserId)     // process_user_account(UserId) {account_client.send(user_id)}


    # await message.photo[-1].download(photo_name)
    # if(account_client.check_priv_user())
    #     ascii_client = AsciiRpcClient()
    #     response_file_name =  ascii_client.call(photo_name)
    # else:
    #     send ("Pay mone!!!!!!")
    




    # Process_photo.process(photo_name)
    # process (...):
    # ....
    # Sendphoto(...) {client.call}
    # ....
    # logger.warning(f"ABOBA {response_file_name.encode('utf-8')=}")

    # try:
    #     # with open(photo_name, "rb") as image:
    #     #     binary = enc64(image.read()) #encoding image to base64
    #     #     os.remove(photo_name)
    #     #     await bot.send_message(message.chat.id, text="I've converted this image to Base64")
    #     #     img = BytesIO(dec64(binary)) #decoding image from base64
    #     #     img.name = "image.jpeg"
    #     #     img.seek(0)
    #     #     await bot.send_photo(chat_id=message.chat.id, photo=img, caption="Decoded image") #sending image
    # except:
    #     await bot.send_message(message.chat.id, text="Error while converting or decoding")
    #     return

# @dp.message_handler()
# async def echo_message(message: types.Message):
#     await bot.send_message(message.chat.id, text=message.text, reply_markup=main_kb)

if __name__ == '__main__':

    tg_server.logger.info("Bot has started")
    tg_server.logger.debug("Bot has started")
    tg_server.start(dp)
    