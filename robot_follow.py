#!/usr/bin/env python3
import ev3dev.ev3 as ev3
from ev3dev2.motor import *
from time import sleep
from robot_controls import Robot
    
def main(robot):

# PID stuff
Kp = 1  # proportional gain
Ki = 2000  # integral gain
Kd = 0  # derivative gain

Ts = 0.5  # sampling time for color sensor is twice per second = 0.5 s

integral = 0
previous_error = 0

# wanted value for the color sensor
target_value = 35

# main loop
while not robot.manual_control:

	if robot.button.any(): exit()
	
	if robot.ts.value():
		robot.package = True
		robot.stop()
		robot.hook_package()
		
	# package stuff
	distance = robot.us.value()
	print("distance = ", distance)
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
		if u < -100: u = -100
		elif u > 100: u = 100
		robot.steer_pair.on_for_seconds(u, robot.speed, Ts, brake=False, block=False)
		# tank_pair.on_for_seconds(speed * (1 + u/100), speed * (1 - u/100), Ts, brake=False, Block=False)
	previous_error = error

# Main
if __name__ == "__main__":
    robot = Robot()
    main(robot)
