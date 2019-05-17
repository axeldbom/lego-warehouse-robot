#!/usr/bin/env python3
import ev3dev.ev3 as ev3
from ev3dev2.motor import *
from time import sleep

class Robot:
# Constructor
    def __init__(self, speed, turn_speed):
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
        self.speed = speed
        self.turn_speed = turn_speed
        self.drive_duration = 0.7
        self.turn_duration = 0.25

        # initiate individual motors
        self.mm = MediumMotor(OUTPUT_A)
        self.hook_speed = 25
        
    def hook_package(self):   
        # if currently carrying a package, lift the hook. else lower the hook
        #if not self.package:
            self.mm.on(-self.hook_speed)
            self.mm.wait_until_not_moving()
            self.package = True

    def unhook_package(self):
        #if self.package:
            self.mm.on(self.hook_speed)
            self.mm.wait_until_not_moving()
            self.package = False
    
    def drive_forward(self):
        self.steer_pair.on_for_seconds(0, self.speed, self.drive_duration, brake=False, block=False)

    def drive_backwards(self):
        self.steer_pair.on_for_seconds(0, -self.speed, self.drive_duration, brake=False, block=False)
    
    def turn_right(self):
        self.steer_pair.on_for_seconds(100, self.turn_speed, self.turn_duration, brake=False, block=False)

    def turn_left(self):
        self.steer_pair.on_for_seconds(-100, self.turn_speed, self.turn_duration, brake=False, block=False)

    def tank_stop(self):
        self.tank_pair.off()

    def color_sensor(self):
        for i in range(0,100):
            print(self.cs.value())
            time.sleep(0.5)
    
    def stop(self):
        self.steer_pair.off()
        
    def turn_90(self):
        self.steer_pair.on_for_degrees(100, self.speed, -170, brake=False, block=True)
        
    def turn_180(self):
        self.steer_pair.on_for_degrees(100, self.speed, -340, brake=False, block=True)
