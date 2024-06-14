
import cv2
from picamera2 import  Picamera2
from libcamera import  controls
import time

lensposition=5

def gen_video():
    """Video streaming generator function."""
    global lensposition
    picam2 = Picamera2()
    capture_config=picam2.create_still_configuration({'format':'RGB888', 'size':(800,606)})
    picam2.configure(capture_config)
    picam2.start()
    
    #vs = cv2.VideoCapture(0)
    while True:
        # Set manual focus
        picam2.set_controls({"AfMode": controls.AfModeEnum.Manual,"LensPosition":lensposition})
        frame = picam2.capture_array()
        #print (lensposition)
        #ret,frame=vs.read()
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame=jpeg.tobytes()
        yield (b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def capture_and_send_image(counter):
    picam2 = Picamera2()
    capture_config=picam2.create_still_configuration({'format':'RGB888', 'size':(800,606)})
    picam2.configure(capture_config)
    picam2.start()
    picam2.set_controls({"ExposureTime":100000})
    for i in range (counter):
        time.sleep(2)
        image_path = f'/home/jimmyzhang1/Desktop/web2/images/image_{i}.jpg'
        picam2.set_controls({"AfMode": controls.AfModeEnum.Manual,"LensPosition":18})
        picam2.capture_file(image_path)
    picam2.stop()

def set_lensposition_state (state):
    global lensposition
    if state == 'increase':
        lensposition += 1
        print (lensposition)
        return lensposition
    elif state == 'decrease':
        lensposition -=1
        print (lensposition)
        return lensposition
    