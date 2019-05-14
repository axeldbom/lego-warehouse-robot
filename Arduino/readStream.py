import serial, time

ser = serial.Serial('/dev/ttyACM0', 9600)

while 1:
    serial_line = ser.readline()
    
    # print tempearture data only
    print(serial_line[serial_line.find("Temp"):serial_line.find("C")+1])

    time.sleep(300) # sleep 5 minutes

    # Loop restarts once the sleep is finished

ser.close() # Only executes once the loop exits