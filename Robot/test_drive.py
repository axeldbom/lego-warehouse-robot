#!/usr/bin/env python3
import ev3dev.ev3 as ev3
from ev3dev2.motor import *
from time import sleep
from robot_controls import Robot

if __name__ == "__main__":
	robot = Robot()
	robot.color_sensor()
