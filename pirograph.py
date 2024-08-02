import pygame
from pirograph_cam import PirographCam
from time import time, sleep
import numpy as np


pirocam = PirographCam()

width, height = pirocam.get_size()


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


def handle_inputs():
    """We'll eventually expand this to handle exposure changes etc."""
    global pirocam
    global running
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            # Tidy up camera and exit
            print("Goodbye")
            pirocam.stop()
            running = False
        else:
            pass


def frame_stats(time_begin, time_start, frame_count, sample_window=1):
    """Output frame statistics.

    Note that the variable passing seems to have a minor performance impact,
    though this is negligible on a five-frame window. Could be related to
    terminal scrollback?"""
    time_now = time()
    time_taken = (time_now - time_start) / sample_window
    time_since_begin = time_now - time_begin
    frame_rate = frame_count / time_since_begin
    print(
        f"Frame {frame_count} in {time_taken:.3f} secs (5-frame rolling average), at {frame_rate:.2f} fps."
    )
    # Original telemetry, for reference
    # print "Frame %d in %.3f secs, at %.2f fps: shutter: %d, low: %d high: %d" % (frame_count, time_taken, (frame_count/time_since_begin), camera.shutter_speed, threshold_low, threshold_high)


def main():
    # Take a timestamp for the start of the run.
    # Note that the camera is already set up
    time_begin = time()
    frame_count = 0
    while running:
        # Timestamp for the start of this frame
        time_start = time()
        surface = pirocam.capture_frame()
        screen.blit(surface, (0, 0))
        pygame.display.update()
        frame_count += 1

        # Check inputs every five frames only, might be quicker
        # (or might give a horrid update cadence, we'll see)
        if frame_count % 5 == 0:
            frame_stats(time_begin, time_start, frame_count, 5)
            handle_inputs()
            current_gain = pirocam.analogue_gain
            # Increase exposure
            pirocam.analogue_gain = current_gain + 0.1


if __name__ == "__main__":
    main()
