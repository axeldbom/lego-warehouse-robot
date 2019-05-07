#!/usr/bin/env python3
import ev3dev.ev3 as ev3
from ev3dev2.motor import *
from time import sleep

class Robot:
# Constructor
    def __init__(self):
        self.manual_control = False
        self.button = ev3.Button()
        self.package = False

        # initiate sensors
        self.cs = ev3.ColorSensor()
        self.us = ev3.UltrasonicSensor()
        self.ts = ev3.TouchSensor()
        
        self.cs.mode = 'COL-REFLECT'
        self.us.mode = 'US-DIST-CM'  # actually measures mm and not cm

        # initiate motor pairs
        self.tank_pair = MoveTank(OUTPUT_B, OUTPUT_C)
        self.steer_pair = MoveSteering(OUTPUT_B, OUTPUT_C)
        self.speed = 25

        # initiate individual motors
        self.mm = MediumMotor(OUTPUT_A)
        self.hook_speed = 50
        
    def hook_package(self):   
        # if currently carrying a package, lift the hook. else lower the hook
        if self.package:
            self.mm.on(self.hook_speed)
            self.mm.wait_until_not_moving()
            self.package = False
            return
        else:
            self.mm.on(-self.hook_speed)
            self.mm.wait_until_not_moving()
            self.package = True

    def drive_forward(self):
        self.steer_pair.on_for_seconds(0, 25, 0.5)

    def drive_backwards(self):
        self.steer_pair.on_for_seconds(0, -25, 0.5)
    
    def turn_right(self):
        self.steer_pair.on_for_seconds(100, 25, 0.5)

    def turn_left(self):
        self.steer_pair.on_for_seconds(-100, 25, 0.5)

    def tank_stop(self):
        self.tank_pair.off()

    def color_sensor(self):
        for i in range(0,100):
            print(cs.value())
            time.sleep(0.5)
    
    def stop(self):
        self.steer_pair.off()

