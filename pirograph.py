import pygame
from picamera2 import Picamera2, Preview
from picamera2.controls import Controls
from time import time, sleep
import numpy as np


# Frame size
# this will need substantial experimentation
# In some respects, a square frame fits better
width, height = 1280, 720

# Instantiate the camera
picam2 = Picamera2()

# capture_config = picam2.create_still_configuration({"size": (width, height)}, controls=camera_controls)
capture_config = picam2.create_still_configuration({"size": (width, height)})
preview_config = picam2.create_still_configuration({"size": (width, height)})
picam2.configure(capture_config)

# Start the camera
# We're not using the preview window, but need it to run the camera event loop
picam2.start_preview(Preview.NULL)
picam2.start()
# Give the camera a couple of seconds to sort itself out
sleep(2)

# Capture the camera settings
metadata = picam2.capture_metadata()
controls = {c: metadata[c] for c in ["ExposureTime", "AnalogueGain"]}

# Lock the exposure, using the object syntax
exposure_controls = Controls(picam2)
exposure_controls.AnalogueGain = controls["AnalogueGain"]
exposure_controls.ExposureTime = controls["ExposureTime"]
picam2.set_controls(exposure_controls)

# Now configure the PyGame environment
pygame.init()
# TODO: I'm not sure what the 0 is in the following line
screen = pygame.display.set_mode((width, height), 0, 32)
pygame.display.set_caption("Pirograph")
# Disable Pygame events...
pygame.event.set_allowed(None)
# ...and selectively re-enable the ones we actually want
pygame.event.set_allowed([pygame.KEYDOWN, pygame.QUIT])

# System status
running = True


def capture_frame():
    """Grab a camera frame and return a pygame surface.

    Doesn't seem to affect performance - we're presumably passing the
    surface object reference rather than copying it."""
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


def change_exposure():
    """Testing that I have this right."""
    global picam2
    global exposure_controls
    exposure_controls.ExposureTime += 1000
    exposure_controls.AnalogueGain += 0.1
    picam2.set_controls(exposure_controls)
    print(exposure_controls.ExposureTime, exposure_controls.AnalogueGain)



def output_exposure():
    """It looks like the object methods don't return properties.

    ...so this is the best way of doing this. Now rolled into the startup code."""
    global picam2
    metadata = picam2.capture_metadata()
    controls = {c: metadata[c] for c in ["ExposureTime", "AnalogueGain"]}
    print(controls)
    # Result is about 30000 for ExposureTime, 2.0 for AnalaogueGain
    # Looks like the gain varies preferentially for the autoexposure system


def frame_stats(time_begin, time_start, frame_count, sample_window = 1):
    """Output frame statistics.

    Note that the variable passing seems to have a minor performance impact,
    though this is negligible on a five-frame window. Could be related to
    terminal scrollback?"""
    time_now = time()
    time_taken = (time_now - time_start) / sample_window
    time_since_begin = time_now - time_begin
    frame_rate = frame_count / time_since_begin
    print (f"Frame {frame_count} in {time_taken:.3f} secs (5-frame rolling average), at {frame_rate:.2f} fps.")
    # Original telemetry, for reference
    # print "Frame %d in %.3f secs, at %.2f fps: shutter: %d, low: %d high: %d" % (frame_count, time_taken, (frame_count/time_since_begin), camera.shutter_speed, threshold_low, threshold_high)


def main():
    # Take a timestamp for the start of the run.
    # Note that the camera is already set up
    time_begin = time()
    frame_count = 0
    while (running):
        # Timestamp for the start of this frame
        time_start = time()
        surface = capture_frame()
        screen.blit(surface, (0, 0))
        pygame.display.update()
        frame_count += 1

        # Check inputs every five frames only, might be quicker
        # (or might give a horrid update cadence, we'll see)
        if frame_count % 5 == 0:
            frame_stats(time_begin, time_start, frame_count, 5)
            handle_inputs()
            change_exposure()
            # output_exposure()


if __name__ == "__main__":
    main()


