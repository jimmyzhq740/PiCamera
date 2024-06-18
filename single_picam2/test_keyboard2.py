import pygame
from picamera2 import Picamera2, Preview
from libcamera import Transform, controls
import threading
import time
import os

def create_folder_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Folder '{path}' created.")
    else:
        print(f"Folder '{path}' already exists.")

picam2 = Picamera2()

pygame.init()
window = pygame.display.set_mode((300, 300))
pygame.display.set_caption("Pygame Demonstration")

def run_focus():
    mainloop=True
    lensposition= 5.0
    transform = Transform()
    picam2.start_preview(Preview.QTGL, x=200, y=100, width=800, height=600)
    picam2.start()
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
    picam2.stop()
    picam2.stop_preview()
    pygame.quit()

run_focus()
