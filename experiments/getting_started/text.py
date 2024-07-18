# Needs sudo apt-get install python3-opencv,
# which isn't mentined in the tutorial documentation. Sigh.
from picamera2 import Picamera2, MappedArray
import cv2, time

resolution = (2592, 1944)
filepath = "/home/jonathan/Desktop/"

def apply_text(request):
    # text options
    colour = (255, 255, 255)
    origin = (60, 200)
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = 6
    thickness = 18
    text = "Hello, world!"
    with MappedArray(request, "main") as m:
        cv2.putText(m.array, text, origin, font, scale, colour, thickness)

# create camera object
picam2 = Picamera2()

# Create two separate configs - one for preview and one for capture.
# Make sure the preview is the same resolution as the capture, to make
# sure the overlay stays the same size
capture_config = picam2.create_still_configuration({"size": resolution})
preview_config = picam2.create_preview_configuration({"size": resolution})

# Set the current config as the preview config
picam2.configure(preview_config)

# Add the timestamp
picam2.pre_callback = apply_text
# start the camera
picam2.start(show_preview=True)
time.sleep(2)

# switch to capture config and take a picture
image = picam2.switch_mode_and_capture_file(capture_config, filepath+"textOnPhoto.jpg")

# CLose the camera
picam2.close()
