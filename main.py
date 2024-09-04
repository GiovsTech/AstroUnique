import sys
sys.path.append('lib/')

from flask import Flask, render_template, Response, request, send_from_directory
from lib.camera import VideoCamera
import os
from star_location_by_gps import *
from threading import Thread

def async_timelapse_detection(fn1, fn2, argue, argue2):
    if fn1 == True:
        thr = Thread(target=pi_camera.take_timelapse(argue,argue2), args=[argue, argue2])
    elif fn2 == True:
        thr = Thread(target=pi_camera.star_detection(int(argue)), args=[int(argue)])
    thr.start()
    return thr

pi_camera = VideoCamera(flip=False) 

app = Flask(__name__)

@app.route('/')
def index() -> str:
    return render_template('index.html') 

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed() -> Response:
    return Response(gen(pi_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/picture')
def take_picture() -> str:
    pi_camera.take_picture()
    return "None"


@app.route('/timelapse', methods=['GET'])
def timelapse_request():
    sec = request.args.get("sec", "")
    hour = request.args.get("h", "")
    async_timelapse_detection(True, None, sec, hour)
    return "None"

@app.route('/detection', methods=['GET'])
def detection():
    h = request.args.get("h", "")
    async_timelapse_detection(None, True, int(h), None)
    return "None"

@app.route('/getlocation', methods=['GET'])
def get_location():
    lat = request.args.get("lat", "")
    lon = request.args.get("lon", "")
    datetime = request.args.get("date", "")
    cd_to_cel(float(lat), float(lon))
    return "DONE"


if __name__ == '__main__':
    context = ('local.crt', 'local.key')
    app.run(host='0.0.0.0', debug=False, ssl_context=context, threaded=True)
