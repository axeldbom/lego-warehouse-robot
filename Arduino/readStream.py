import serial, time

# port for unix/mac is '/dev/tty****'
#          windows is 'COM*'
# ser = serial.Serial('/dev/ttyACM0', 9600)
ser = serial.Serial('COM9', 9600)

while 1:
    UV_line = ser.readline()
    temp_line = ser.readline()
    
    # print tempearture data only
    print(UV_line.decode('utf-8').strip())
    print(str(temp_line, 'utf-8').strip())

    time.sleep(2) # sleep 2 sec

    # Loop restarts once the sleep is finished

ser.close() # Only executes once the loop exits
