# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from asyncio.log import logger
from nis import cat
import time

from PIL import Image
import numpy as np
import math
import socket
import pika

import logging
import logging.config

logging.config.fileConfig(fname='/usr/src/app/logger.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

# ASCII_GRADIENT = ["Ñ" ,"@", "#", "W", "$", "9", "8", "7", "6", "5", "4", "3", "2", "1", "0", "?", "!", "a", "b", "c", ";", ":", "+", "="," -", ",", ".","_", " "]
ASXII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", ".", " "]

new_width = 500

def resize_image(image):
    width, height = image.size
    ratio = height/width/1.65
    new_height = int(new_width * ratio)
    resized_image = image.resize((new_width, new_height))
    return resized_image

def image_to_ascii(image):
    pixels = image.getdata()
    # ASCII_GRADIENT.reverse()
    # ASXII_CHARS.reverse()
    kf = math.ceil(256 / len(ASXII_CHARS))
    # kf = math.ceil(256 / len(ASCII_GRADIENT))
    characters = "".join(ASXII_CHARS[math.floor(pixel / kf)] for pixel in pixels)
    # characters = "".join(ASCII_GRADIENT[math.floor(pixel / kf)] for pixel in pixels)
    return characters

def get_image_from_socket():
    sockFd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logger.info("Binding socket")
    sockFd.bind(('localhost', 1703))
    sockFd.listen()

    logger.info("Accepting client")
    client_sock, client_adress = sockFd.accept()
    logger.info("Client has accepted succesfully")
    file = open('server_img.jpg', "wb")

    image_chunk = client_sock.recv(2048)
    while image_chunk:
        file.write(image_chunk)
        logger.info("Reading data from socket")
        image_chunk = client_sock.recv(2048)
    file.close()
    client_sock.close()

def do_stuff(image_name:str):
    """
    Needed to do all job and return text file in byte type
    :param image_bytes:
    :return:
    """
    # logger.info("Do stuff started")
    # with open('file.jpg', 'wb') as binary_file:
    #     binary_file.write(image_bytes)

    working_directory = image_name[:image_name.rfind('/')]
    photo_name = image_name[image_name.rfind('/')+1:image_name.rfind('.')]
    logger.info(f"{working_directory=}")
    logger.info(f"{photo_name=}")
    try:
        image = Image.open(image_name).convert('L')
    except:
        error = "File do not exist"
        logger.info(error)
        raise (error)

    image_string = image_to_ascii(resize_image(image))
    pixels = len(image_string)
    ascii_image = "\n".join(image_string[i:(i+new_width)] for i in range(0, pixels, new_width))

    text_file = working_directory + '/' + photo_name + '.txt'
    logger.info(f"{text_file=}")

    with open(text_file, 'w') as f:
        f.write(ascii_image)

    logger.info("logger.infoing ascii image:")
    logger.info(ascii_image)
    # logger.info(len(image.getdata()))

    return ascii_image




def on_request(ch, method, props, body):
    logger.info("on_request begin")
    logger.info(f"Working on request with {props.correlation_id=}")
    image_name_binary = body

    try:
        response = do_stuff(image_name_binary.decode('utf-8'))    
    except:
        logger.info(f"Error:")
        return 

    

    # time.sleep(60)

    ch.basic_publish(
        exchange='',
        routing_key=props.reply_to,
        properties=pika.BasicProperties(correlation_id=props.correlation_id),
        body=bytes(response, 'utf-8')
    )

    ch.basic_ack(delivery_tag=method.delivery_tag)



if __name__ == '__main__':

    
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq')) #ascii-project-net
    channel = connection.channel()

    channel.queue_declare(queue='rpc_queue')

    channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)
    # channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)

    logger.info(" [x] Awaiting RPC requests")
    channel.start_consuming()






    # get_image_from_socket()
    # image_name = "pain-nartuto.jpg"
    # image = Image.open('images/eifel-tower.jpg').convert('L')
    # image_string = image_to_ascii(resize_image(image))
    # pixels = len(image_string)
    # ascii_image = "\n".join(image_string[i:(i+new_width)] for i in range(0, pixels, new_width))
    #
    # logger.info(ascii_image)
    # # logger.info(len(image.getdata()))
    # with open("image.txt", "w")  as f:
    #     f.write(ascii_image)


    # image = Image.fromarray(image_ar)
    # image.save('images/1.jpg')
    # logger.info(image.shape)o

