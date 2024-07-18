from picamera2 import Picamera2
from time import sleep

picam2 = Picamera2()

# Show unaltered image
picam2.start(show_preview=True)
sleep(2)
picam2.stop_preview()
picam2.stop()

# Alter the image levels
# It's not clear that this works, as such.
controls = {
    "ExposureTime": 10000,
    "AnalogueGain": 1.0,
    "Contrast": 2
}

preview_config = picam2.create_preview_configuration(controls=controls)
picam2.configure(preview_config)

# Show altered image
picam2.start(show_preview=True)
sleep(2)
picam2.close()
