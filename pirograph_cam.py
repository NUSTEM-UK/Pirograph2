from picamera2 import Picamera2, Preview
from picamera2.controls import Controls
import pygame
from time import sleep


# Factor out camera control and operations from pirograph.py as a PirographCam class


class PirographCam:
    def __init__(self, width=1280, height=720):
        """Initialize the camera and set up initial exposure settings."""

        self.width = width
        self.height = height

        # Instantiate the camera
        self.picam2 = Picamera2()

        # basic configuration
        self.capture_config = self.picam2.create_still_configuration(
            {"size": (self.width, self.height)}
        )
        self.preview_config = self.picam2.create_still_configuration(
            {"size": (self.width, self.height)}
        )
        self.picam2.configure(self.capture_config)

        # Start the preview to run the camera event loop (but don't display it)
        self.picam2.start_preview(Preview.NULL)
        # Start offering frames
        self.picam2.start()
        # Give the camera a couple of seconds to sort itself out
        sleep(2)

        # Capture the camera settings
        self.metadata = self.picam2.capture_metadata()
        self.controls = {c: self.metadata[c] for c in ["ExposureTime", "AnalogueGain"]}

        # Lock the exposure, using the object syntax
        self.exposure_controls = Controls(self.picam2)
        self.exposure_controls.AnalogueGain = self.controls["AnalogueGain"]
        self.exposure_controls.ExposureTime = self.controls["ExposureTime"]
        self.picam2.set_controls(self.exposure_controls)

    def capture_frame(self) -> pygame.Surface:
        """Grab a camera frame and return a pygame surface."""
        return pygame.image.frombuffer(
            self.picam2.capture_array("main").data, (self.width, self.height), "RGB"
        )

    def stop(self) -> None:
        """Stop the camera and close the preview window."""
        self.picam2.stop()
        self.picam2.stop_preview()

    # Exposure controls
    def set_exposure(self, exposure_time: float, analogue_gain: float) -> None:
        """Set the exposure time and analogue gain."""
        self.exposure_controls.AnalogueGain = analogue_gain
        self.exposure_controls.ExposureTime = exposure_time
        self.picam2.set_controls(self.exposure_controls)

    # return width and height tuple
    def get_size(self) -> tuple:
        """Return the camera frame size."""
        return (self.width, self.height)

    # return current exposure time
    @property
    def exposure_time(self) -> float:
        """Return the current exposure time."""
        return self.exposure_controls.ExposureTime

    # set exposure time
    @exposure_time.setter
    def exposure_time(self, value: float) -> None:
        """Set the exposure time."""
        self.exposure_controls.ExposureTime = value
        self.picam2.set_controls(self.exposure_controls)

    # return current analogue gain
    @property
    def analogue_gain(self) -> float:
        """Return the current analogue gain."""
        return self.exposure_controls.AnalogueGain

    # set analogue gain
    @analogue_gain.setter
    def analogue_gain(self, value: float) -> None:
        """Set the analogue gain."""
        self.exposure_controls.AnalogueGain = value
        self.picam2.set_controls(self.exposure_controls)
