import sys
sys.path.append('./../../')
import socket
from Robot.robot_controls import Robot
import argparse
import _thread as thread

"""
Argument that can be passed when running the script

* help: displays all available flags
* devm: Developer mode, which enables an external window that shows the video feed
* url: Url to the server, http://<url>

"""
parser = argparse.ArgumentParser()
parser.add_argument(
    '--dname', help='Device name - the name of the device to connect to', default='localhost')
args = parser.parse_args()


robot = Robot(10, 10)
autonomous = False


def autonomous_robot(robot,test):
    global autonomous
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

        # package stuff
        distance = robot.us.value()
        if distance < 40 and not robot.package:
            robot.stop()
            robot.hook_package()
            time.sleep(0.5)
            robot.turn_180()
            robot.steer_pair.on_for_seconds(0, -robot.speed, 3.5)
            robot.unhook_package()
            robot.steer_pair.on_for_seconds(0, -robot.speed, 1.5)
            robot.turn_90()

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


def server():
    global autonomous
    host = args.dname   # get local machine name
    port = 4040  # Make sure it's within the > 1024 $$ <65535 range

    s = socket.socket()
    s.bind((host, port))

    s.listen(1)
    client_socket, adress = s.accept()
    print("Connection from: " + str(adress))
    thread.start_new_thread(autonomous_robot, (robot,"arg"))
    while True:
        data = client_socket.recv(7).decode('utf-8')
        if not data:
            break
        if data == 'keyadow' and autonomous:
            autonomous = False
        elif data == 'keyadow' and not autonomous:
            autonomous = True

        if not autonomous:
            if data == "arrowup":
                robot.drive_forward()
            if data == "arrowdo":
                robot.drive_backwards()
            if data == "arrowle":
                robot.turn_left()
            if data == "arrowri":
                robot.turn_right()
            if data == "spaceba":
                robot.hook_package()
        else:
            print(data)
    client_socket.close()


server()
