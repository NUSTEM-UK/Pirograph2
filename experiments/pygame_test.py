import pygame
from picamera2 import Picamera2, Preview
from time import sleep

pygame.init()

x = 1280
y = 800

# TODO: Check the syntax here - what's the zero?
screen = pygame.display.set_mode((x, y), 0, 32)

pygame.display.set_caption("Pirograph")
pygame.event.set_allowed(None)
pygame.event.set_allowed([pygame.KEYDOWN, pygame.QUIT])

# Set up the camera
picam2 = Picamera2()
capture_config = picam2.create_still_configuration({"size": (x, y)})
preview_config = picam2.create_still_configuration({"size": (x, y)})
picam2.configure(preview_config)

picam2.start_preview(Preview.NULL)
picam2.start()

sleep(2)

def main():
    global x, y
    status = True
    frame_count = 0
    while (status):
        # Get a frame
        frame = picam2.capture_array("main")
        # Convert frame to Pygame surface
        # surface = pygame.image.frombuffer(frame.tostring(), frame.shape[1::-1], "BGR")
        # Alternative approach (neater, but no faster?)
        surface = pygame.image.frombuffer(frame.data, (x, y), 'RGB')
        # Blit surface to screen
        screen.blit(surface, (0, 0))
        pygame.display.update()
        print(f"Frame: {frame_count}")
        frame_count += 1

        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                # Tidy up camera
                print("Goodbye")
                picam2.close()
                status = False

if __name__ == "__main__":
    main()




# Stackoverflow: https://stackoverflow.com/questions/19306211/opencv-cv2-image-to-pygame-image
# pygame image from opencv image buffer. Shape handles width/height inversion. openCV tends to be BGR
# pygame.image.frombuffer(image.tostring(), image.shape[1::-1], "BGR")


