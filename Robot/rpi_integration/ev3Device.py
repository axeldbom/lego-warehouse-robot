import sys
sys.path.append('../../')
import socket
from Robot.robot_controls import Robot

robot = Robot(30, 30)


def server():
    host = socket.gethostname()   # get local machine name
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
