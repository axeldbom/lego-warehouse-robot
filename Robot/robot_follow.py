#!/usr/bin/env python3
import ev3dev.ev3 as ev3
from ev3dev2.motor import *
from time import sleep
from robot_controls import Robot

def main(robot):

    # PID stuff
    Kp = 1  # proportional gain
    Ki = 2000  # 2000  # integral gain
    Kd = 0  # derivative gain

    Ts = 0.5  # sampling time for color sensor is twice per second = 0.5 s

    integral = 0
    previous_error = 0

    # start gyro ange
    gyro_start = robot.gs.value()
    
    # wanted value for the color sensor
    target_value = 45  # 35 is good for black/white
    print("target value = ", target_value)
    
    # main loop
    while not robot.manual_control:

        if robot.button.any(): exit()

        robot.gyro_sensor()
        angle_diff = abs(gyro_start - robot.gs.value())

        '''
        if angle_diff >= 170 and robot.package):
            robot.turn_180()
            robot.unhook_package()
            robot.package = False
            robot.turn_180()
        '''
        
        if robot.ts.value():
            robot.package = True
            robot.stop()
            robot.unhook_package()
	    
        # package stuff
        distance = robot.us.value()
        print("distance = ", distance)
        if distance < 40 and not robot.package:
            gyro_start = robot.gs.value()
            robot.stop()
            robot.hook_package()

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
        print("u = ", u)

        # run motors
        if u > -1 and u < 1:
            robot.steer_pair.on_for_seconds(0, robot.speed, Ts, brake=False, block=False)
        else:
            if u < -100: u = -100
            elif u > 100: u = 100
            robot.steer_pair.on_for_seconds(u, robot.speed, Ts, brake=False, block=False)
	    # tank_pair.on_for_seconds(speed * (1 + u/100), speed * (1 - u/100), Ts, brake=False, Block=False)
        previous_error = error

# Main
if __name__ == "__main__":
    speed = 10
    turn_speed = 10
    robot = Robot(speed, turn_speed)
    main(robot)
