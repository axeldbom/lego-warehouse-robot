import socketio
import cv2
import base64
import time
import requests
# requests lib is needed - use pip install requests
# Handling real time stuff, use opencv - pip install opencv-python


def cameraStuff(sio):
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while True:
        check, frame = camera.read()
        frame = cv2.flip(frame, 1)
        data = base64.b64encode(frame)  # data to send via socket
        if sio is not None:
            sio.emit('forwardImageRobot', data)
        cv2.imshow("TEST", frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        time.sleep(10)

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


@sio.on('my message')
def on_message(data):
    print('message received with ', data)
    sio.emit('my response', {'response': 'my response'})


@sio.on('disconnect')
def on_disconnect():
    print('disconnected from server')


sio.connect('http://localhost:3000')
sio.wait()
