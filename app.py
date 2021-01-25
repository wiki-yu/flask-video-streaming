#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response
import cv2
import numpy as np

# import camera driver
if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from camera_opencv import Camera

# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

app = Flask(__name__)


@app.route('/')
def index():
    """Video streaming home page."""
    print("step2")
    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    print("step4")
    while True:
        frame = camera.get_frame()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY ) 
        # # aca5472-17uc
        # width = 100
        # height = 100
        # dim = (width,height)
        # frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA) 
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    print("step3")
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    print("step1")
    app.run(host='0.0.0.0', threaded=True)
