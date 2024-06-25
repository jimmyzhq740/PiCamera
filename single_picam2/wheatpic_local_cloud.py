import os
import time
from datetime import datetime
from picamera2 import Picamera2, Preview
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
import pkg_resources

# Initialize the camera
picam2 = Picamera2()

# Create the full resolution configuration
camera_config = picam2.create_still_configuration(main={"size": (4096, 4096)}, lores={"size": (640, 640)}, display="lores")
picam2.configure(camera_config)

# Set the directory to save images
save_directory = "/home/jimmyzhang1/Desktop/wheat_images"

# Create the directory if it does not exist
os.makedirs(save_directory, exist_ok=True)

capture_config2 = picam2.set_controls({"ExposureTime": 20000, "AnalogueGain": 1.5})
picam2.title_fields = ["ExposureTime", "AnalogueGain"]
# Start the camera preview
picam2.start_preview(Preview.QTGL)
picam2.start()

def upload_file_to_gdrive(file_path):
    gauth = GoogleAuth()
    gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(
        pkg_resources.resource_filename(__name__, "seedgermination-88c216809a20.json"), scopes=['https://www.googleapis.com/auth/drive'])

    drive = GoogleDrive(gauth)
    today = datetime.today().strftime("%m/%d/%y")

    folder_name = "Brassica Image"
    parent_directory_id = '1xAva05cVbtPTvT5jI02r1zdVQxpKTRgJ'

    folder_meta = {
        "title":  folder_name,
        "parents": [{'id': parent_directory_id}],
        'mimeType': 'application/vnd.google-apps.folder'
    }

    # Check if folder already exists
    folder_id = None
    foldered_list = drive.ListFile(
        {'q':  "'"+parent_directory_id+"' in parents and trashed=false"}).GetList()

    for file in foldered_list:
        if (file['title'] == folder_name):
            folder_id = file['id']

    if folder_id is None:
        folder = drive.CreateFile(folder_meta)
        folder.Upload()
        folder_id = folder.get("id")

    file_title = os.path.basename(file_path)
    file1 = drive.CreateFile(
        {'parents': [{"id": folder_id}], 'title': file_title})

    file1.SetContentFile(file_path)
    file1.Upload()
    print(f"\n--------- File '{file_title}' is Uploaded ----------")

def capture_and_upload():
    file_path = capture_image()
    upload_file_to_gdrive(file_path)

def capture_image():
    # Generate the file name with current date and time
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"image_{timestamp}.jpg"
    file_path = os.path.join(save_directory, file_name)
    
    # Capture the image
    picam2.capture_file(file_path)
    print(f'Image Captured: {file_path}')
    return file_path

try:
    while True:
        capture_and_upload()
        # Wait for 1 hour (3600 seconds)
        time.sleep(3600)
except KeyboardInterrupt:
    # Stop the preview on keyboard interrupt
    picam2.stop_preview()
    picam2.close()
