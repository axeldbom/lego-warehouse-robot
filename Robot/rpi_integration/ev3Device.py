import sys
sys.path.append('../../')
import socket
from Robot.robot_controls import Robot
import argparse

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


robot = Robot(30, 30)


def server():
    host = args.dname   # get local machine name
    port = 4040  # Make sure it's within the > 1024 $$ <65535 range

    s = socket.socket()
    s.bind((host, port))

    s.listen(1)
    client_socket, adress = s.accept()
    print("Connection from: " + str(adress))
    while True:
        data = client_socket.recv(7).decode('utf-8')
        if not data:
            break
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
        print(data)
        print('--------------')
        # print('From online user: ' + data)
        # data = data.upper()
        # client_socket.send(data.encode('utf-8'))
    client_socket.close()


server()
