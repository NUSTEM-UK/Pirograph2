from picamera2 import Picamera2
from time import sleep
import cv2

picam2 = Picamera2()

picam2.preview_configuration.size = (2592, 1944)
picam2.start(show_preview=True)

sleep(2)

picam2.capture_file("/home/jonathan/Desktop/toProcess.jpg")
picam2.close()

# Oh great, we bounce the file via disk. That's
# always a great way to show an example. Sigh.

img = cv2.imread("/home/jonathan/Desktop/toProcess.jpg")

# Convert to greyscale
greyscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
inverted = 255 - greyscale
blur_inverted = cv2.GaussianBlur(inverted, (125, 125), 0)
inverted_blur = 255 - blur_inverted
sketch = cv2.divide(greyscale, inverted_blur, scale=256)
cv2.imwrite("/home/jonathan/Desktop/sketchImage.jpg", sketch)

