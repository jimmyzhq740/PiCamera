import pygame
from picamera2 import Picamera2, Preview
from libcamera import Transform, controls
import threading
import time

picam2 = Picamera2()

pygame.init()
window = pygame.display.set_mode((300, 300))
pygame.display.set_caption("Pygame Demonstration")

def run_focus():
    mainloop=True
    lensposition= 5.0
    while mainloop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False
            if event.type == pygame.KEYDOWN:
                print(pygame.key.name(event.key))
                if event.key == pygame.K_UP:
                    lensposition +=1
                    picam2.set_controls({"AfMode": controls.AfModeEnum.Manual,"LensPosition":lensposition})
                    print('Lensposition: ', lensposition)
                elif event.key == pygame.K_DOWN:
                    lensposition -=1
                    picam2.set_controls({"AfMode": controls.AfModeEnum.Manual,"LensPosition":lensposition})
                    print('Lensposition: ', lensposition)
                elif event.key == pygame.K_ESCAPE:
                    mainloop=False

    pygame.quit()

def run_camera():
    # Initialize the preview here.
    try:
        picam2.start_preview(Preview.QTGL, x=200, y=100, width=800, height=600)
        picam2.start()
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # Use ESCAPE key to close the preview
                        running = False

    except RuntimeError as e:
        print(f"Failed to start the camera: {e}")
    finally:
        picam2.stop()
        picam2.stop_preview()

if __name__ == "__main__":
    try:
        t1 = threading.Thread(target=run_focus)
        # t1.daemon = True
        t1.start()
        run_camera()

    finally:
        pygame.quit()


# Keep the program alive until we stop it manually
# try:
#     input("Press Enter to stop...")
# finally:
#     picam2.stop_preview()
#     picam2.stop()
