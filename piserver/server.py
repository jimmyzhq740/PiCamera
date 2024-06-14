import socket
import os 
import requests
import dweepy
import time
import random
import threading
import argparse

from flask import Flask, jsonify, Response
from uuid import getnode as get_mac
from utils import is_raspberry_pi, get_thing
from camera import gen_video, set_lensposition_state, capture_and_send_image

app = Flask(__name__)


def get_ip():
    """
    Get the external IP address as a string
    """
    try:
        #socket.gethostname() retrieves the hostname of the machine, in this case, return raspberrypi  
        ip_list = socket.gethostbyname_ex(socket.gethostname())[2]

        #filter out localhost address
        ip = next ((ip for ip in ip_list if not ip.startswith("127.")), None)

        if ip:
            return ip
    except socket.gaierror:
        pass

    # if the above method fails, use an alternative approach 
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8",53))
            return s.getsockname()[0]
    except Exception:
        return "no IP found"

def getserial():
    # Extract serial from cpuinfo file
    cpuserial = "0000000000000000"
    try:
        f = open('/proc/cpuinfo', 'r')
        for line in f:
            if line[0:6] == 'Serial':
                cpuserial = line[10:26]
        f.close()
    except:
        cpuserial = "ERROR000000000"
    return cpuserial

def get_hw_id():
    """
    Retrieve a unique hardware identifier for the machine it's running.
    The identifier could be a MAC address for non-raspberry pi 
    Or a UUID for raspberry pi device
    """
    if not is_raspberry_pi():
        return str(hex(get_mac()))
    
    if os.path.exists('/home/pi/serial.txt'):
        with open('/home/pi/serial.txt', 'r') as f:
            return f.read().strip()
    
    r = requests.get("https://www.uuidgenerator.net/api/version4")
    uid = str(r.content)

    with open('/home/pi/serial.txt', 'w') as f:
        f.write(uid)

    return uid.strip()

last_ip = "ha"

def ip_update_loop(secret, verbose):
    """
    Periodically check and update the local IP address and the master server IP. 
    It uses a service called dweepy to get the master server's IP and then
    continuously checks the local IP address, updating the master server 
    if the local Ip address changes

    """
    global last_ip

    #The secret is turned into SHA-1 hash in hex format
    secret = get_thing(secret)

    master_ip = ""

    #The first while loop gets the IP address of the master server
    while True:
        print("Getting mastcapture_and_send_imageer")
        try:
            d = dweepy.get_latest_dweet_for(secret)
            print(d)
            master_ip = d[0]['content']['master_ip']
            break
        except Exception as e:
            print(e)

        time.sleep(random.randint(4, 30))

    print("Master IP", master_ip)

    print (get_ip())
    # this while runs infinitly, and update the local ip address via last_ip= get_ip()
    while True:
        if (last_ip != get_ip()):
            try:
                requests.get("http://%s:5555/ip/%s" % (master_ip, get_ip()))
                last_ip = get_ip()
            except:
                last_ip = "ha"
        time.sleep(3)

@app.route('/ping')
def ping():
    """
    Endpoint to receive the uuid of a raspberry pi
    """
    return jsonify({"uuid": get_hw_id()})

@app.route('/reboot')
def reboot():
    """
    Endpoint to reboot
    """
    os.system('reboot now')
    return jsonify({"ok": "ok"})

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

@app.route('/start_capture')
def start_capture():
    capture_and_send_image(30)
    return jsonify({"message": "Capture Finished"}),200
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PiShot slave server.")

    parser.add_argument(
        "--secret",
        help="A long unique string that's consistent across all Pi's",
        action="store",
        dest="secret",
        type=str,
        required=True,
    )

    parser.add_argument(
        "--verbose",
        help="Print out verbose messages.",
        action="store_true",
        dest="verbose",
    )

    args = parser.parse_args()

    #threading used to run the system 
    ip_thread = threading.Thread(
        target=ip_update_loop,
        args=(args.secret, args.verbose,)
    )

    ip_thread.daemon = True
    ip_thread.start()

    app.run(host="0.0.0.0", port=5000)

print (get_ip())
print (getserial())
print (get_hw_id())
print (socket.gethostname())
print (socket.gethostbyname_ex(socket.gethostname()))