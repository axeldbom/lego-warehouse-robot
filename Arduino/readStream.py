import serial, time, msvcrt

# port for unix/mac is '/dev/tty****'
#          windows is 'COM*'
# ser = serial.Serial('/dev/ttyACM0', 9600)
ser = serial.Serial('COM9', 9600)
init_time = -1

string_arr = ["","UV: ","VIS: ","IR: ","Temp: ","Humidity: "]
while 1:
    # UV:VIS:IR:TEMP:HUM
    stream_line = ser.readline()
    warning = False
    print_str = []

    # initial timestamp =  (server's time) - (first timestamp from arduino)
    # timestamp = (initialtimestamp) + timestamp
    
    if str(stream_line,'utf-8').strip()[-1:]=="/":
        # format string output
        arr = str(stream_line, 'utf-8').strip()[:-1].split(":")
        if init_time==-1:
            init_time = int(round(time.time() * 1000)) - int(arr[0][:-3])
        arr[0] = str(init_time + int(arr[0][:-3]))
        for idx,val in enumerate(arr):
            print_str.append(string_arr[idx] + val)
        if warning:
            warning = False
        print("{:16}{:10}{:14}{:12}{:>12}C{:>18}%".format(print_str[0],print_str[1],print_str[2],print_str[3],print_str[4],print_str[5]))
    else:
        stripped = str(stream_line, 'utf-8').strip()
        if stripped.startswith("WARNINGS"):
            warning = True
            print(stripped)
            arr = str(ser.readline(), 'utf-8').strip()[:-1].split(":")
            arr[0] = str(init_time + int(arr[0][:-3]))
            for idx,val in enumerate(arr):
                print_str.append(string_arr[idx] + val)
        print("{:16}{:10}{:14}{:12}{:>12}C{:>18}%".format(print_str[0],print_str[1],print_str[2],print_str[3],print_str[4],print_str[5]))

    if warning == False:
        try:
            1 # dummy line 
        except KeyboardInterrupt:
            t = input()
            print('input', t)
            ser.write(t.encode('utf-8'))

    # Loop restarts once the sleep is finished

ser.close() # Only executes once the loop exits
