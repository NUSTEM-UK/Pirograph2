from picamera2 import Picamera2, Preview
from time import sleep
from libcamera import Transform

picam2 = Picamera2()
picam2.start_preview(Preview.QTGL, transform=Transform(hflip=True))
picam2.start()
sleep(5)
picam2.close()
