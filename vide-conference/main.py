import cv2
import socket, imutils, base64
from io import BytesIO
import numpy as np

#Initialize video capture
cap = cv2.VideoCapture(0)
#scaling factor
scaling_factor = 0.5
# Loop until you hit the Esc key


WIDTH = 400
HOST = '146.70.46.20'
HOST1 = 'localhost'
PORT = 6666

socket_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Connecting...")
socket_fd.connect((HOST, PORT))
print("Cinnected")

def array_to_bytes(x: np.ndarray) -> bytes:
    np_bytes = BytesIO()
    np.save(np_bytes, x, allow_pickle=True)
    return np_bytes.getvalue()

 
while True:
    # Capture the current frame
    ret, frame = cap.read()
    frame = imutils.resize(frame,width=WIDTH)
    encoded, buffer = cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY,80])
    message = base64.b64encode(buffer)
    socket_fd.send(message)
	# frame = cv2.putText(frame,'FPS: '+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)    
    print(f"{len(message)}")

# Display the image
    # socket_fd.send(frame_in_bytes)

    # cv2.imshow('Webcam', frame)
    cv2.imshow('TRANSMITTING VIDEO',frame)
# Detect if the Esc key has been pressed
    c = cv2.waitKey(1)
    if c == 27:
        break
# Release the video capture object
cap.release()
# Close all active windows
cv2.destroyAllWindows()


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