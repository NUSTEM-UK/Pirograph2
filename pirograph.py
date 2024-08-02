import pygame
from picamera2 import Picamera2, Preview
from time import sleep
import numpy as np


# Frame size
# this will need substantial experimentation
# In some respects, a square frame fits better
width, height = 1280, 720

# Instantiate the camera
picam2 = Picamera2()

# Configure camera capture settings
# Here, using same settings for preview and capture
capture_config = picam2.create_still_configuration({"size": (width, height)})
preview_config = picam2.create_still_configuration({"size": (width, height)})
picam2.configure(capture_config)

# Start the camera
# We're not using the preview window, but need it to run the camera event loop
picam2.start_preview(Preview.NULL)
picam2.start()
# Give the camera a couple of seconds to sort itself out
sleep(2)

# Now configure the PyGame environment
pygame.init()
# TODO: I'm not sure what the 0 is in the following line
screen = pygame.display.set_mode((width, height), 0, 32)
pygame.display.set_caption("Pirograph")
# Disable Pygame events...
pygame.event.set_allowed(None)
# ...and selectively re-enable them
pygame.event.set_allowed([pygame.KEYDOWN, pygame.QUIT])

# System status
running = True

def capture_frame():
    """Grab a camera frame and return a pygame surface."""
    global screen
    global width, height
    global picam2
    surface = pygame.image.frombuffer(picam2.capture_array("main").data, (width, height), 'RGB')
    return surface


def handle_inputs():
    """We'll eventually expand this to handle exposure changes etc."""
    global picam2
    global running
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            # Tidy up camera and exit
            print("Goodbye")
            picam2.close()
            running = False
        else:
            pass


def main():
    frame_count = 0
    while (running):
        surface = capture_frame()
        screen.blit(surface, (0, 0))
        pygame.display.update()
        frame_count += 1

        # Check inputs every five frames only, might be quicker
        # (or might give a horrid update cadence, we'll see)
        if frame_count % 5 == 0:
            handle_inputs()

        print(f"Displayed frame: {frame_count}")

if __name__ == "__main__":
    main()


