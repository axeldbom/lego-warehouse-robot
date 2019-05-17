import socketio
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
parser.add_argument(
    '--strm', help='Streamer mode - streams footage from the device to the server', action='store_true')
parser.add_argument(
    '--rspeed', help='Streamer mode - streams footage from the device to the server', default=10)
args = parser.parse_args()
if not args.devm:
    from robot_controls import Robot
    import ev3dev.ev3 as ev3
    from ev3dev2.motor import *
if args.strm:
    import cv2
    print('imported cv2...')

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
autonomous = False
control_dic = {}
sio = socketio.Client()
if not args.devm:
    robot = Robot(int(args.rspeed), int(args.rspeed))


def autonomous_robot(robot):

    # PID stuff
    Kp = 1  # proportional gain
    Ki = 2000  # integral gain
    Kd = 0  # derivative gain

    Ts = 0.5  # sampling time for color sensor is twice per second = 0.5 s

    integral = 0
    previous_error = 0

    # wanted value for the color sensor
    target_value = 45  # 35 is good for black/white

    # main loop
    while autonomous:

        if robot.button.any():
            exit()

        if robot.ts.value():
            robot.package = True
            robot.stop()
            robot.hook_package()

        # package stuff
        distance = robot.us.value()
        if distance < 40 and not robot.package:
            robot.stop()
            robot.hook_package()

        # PID stuff
        error = target_value - robot.cs.value()

        if Ki > 0:
            integral += Ts/Ki * error
        else:
            integral = 0

        if Kd > 0:
            derivative = Kd/Ts * (error - previous_error)
        else:
            derivative = 0

        # final output of PID equation
        # u == 0: continue forward
        # u > 0: steer right
        # u < 0: steer left
        u = Kp * (error + integral + derivative)
        # print("u = ", u)

        # run motors
        if u > -2 and u < 2:
            robot.steer_pair.on_for_seconds(0, robot.speed, Ts, brake=False, block=False)
        else:
            if u < -100:
                u = -100
            elif u > 100:
                u = 100
            robot.steer_pair.on_for_seconds(u, robot.speed, Ts, brake=False, block=False)
            # tank_pair.on_for_seconds(speed * (1 + u/100), speed * (1 - u/100), Ts, brake=False, Block=False)
        previous_error = error


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
        sio.disconnect()


@sio.on('my message')
def on_message(data):
    print('message received with ', data)
    sio.emit('my response', {'response': 'my response'})


@sio.on('keys')
def on_keys(data):
    global autonomous
    control_dic = data
    if data['a'] and autonomous:
        autonomous = False
    elif data['a'] and not autonomous:
        autonomous = True
    if not autonomous:
        if not args.devm:
            if data["ArrowUp"]:
                robot.drive_forward()
            if data["ArrowDown"]:
                robot.drive_backwards()
            if data["ArrowLeft"]:
                robot.turn_left()
            if data["ArrowRight"]:
                robot.turn_right()
            if data["SpaceBar"]:
                robot.hook_package()
        else:
            print(data)
    else:
        autonomous_robot(robot)


@sio.on('disconnect')
def on_disconnect():
    print('disconnected from server')


sio.connect('http://'+args.url)
sio.wait()
