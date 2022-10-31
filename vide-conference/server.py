from traceback import print_tb
from py import process
import imutils
import cv2
import socket, base64
from io import BytesIO
import numpy as np
import threading
import argparse
import asyncio

HOST = 'localhost'
PORT = 6666

BUF = 65536

loop = asyncio.get_event_loop()
loop1 = asyncio.get_event_loop()

client_list = set()

def bytes_to_array(b: bytes) -> np.ndarray:
    np_bytes = BytesIO(b)
    return np.load(np_bytes, allow_pickle=True)
def bytes_to_array(b: bytes) -> np.ndarray:
    np_bytes = BytesIO(b)
    return np.load(np_bytes, allow_pickle=True)
    
def on_client(thread_name, packet, client_addr):
    # print(f"{thread_name}, {socket_client=}")
   
    print("aboba")
    data = base64.b64decode(packet,' /')
    npdata = np.frombuffer(data,dtype=np.uint8)
    frame = cv2.imdecode(npdata,1)
    cv2.imshow(f"RECEIVING VIDEO {thread_name}",frame)
        # try:
        #     for socket in socket_list:
        #         if socket!=socket_client:
        #             socket.send(packet)
        # except Exception as e:
        #     print(f"Unable to sent on socket:{socket}")
    # frame = cv2.putText(frame,'FPS: '+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
   

def procces_packet(socket_fd):
    print("Procces packet")
    i = 0
    while True:
        # Capture the current frame 
        # sockfd, client_address = socket_fd.accept()

        # print(f"Client {client_address=} was accepted, {sockfd=}")
        # socket_list.append(sockfd)
        # t = threading.Thread(name=f"THREAD{sockfd}", target=on_client, args=[f"THREAD{sockfd}" ,sockfd])
        # # t.setDaemon(True)
        # t.start()

        print("Waiting for data from user")
        packet,client_addr = socket_fd.recvfrom(BUF)
        packet1 = packet
        print(f"{client_addr[0]=}, {client_addr[1]=}")

        client_addr_return = (client_addr[0], 7666)
        # client_addr_return[1] = 7666
        if client_addr_return not in client_list:
            client_list.add(client_addr_return)
        else:
            if i ==0:
                client_list.add((client_addr[0], 7667))
            i+=1
        print(f"{client_list=}")
            

        print("Data has been recieved")
        data = base64.b64decode(packet,' /')
        npdata = np.frombuffer(data,dtype=np.uint8)
        frame = cv2.imdecode(npdata,1)
        cv2.imshow(f"RECEIVING VIDEO {client_addr}",frame)

        for client in client_list:
            if client != client_addr:
                print(f"Sending video back {client=}")
                print(f"{(packet==packet1)=}")
                socket_fd.sendto(packet, client)
    # Detect if the Esc key has been pressed
        c = cv2.waitKey(1)
        if c == 27:
            break
    # Close all active windows
    cv2.destroyAllWindows()


if __name__ == '__main__':



    socket_fd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_fd.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUF)
    socket_fd.bind((HOST, PORT))
    
    

    # socket_fd.listen(10)

    # sockfd, client_address = socket_fd.accept()
    # msg,client_addr = socket_fd.recvfrom(BUF)
    # print('GOT connection from ',client_addr)
    # if loop1.is_running:
    #     loop1.stop()
    # t = threading.Thread( target=lambda: loop1.run_forever())
    # t.setDaemon(True)
    # t.start()

    # print("create task")
    # task = loop.create_task(procces_packet(socket_fd))
    # loop.run_forever()
    procces_packet(socket_fd)
    # asyncio.run(procces_packet(socket_fd))
   

    
