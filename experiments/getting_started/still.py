from picamera2 import Picamera2
from time import sleep

picam2 = Picamera2()

# Needs a full path to write successfully
# Also: preview is heavily cropped
# picam2.start_and_capture_file("/home/jonathan/Desktop/new_image.jpg")

# Sequence capture
# picam2.start_and_capture_files("/home/jonathan/Desktop/sequence{:d}.jpg", num_files=3, delay=0.5)

# Video capture
# picam2.start_and_record_video("/home/jonathan/Desktop/new_video.mp4", duration=5, show_preview=True)

# Maximum resolution (for v1 module)
# Looks like v1.2 module is max. 3280x2464
# Minimum is supposedly 64x64
# picam2.preview_configuration.size = (2592, 1944)
# picam2.start(show_preview=True)
# sleep(2)
# picam2.capture_file("/home/jonathan/Desktop/max.jpg")

# This is straight from the tutorial, and the resulting image is 800x600. Sheesh. Need to swap these two configuration directives to achieve the expected results. :facepalm
picam2.preview_configuration.sensor.output_size = (2592,1944)
picam2.preview_configuration.main.size = (800,600)
picam2.configure("preview")
picam2.start(show_preview=True)
sleep(2)
picam2.capture_file("/home/jonathan/Desktop/max2.jpg")

picam2.close()
