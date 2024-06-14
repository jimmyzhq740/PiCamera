from flask import Flask, render_template, Response, jsonify
import cv2
from picamera2 import  Picamera2
from libcamera import  controls
import time
import io


app = Flask(__name__,template_folder='templates/')
lensposition=5

#app.config["CACHE_TYPE"] = "null"
@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

def capture_and_send_image(counter):
    picam2 = Picamera2()
    capture_config=picam2.create_still_configuration({'format':'RGB888', 'size':(800,606)})
    picam2.configure(capture_config)
    picam2.start()
    picam2.set_controls({"ExposureTime":1000000})
    for i in range (counter):
        time.sleep(2)
        image_path = f'/home/jimmyzhang1/Desktop/web2/images/image_{i}.jpg'
        picam2.set_controls({"AfMode": controls.AfModeEnum.Manual,"LensPosition":18})
        picam2.capture_file(image_path)
    picam2.stop()

@app.route('/start_capture')
def start_capture():
    capture_and_send_image(30)
    return jsonify({"message": "Capture Finished"}),200


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

@app.route('/increaselens')
def increase_lens():
    result = set_lensposition_state ('increase')
    return jsonify(result)     

@app.route('/decreaselens')
def decrease_lens():
    result = set_lensposition_state ('decrease')
    return jsonify(result)   

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_video(),mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__': 
    app.run(host='0.0.0.0', port =5000
            , debug=True, threaded=True)
