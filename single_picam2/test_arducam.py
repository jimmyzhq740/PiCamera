import os
import time
import sys
import threading
import pygame,sys
from pygame.locals import *
from time import ctime, sleep
os.environ['XDG_RUNTIME_DIR'] = '/run/user/1000'
pygame.init()
screen=pygame.display.set_mode((320,240),0,32)
pygame.key.set_repeat(100)
def runFocus(func):
    temp_val = 512
    while True:
        try:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    print(temp_val)
                    if event.key == pygame.K_UP:
                        print('UP')
                        if temp_val < 1000:
                            temp_val += 10
                        value = (temp_val << 4) & 0x3ff0
                        dat1 = (value >> 8) & 0x3f
                        dat2 = value & 0xf0
                        os.system(f"i2cset -y 0 0x0c {dat1} {dat2}")
                    elif event.key == pygame.K_DOWN:
                        print('DOWN')
                        if temp_val > 10:  # Fixed the logic to allow decrement down to 10
                            temp_val -= 10
                        value = (temp_val << 4) & 0x3ff0
                        dat1 = (value >> 8) & 0x3f
                        dat2 = value & 0xf0
                        os.system(f"i2cset -y 0 0x0c {dat1} {dat2}")
        except pygame.error as e:
            print(f"Pygame error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

                    
def runCamera():
    try:
        # Make sure the command is correctly configured
        cmd = "sudo libcamera-still -t 0"
        os.system(cmd)
    except Exception as e:
        print(f"Error in runCamera: {e}")
if __name__ == "__main__":
    try:
        t1 = threading.Thread(target=runFocus, args=(None,))
        t1.daemon = True
        t1.start()

        runCamera()
    finally:
        pygame.quit()