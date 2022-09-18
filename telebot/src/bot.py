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

# import ascii-storage

help_message = "Hi!👋 I\'m ASCII-Art bot. You can send me any image and I\'ll create an ASCII Art.\nℹ️For other information press buttons below"
greetings_message = "Hi!👋 I\'m ASCII-Art bot. You can send me any image and I\'ll create an ASCII Art.\nℹ️For other information press \"Help\" button "
class AsciiRpcClient(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(queue=self.callback_queue,
                                    on_message_callback=self.on_response)
        self.response = None
        self.correlation_id = None

    def on_response(self, ch, method, props, body):
        logger.debug("Getting response")
        logger.debug(f"Comparing crrelation ids: {self.correlation_id=}, {props.correlation_id}")
        if self.correlation_id == props.correlation_id:
            logger.debug(f"Body: {body=}")
            self.response = body.decode("utf-8")
            ch.basic_ack(delivery_tag=method.delivery_tag)

    def call(self, image_path: str):
        logger.debug(f"Doing call for image:{image_path=}")
        self.response = None
        self.correlation_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.correlation_id,
            ),
            body=bytearray(image_path, 'utf-8')
        )
        self.connection.process_data_events(time_limit=None)
        return self.response


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

button_help = KeyboardButton('**Help**ℹ️')
button_send = KeyboardButton('Send photo')

main_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
main_kb.row(button_help, button_send)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Ascii Art Bot", reply_markup=main_kb)

@dp.message_handler(lambda message: message.text == '**Help**ℹ️')
@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await bot.send_message(message.chat.id, text=help_message, reply_markup=main_kb)

@dp.message_handler(lambda message: message.text == 'Send photo')
@dp.message_handler(commands=['send'])
async def process_photo_command(message: types.Message):
    await bot.send_message(message.chat.id, text="Later..", reply_markup=main_kb)

@dp.message_handler(content_types=['photo'])
async def process_get_photo(message: types.Message):
    await bot.send_message(message.chat.id, text="Бот прийняв Іслам. Діма поки грається з ним, тому ascii артов не буде)()(()))", reply_markup=main_kb)
    return
    photo_name = '/home/dspitsyn/ascii-db/'+ str(message.chat.username)+'/'+ str(message.message_id) + '.jpg'
    # logger.warning(f"{photo_name=}")
    await message.photo[-1].download(photo_name)
    ascii_client = AsciiRpcClient()
    response_file_name = ascii_client.call(photo_name)
    # logger.warning(f"ABOBA {response_file_name.encode('utf-8')=}")

    await bot.send_document(message.chat.id, document=('text.txt', response_file_name.encode('utf-8')))
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

@dp.message_handler()
async def echo_message(message: types.Message):
    await bot.send_message(message.chat.id, text="Бот прийняв Іслам. Діма поки грається з ним, тому ascii артов не буде)()(()))", reply_markup=main_kb)

if __name__ == '__main__':
    logging.config.fileConfig(fname='logger.conf', disable_existing_loggers=False)
    logger = logging.getLogger(__name__)
    logger.info("Bot has started")
    logger.debug("Bot has started")
    executor.start_polling(dp)