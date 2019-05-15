import socketio
import base64
import time
import socket
import argparse
import cv2


"""
Argument that can be passed when running the script

* help: displays all available flags
* devm: Developer mode, which enables an external window that shows the video feed
* url: Url to the server, http://<url>

"""
parser = argparse.ArgumentParser()
parser.add_argument(
    '--url', help='url to the server - http://<input>, defaults as localhost:3000', default='localhost:3000')
parser.add_argument(
    '--strm', help='Streamer mode - streams footage from the device to the server', action='store_true')
parser.add_argument(
    '--dname', help='Device name - the name of the device to connect to', default='localhost:3000')
args = parser.parse_args()


"""
**recordAndEmit**

Records footage with connected camera device and emits the data to a server with the help of the sio socket.
* sio - socket used to send the data to a server
return None
"""


def recordAndEmit(socket=None, delay=1/30):
    camera = cv2.VideoCapture(0)
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
        time.sleep(delay)  # regulates how fast we send a signal to the server

    camera.release()


host = args.dname  # get local machine name
port = 4040  # Make sure it's within the > 1024 $$ <65535 range

r_socket = socket.socket()
r_socket.connect((host, port))


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
    if args.strm:
        recordAndEmit(sio)
        sio.disconnect()

    elif len(input("Press enter to terminate...\n")) >= 0:
        r_socket.close()
        sio.disconnect()


@sio.on('my message')
def on_message(data):
    print('message received with ', data)
    sio.emit('my response', {'response': 'my response'})


@sio.on('keys')
def on_keys(data):
    if data["ArrowUp"]:
        r_socket.send('arrowup'.encode('utf-8'))
    if data["ArrowDown"]:
        r_socket.send('arrowdo'.encode('utf-8'))
    if data["ArrowLeft"]:
        r_socket.send('arrowle'.encode('utf-8'))
    if data["ArrowRight"]:
        r_socket.send('arrowri'.encode('utf-8'))
    if data["SpaceBar"]:
        r_socket.send('spaceba'.encode('utf-8'))


@sio.on('disconnect')
def on_disconnect():
    print('disconnected from server')


sio.connect('http://'+args.url)
sio.wait()
