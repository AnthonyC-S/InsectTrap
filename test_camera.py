# import cv2

# cap = cv2.VideoCapture(0)
# success, image = cap.read()

# print(image)

# cap.release()
# cv2.destroyAllWindows()

import time
from picamera2 import Picamera2, Preview

picam = Picamera2()

config = picam.create_preview_configuration()
picam.configure(config)

picam.start_preview(Preview.QTGL)

picam.start()
time.sleep(2)
picam.capture_file("test-python.jpg")

picam.close()