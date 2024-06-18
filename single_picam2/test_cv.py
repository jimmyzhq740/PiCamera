from picamera2 import Picamera2, Preview
from libcamera import Transform, controls
import time
from pprint import *

picam2 = Picamera2()
pprint(picam2.sensor_modes)

# Initializes the camera's view on the screen with specified settings
# Make sure the Transform is properly used, here it's initialized without parameters but you might need specifics
transform = Transform()  # Add parameters if needed, e.g., Transform(hflip=True)
picam2.start_preview(Preview.QTGL, x=200, y=100, width=800, height=600, transform=transform)
# Start the camera
try:
    picam2.start()
except RuntimeError as e:
    print(f"Failed to start the camera: {e}")

picam2.set_controls({"ExposureTime":40000,"AnalogueGain":1.0,"ExposureValue": 26.0})

# Set automatic focus
picam2.set_controls({"AfMode": controls.AfModeEnum.Manual,"LensPosition":11.0})

# time.sleep(10)
# picam2.stop_preview()
# # Keep the program alive until we stop it manually
try:
    input("Press Enter to stop...")
finally:
    picam2.stop_preview()
    picam2.stop()
