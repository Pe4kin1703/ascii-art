import imutils
import cv2
import socket, base64
from io import BytesIO
import numpy as np
import threading

HOST = 'localhost'
PORT = 6666

BUF = 65536

socket_list = []

def bytes_to_array(b: bytes) -> np.ndarray:
    np_bytes = BytesIO(b)
    return np.load(np_bytes, allow_pickle=True)
def bytes_to_array(b: bytes) -> np.ndarray:
    np_bytes = BytesIO(b)
    return np.load(np_bytes, allow_pickle=True)

def on_client(thread_name, socket_client):
    print(f"{thread_name}, {socket_client=}")
    while True:
        print("aboba")
        packet = socket_client.recv(BUF)
        data = base64.b64decode(packet,' /')
        npdata = np.frombuffer(data,dtype=np.uint8)
        frame = cv2.imdecode(npdata,1)
        cv2.imshow("RECEIVING VIDEO",frame)
        # try:
        #     for socket in socket_list:
        #         if socket!=socket_client:
        #             socket.send(packet)
        # except Exception as e:
        #     print(f"Unable to sent on socket:{socket}")
    # frame = cv2.putText(frame,'FPS: '+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
   



if __name__ == '__main__':

    socket_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_fd.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUF)
    socket_fd.bind((HOST, PORT))

    socket_fd.listen(10)

    

    sockfd, client_address = socket_fd.accept()
    while True:
        # Capture the current frame 
        
        print(f"Client {client_address=} was accepted, {sockfd=}")
        socket_list.append(sockfd)
        t = threading.Thread(name=f"THREAD{sockfd}", target=on_client, args=[f"THREAD{sockfd}" ,sockfd])
        # t.setDaemon(True)
        t.start()


        # packet = sockfd.recv(BUF)
        # data = base64.b64decode(packet,' /')
        # npdata = np.frombuffer(data,dtype=np.uint8)
        # frame = cv2.imdecode(npdata,1)
        # cv2.imshow("server VIDEO",frame)
        # # try:
        # #     for socket in socket_list:
        # #         if socket!=socket_client:
        # #             socket.send(packet)
        # # except Exception as e:
        # print(f"Unable to sent on socket:{socket}")
        
    # Detect if the Esc key has been pressed
        c = cv2.waitKey(1)
        if c == 27:
            break
    # Close all active windows
    cv2.destroyAllWindows()
