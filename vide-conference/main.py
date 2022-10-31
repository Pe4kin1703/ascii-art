import imp
from ipaddress import ip_address
import threading
from tkinter import E
from traceback import print_tb
import cv2
import socket, imutils, base64
from io import BytesIO
import numpy as np
import argparse
import time
import threading
from multiprocessing import Process,  Pool
from multiprocessing.pool import AsyncResult
import os

#Initialize video capture

parser = argparse.ArgumentParser()

parser.add_argument('--file-name', required=True)

opt = parser.parse_args()

file_name = opt.file_name
print(f"{file_name=}")

WIDTH = 400
cap = cv2.VideoCapture(file_name)
#scaling factor
scaling_factor = 0.5
# Loop until you hit the Esc key

BUF = 65435


HOST = '146.70.46.20'
HOST1 = 'localhost'
PORT = 6666

PORT_RETURN = 7666

socket_fd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_fd.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, BUF)
print("Connecting...")
socket_fd.connect((HOST1, PORT))
print("Cinnected")


# socket_return.settimeout(0.03)

def array_to_bytes(x: np.ndarray) -> bytes:
    np_bytes = BytesIO()
    np.save(np_bytes, x, allow_pickle=True)
    return np_bytes.getvalue()

def return_trafic():
    socket_return = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_return.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUF)
    print(f"Binding return socket{(HOST1, PORT_RETURN)=}")
    try:
        socket_return.bind((HOST1, PORT_RETURN))
    except Exception as e:
        print(f"Error:{e}")
        print(f"Binding return socket{(HOST1, PORT_RETURN+1)=}")
        socket_return.bind((HOST1, PORT_RETURN+1))
        # Capture the current frame 
        # sockfd, client_address = socket_fd.accept()

        # print(f"Client {client_address=} was accepted, {sockfd=}")
        # socket_list.append(sockfd)
        # t = threading.Thread(name=f"THREAD{sockfd}", target=on_client, args=[f"THREAD{sockfd}" ,sockfd])
        # # t.setDaemon(True)
        # t.start()
    while True:

        print("Waiting for data from server")
        packet,client_addr = socket_return.recvfrom(BUF)
       
        data = base64.b64decode(packet,' /')
        npdata = np.frombuffer(data,dtype=np.uint8)
        frame = cv2.imdecode(npdata,1)
        print("Showing recieved image")
        cv2.imshow(f"FROM{socket_return}",frame)
        c = cv2.waitKey(1)
        if c == 27:
            break
    cap.release()
            
        # 
        # Close all active windows
    cv2.destroyAllWindows()

            # print(f"{client_addr[0]=}, {client_addr[1]=}")

            # client_addr_return = client_addr
            # client_addr_return[1] = 7666
            # if client_addr_return not in client_list:
            #     client_list.append(client_addr_return)

    

def procces_video():
    while True:
    #     print("Reading video frame")
    #     # cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
        
        ret, frame = cap.read()
        print("Frame has been read")
        frame = imutils.resize(frame,width=WIDTH)
    #     
        encoded, buffer = cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY,80])
        message = base64.b64encode(buffer)
        print("Sending message")
        socket_fd.sendto(message[:BUF-100], (HOST1, PORT))
        print("Sleeping")
        time.sleep(0.03)
        cv2.imshow('TRANSMITTING VIDEO',frame)

        # cv2.imshow('TRANSMITTING VIDEO',frame)
    # Detect if the Esc key has been pressed
        c = cv2.waitKey(1)
        if c == 27:
            break
    # Release the video capture object
    cap.release()
    # Close all active windows
    cv2.destroyAllWindows()
        
            # time.sleep(float(0.03))
            # time.sleep(0.0002)

            # packet,server_addr = socket_fd.recvfrom(BUF)
            # if packet is not None:
            #     data = base64.b64decode(packet,' /')
            #     npdata = np.frombuffer(data,dtype=np.uint8)
            #     frame = cv2.imdecode(npdata,1)
            #     cv2.imshow(f"RECEIVING VIDEO From server {socket_fd}",frame)
            # frame = cv2.putText(frame,'FPS: '+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)    
            # print(f"{len(message[:50000])=}")

        # Display the image
            # socket_fd.send(frame_in_bytes)

            # cv2.imshow('Webcam', frame)
        
    # Detect if the Esc key has been pressed


    # Release the video capture object




pid = os.fork()


if pid > 0:
    procces_video()
       
else:
    return_trafic()
    
    


# while True:
#     p = Pool(2)
#     print("Applying return handl")
#     return_trafic_handelr = p.apply(func=return_trafic)
#     # return_trafic_handelr.wait(0.04)
#     print("Applying forward handl")
#     forward_trafic_handelr = p.apply(func=procces_video)
#     print("loop iteration done")
#     # forward_trafic_handelr.wait(0.04)
    

# p.close()
# p.join()

# t = Process(target=return_trafic)
# # t.setDaemon(True)
# t.start()

# t1 = Process(target=procces_video)
# t1.start()

# t.join()

# t1.join()
# t.join()



# This is server code to send video frames over UDP
# import cv2, imutils, socket
# import numpy as np
# import time
# import base64

# BUFF_SIZE = 65536
# server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
# server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
# host_name = socket.gethostname()
# host_ip = '192.168.1.102'#  socket.gethostbyname(host_name)
# print(host_ip)
# port = 9999
# socket_address = (host_ip,port)
# server_socket.bind(socket_address)
# print('Listening at:',socket_address)

# vid = cv2.VideoCapture(0) #  replace 'rocket.mp4' with 0 for webcam
# fps,st,frames_to_count,cnt = (0,0,20,0)

# while True:
# 	msg,client_addr = server_socket.recvfrom(BUFF_SIZE)
# 	print('GOT connection from ',client_addr)
# 	WIDTH=400
# 	while(vid.isOpened()):
# 		_,frame = vid.read()
# 		frame = imutils.resize(frame,width=WIDTH)
# 		encoded,buffer = cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY,80])
# 		message = base64.b64encode(buffer)
# 		server_socket.sendto(message,client_addr)
# 		frame = cv2.putText(frame,'FPS: '+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
# 		cv2.imshow('TRANSMITTING VIDEO',frame)
# 		key = cv2.waitKey(1) & 0xFF
# 		if key == ord('q'):
# 			server_socket.close()
# 			break
# 		if cnt == frames_to_count:
# 			try:
# 				fps = round(frames_to_count/(time.time()-st))
# 				st=time.time()
# 				cnt=0
# 			except:
# 				pass
# 		cnt+=1