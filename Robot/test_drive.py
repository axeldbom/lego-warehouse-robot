#!/usr/bin/env python3
import ev3dev.ev3 as ev3
from ev3dev2.motor import *
from time import sleep
from robot_controls import Robot

if __name__ == "__main__":
    robot = Robot(25,50)
    # robot.color_sensor()
    print("in main")
    while True:
        x = input("degrees: ")
        if x == 'q': exit()
        x = int(x)
        robot.steer_pair.on_for_degrees(100, 25, x, brake=False)
    
    
    '''
    while True:
        x = input(":")
        if x == 'h':
            robot.hook_package()
            print("hooked")
        #time.sleep(1)
        elif x == 'u':
            robot.unhook_package()
            print("unhooked")
        elif x == 'r':    
            for i in range(0,25):
                distance = robot.us.value()
                print("Dist = ", distance)
                if distance < 50:
                    print("if")
                    robot.hook_package()
                else:
                    robot.unhook_package()
                time.sleep(0.5)
        else:
            exit()
    '''
    '''    
    for i in range(0,100) :
        robot.gyro_sensor()
        time.sleep(0.5)
    '''
