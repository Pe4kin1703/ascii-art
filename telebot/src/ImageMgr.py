from aiogram import Bot, types
import logging
import logging.config

class ImageManager(object):
    def __init__(self) -> None:
        self.photo_name = None 
        # logging.config.fileConfig(fname='logger.conf', disable_existing_loggers=False)
        self.logger = logging.getLogger(__class__.__name__)

    def create_photo_name(self, message: types.Message)-> str:
        self.photo_name = '/home/dspitsyn/ascii-db/'+ str(message.chat.username)+'/'+ str(message.message_id) + '.jpg'
        return self.photo_name

    async def download_image(self, message: types.Message):
        self.logger.info("Dowloading image from user: ")
        await message.photo[-1].download(self.photo_name)
    
    def get_photo_name(self):
        return self.photo_name