# Arduino

`arduinoSensor-05-05` : streams sensor values via Bluetooth



# Python Script

To use python script, first have to install necessary packages:

1. `gunzip -c pyserial-3.4.tar.gz | tar xopf -`
2. `cd pyserial-3.4`
3. `python setup.py install`

`readStream.py` : reads streamed data from Arduino device over bluetooth channel

* in the code, change the port on `line 5` according to the device running the script (for windows, the ports start with `COM`, where as Linux/Mac uses `/dev/tty`).