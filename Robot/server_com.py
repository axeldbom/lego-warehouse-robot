import socketio
import cv2
import base64
import time
import requests
import sys
import argparse
# requests lib is needed - use pip install requests
# Handling real time stuff, use opencv - pip install opencv-python

"""
Argument that can be passed when running the script

* help: displays all available flags
* devm: Developer mode, which enables an external window that shows the video feed
* url: Url to the server, http://<url>

"""
parser = argparse.ArgumentParser()
parser.add_argument(
    '--devm', help='Developer mode - illustrates the video feed in a canvas', action='store_true')
parser.add_argument(
    '--url', help='url to the server - http://<input>, defaults as localhost:3000', default='localhost:3000')
args = parser.parse_args()


"""
**recordAndEmit**

Records footage with connected camera device and emits the data to a server with the help of the sio socket.
* sio - socket used to send the data to a server
return None
"""


def recordAndEmit(socket=None, delay=1/30):
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while True:
        check, frame = camera.read()
        frame = cv2.flip(frame, 1)
        try:
            img = cv2.imencode('.jpg', frame)[1]
        except Exception as e:
            print('Camera is not available, exiting...')
            return
        data = base64.b64encode(img)
        if socket is not None:
            socket.emit('forwardImageRobot', str(data))
        if args.devm:
            cv2.imshow("TEST", frame)
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
        time.sleep(delay)  # regulates how fast we send a signal to the server

    if args.devm:
        cv2.destroyAllWindows()
    camera.release()


"""
The socket and functions used to communicate with the server.
"""
sio = socketio.Client()


@sio.on('connect')
def on_connect():
    print('connection established')
    data = {
        'nickname': 'Mr.Robot',
        'title': 'Robot stream',
        'robotClient': True,
        'password': '0000'
    }
    sio.emit('startNewStreamRobot', data)
    recordAndEmit(sio)
    sio.disconnect()


@sio.on('my message')
def on_message(data):
    print('message received with ', data)
    sio.emit('my response', {'response': 'my response'})


@sio.on('disconnect')
def on_disconnect():
    print('disconnected from server')


sio.connect('http://'+args.url)
sio.wait()
