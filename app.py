#!/usr/bin/env python
from importlib import import_module
import os,cv2
from os import listdir
from os.path import isfile, join
import numpy as np
from flask import Flask, render_template, Response, jsonify, request, send_from_directory, url_for
import time
from flask_cors import CORS

from werkzeug.utils import secure_filename

from urllib.request import urlopen

from getmac import get_mac_address as gma
import psutil
import platform
from datetime import datetime
import GPUtil
from markupsafe import escape
import sqlite3 as sql


# import camera driver
if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from camera import Camera

# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

app = Flask(__name__)
# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/')
def index():
    """Video streaming home page."""
    print("step2")
    # return render_template('index.html')

def gen(camera):
    """Video streaming generator function."""
    print("step4")
    while True:
        frame = camera.get_frame()
        width = 5472//10
        height = 3648//10
        dim = (width,height)
        frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA) 
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/motionDetection')
def motionDetection():
    print("step3")
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    print("step1")
    app.run(host='0.0.0.0', threaded=True)
