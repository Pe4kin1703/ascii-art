import pika
import uuid

import logging
import logging.config

class AsciiRpcClient(object):

    def __init__(self):
        self.host = 'localhost'

        self.connection = None
        self.channel = None
        self.response = None
        self.correlation_id = None
        self.callback_queue = None

        logging.config.fileConfig(fname='logger.conf', disable_existing_loggers=False)
        self.logger = logging.getLogger(__name__)

    def start(self):
        self.logger.info(f"Creating server on host: {self.host}")
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host)
        )
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.response = None
        self.correlation_id = None

    def on_response(self, ch, method, props, body):
        self.logger.debug("Getting response")
        self.logger.debug(f"Comparing crrelation ids: {self.correlation_id=}, {props.correlation_id}")
        if self.correlation_id == props.correlation_id:
            self.logger.debug(f"Body: {body=}")
            self.response = body.decode("utf-8")
            ch.basic_ack(delivery_tag=method.delivery_tag)

    def call(self, image_path: str) -> bytearray:
        self.logger.debug(f"Doing call for image:{image_path=}")
        self.response = None
        self.correlation_id = str(uuid.uuid4())
        self.channel.basic_consume(queue=self.callback_queue,
                                   on_message_callback=self.on_response)
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
