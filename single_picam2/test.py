from picamera2 import Picamera2, Preview
from libcamera import Transform, controls
import time
import os
import sys
import piexif

def create_folder_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Folder '{path}' created.")
    else:
        print(f"Folder '{path}' already exists.")

picam2 = Picamera2()

preview_config=picam2.create_preview_configuration()
# Camera configured to aspect ratio 4:3
capture_config=picam2.create_still_configuration({"size":(3456,4608)})
picam2.configure()

# Initializes the camera's view on the screen with specified settings
# Make sure the Transform is properly used, here it's initialized without parameters but you might need specifics
transform = Transform()  # Add parameters if needed, e.g., Transform(hflip=True)
picam2.start_preview(Preview.QTGL, x=200, y=100, width=800, height=600, transform=transform)
picam2.start()

#Control Exposure
capture_config2=picam2.set_controls({"ExposureTime":40000,"AnalogueGain":1.5})
#Add Exposure time and analogue gain on preview title
picam2.title_fields=["ExposureTime", "AnalogueGain"]


# Set manual focus
picam2.set_controls({"AfMode": controls.AfModeEnum.Manual,"LensPosition":8.0})

#create_folder_if_not_exists("/home/jimmyzhang/Desktop/images")

# #Taking multiple pictures
# time.sleep(3)
# picam2.start_and_capture_files("/home/jimmyzhang/Desktop/images/image{:d}.jpg",capture_mode=capture_config,initial_delay=3, delay=2, num_files=30)

# counter=1
# image_import_directory = '/home/jimmyzhang/Desktop/images'
# create_folder_if_not_exists('/home/jimmyzhang/Desktop/images_editted')
# image_save_directory = '/home/jimmyzhang/Desktop/images_editted'
# for filename in os.listdir(image_import_directory):
#     img_import_path = os.path.join (image_import_directory, filename)
#     exif_dict=piexif.load(img_import_path)
#     exif_dict['Exif'][piexif.ExifIFD.FocalLength]=(275,100)
#     exif_dict['Exif'][piexif.ExifIFD.FocalLengthIn35mmFilm]=(16,1)
#     exif_bytes = piexif.dump (exif_dict)
#     editted_filename=f"image{counter}.jpg"
#     counter +=1
#     img_save_path = os.path.join (image_save_directory, editted_filename)
#     piexif.insert(exif_bytes, img_import_path, img_save_path) 

# Keep the program alive until we stop it manually
try:
    input("Press Enter to stop...")
finally:
    picam2.stop_preview()
    picam2.stop()
