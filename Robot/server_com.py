import socketio
import cv2
import base64
import time
import requests
import sys
# requests lib is needed - use pip install requests
# Handling real time stuff, use opencv - pip install opencv-python


def cameraStuff(sio):
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while True:
        check, frame = camera.read()
        frame = cv2.flip(frame, 1)
        img = cv2.imencode('.jpg', frame)[1]
        data = base64.urlsafe_b64encode(img)  # data to send via socket
        print(sys.getsizeof(data))
        if sio is not None:
            sio.emit('forwardImageRobot', data)
        cv2.imshow("TEST", frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        time.sleep(5)  # regulates how fast we send a signal to the server

    camera.release()
    cv2.destroyAllWindows()


sio = socketio.Client()


@sio.on('connect')
def on_connect():
    print('connection established')
    r = requests.post("http://localhost:3000/streamers/r",
                      data={
                          'nickname': "Robot stream",
                          'title': 'Mr.Robot',
                      })
    print(r.status_code, r.reason)
    if r.status_code == 200:
        pass
        sio.emit('streamSocket')
        cameraStuff(sio)
        sio.disconnect()


@sio.on('my message')
def on_message(data):
    print('message received with ', data)
    sio.emit('my response', {'response': 'my response'})


@sio.on('disconnect')
def on_disconnect():
    print('disconnected from server')


sio.connect('http://localhost:3000')
sio.wait()
