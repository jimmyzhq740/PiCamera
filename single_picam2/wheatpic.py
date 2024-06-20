from picamera2 import Picamera2, Preview
from libcamera import Transform, controls
import time
import os
import sys
import piexif

def create_folder_if_not_exists(path):
    if not os.path.exists(path):
        os.mkdir(path)
        print(f"Folder '{path}' created.")
    else:
        print(f"Folder '{path}' already exists.")

picam2 = Picamera2()

preview_config=picam2.create_preview_configuration(main={"size":(4608,2592), "format":"RGB888"})
picam2.configure(preview_config)


# Initializes the camera's view on the screen with specified settings
# Make sure the Transform is properly used, here it's initialized without parameters but you might need specifics
transform = Transform()  # Add parameters if needed, e.g., Transform(hflip=True)
#800x600 pixel (width and height used to set the preview) window 
# at coordinate 100,200 on the display

picam2.start_preview(Preview.QTGL)

# Camera configured to aspect ratio 4:3
capture_config=picam2.create_still_configuration(main={"size":(4608,2592)})
picam2.configure()
picam2.start()

#Control Exposure
capture_config2=picam2.set_controls({"ExposureTime":10000,"AnalogueGain":1.5,"ScalerCrop":(0,0,4608,2592)})
#Add Exposure time and analogue gain on preview title
picam2.title_fields=["ExposureTime", "AnalogueGain"]


# Set manual focus
picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})

create_folder_if_not_exists("/home/jimmyzhang1/Desktop/images")

# #Taking multiple pictures
time.sleep(10)
#picam2.start_and_capture_files("/home/jimmyzhang1/Desktop/images/image_top29.jpg",capture_mode=capture_config,initial_delay=3, delay=5, num_files=1) 

# Keep the program alive until we stop it manually
try:
    input("Press Enter to stop...")
finally:
    picam2.stop_preview()
    picam2.stop()
