import os
import time
from datetime import datetime
from picamera2 import Picamera2, Preview

# Initialize the camera
picam2 = Picamera2()

# Create the full resolution configuration
camera_config = picam2.create_still_configuration(main={"size": (3456, 3456)}, lores={"size": (640, 640)}, display="lores")
picam2.configure(camera_config)

# Set the directory to save images
save_directory = "/home/jimmyzhang1/Desktop/wheat_images"

# Create the directory if it does not exist
os.makedirs(save_directory, exist_ok=True)

capture_config2=picam2.set_controls({"ExposureTime":60000,"AnalogueGain":1.5})
picam2.title_fields=["ExposureTime", "AnalogueGain"]
# Start the camera preview
picam2.start_preview(Preview.QTGL)
picam2.start()



def capture_image():
    # Generate the file name with current date and time
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"image_{timestamp}.jpg"
    file_path = os.path.join(save_directory, file_name)
    
    # Capture the image
    picam2.capture_file(file_path)
    print(f'Image Captured: {file_path}')

try:
    while True:
        capture_image()
        # Wait for 1 hour (3600 seconds)
        time.sleep(3600)
except KeyboardInterrupt:
    # Stop the preview on keyboard interrupt
    picam2.stop_preview()
    picam2.close()
