import socketio
import argparse
import serial
import time
import msvcrt

parser = argparse.ArgumentParser()
parser.add_argument(
    '--code', help='code used to connect to specific socket', action='store_true')
parser.add_argument(
    '--url', help='url to the server - http://<input>, defaults as localhost:3000', default='localhost:3000')
args = parser.parse_args()


def arduinoRead(socket):
    ser = serial.Serial('COM9', 9600)
    init_time = -1
    string_arr = ["", "UV: ", "VIS: ", "IR: ", "Temp: ", "Humidity: "]
    while True:
        # UV:VIS:IR:TEMP:HUM
        stream_line = ser.readline()
        warning = False
        print_str = []

        # initial timestamp =  (server's time) - (first timestamp from arduino)
        # timestamp = (initialtimestamp) + timestamp

        if str(stream_line, 'utf-8').strip()[-1:] == "/":
            # format string output
            arr = str(stream_line, 'utf-8').strip()[:-1].split(":")
            if init_time == -1:
                init_time = int(round(time.time() * 1000)) - int(arr[0])
            arr[0] = str(init_time + int(arr[0]))
            for idx, val in enumerate(arr):
                print_str.append(string_arr[idx] + val)
            if warning:
                warning = False
            print("{:16}{:10}{:10}{:10}{:10}C{:>16}%".format(
                print_str[0], print_str[1], print_str[2], print_str[3], print_str[4], print_str[5]))
        else:
            stripped = str(stream_line, 'utf-8').strip()
            if stripped.startswith("WARNINGS"):
                warning = True
                print(stripped)
                arr = str(ser.readline(), 'utf-8').strip()[:-1].split(":")
                arr[0] = str(init_time + int(arr[0]))
                for idx, val in enumerate(arr):
                    print_str.append(string_arr[idx] + val)
            print("{:16}{:10}{:10}{:10}{:10}C{:>16}%".format(
                print_str[0], print_str[1], print_str[2], print_str[3], print_str[4], print_str[5]))

        if warning == False:
            try:
                1  # dummy line
            except KeyboardInterrupt:
                t = input()
                print('input', t)
                ser.write(t.encode('utf-8'))

        # Loop restarts once the sleep is finished

    ser.close()  # Only executes once the loop exits


sio = socketio.Client()


@sio.on('connect')
def on_connect():
    print('connection established...')
    arduinoRead(sio)


@sio.on('disconnect')
def on_disconnect():
    print('disconnected from server...')


sio.connect('http://'+args.url)
sio.wait()
