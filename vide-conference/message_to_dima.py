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
socket_fd.connect((HOST, PORT))

def array_to_bytes(x: np.ndarray) -> bytes:
    np_bytes = BytesIO()
    np.save(np_bytes, x, allow_pickle=True)
    return np_bytes.getvalue()

 
while True:
    # Capture the current frame
    
    socket_fd.send("Hello")
	# frame = cv2.putText(frame,'FPS: '+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)    
    # print(f"{len(message)}")

# Display the image
    # socket_fd.send(frame_in_bytes)

    # cv2.imshow('Webcam', frame)
    # cv2.imshow('TRANSMITTING VIDEO',frame)
# Detect if the Esc key has been pressed
    c = cv2.waitKey(1)
    if c == 27:
        break
# Release the video capture object
cap.release()
# Close all active windows
cv2.destroyAllWindows()

