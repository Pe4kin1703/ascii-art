import socket
import pika
import uuid
import argparse
import ascii_storage
import base64


class AsciiRpcClient(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(queue=self.callback_queue,
                                   on_message_callback=self.on_response,
                                   auto_ack=True)
        self.response = None
        self.correlation_id = None

    def on_response(self, ch, method, props, body):
        print("Getting response")
        print(f"Comparing crrelation ids: {self.correlation_id=}, {props.correlation_id}")
        if self.correlation_id == props.correlation_id:
            print(f"Body: {body=}")
            self.response = body.decode("utf-8")

    def call(self, image_path : str, image_in_bytes: bytes):
        print(f"Doing call for image:{image_path=}")
        self.response = None
        self.correlation_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.correlation_id,
            ),
            body=image_in_bytes
        )
        self.connection.process_data_events(time_limit=None)
        return self.response


parser = argparse.ArgumentParser(description='Pass image to program')
parser.add_argument('--path', type=str, default=None, help='Image path')
args = parser.parse_args()



image_path = args.path
print(f"{image_path=}")
client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("connecting socket")
# client_sock.connect(('localhost', 1703))


with open(image_path, 'rb') as file:
    image_data = file.read()
    b = bytes(image_data)
    # b.append(bytes('s'))
    # print(f"bytes {b}")

# byte_arr = bytearray(b)
# print(f"{type(byte_arr)} ")

ascii_rpc = AsciiRpcClient()



response = ascii_rpc.call(image_path, b)

print("Response:")
print(response)
print(f"response type {type(response)}")
with open ('client.txt', 'w') as client_file:
    client_file.write(response)


# while image_data:
#     print("Sending image in binary format")
#     client_sock.send(image_data)
#     image_data = file.read(2048)
#
# file.close()
# client_sock.close()