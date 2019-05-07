#!/usr/bin/env python3
import ev3dev.ev3 as ev3
from ev3dev2.motor import *
from time import sleep

class FollowLine:
    # Constructor
    def __init__(self):
        self.manual_control = False
        self.button = ev3.Button()
        self.packet = False

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
        
    def hook(self):   
        # if currently carrying a package, lift the hook. else lower the hook
        if self.packet:
            self.mm.on(self.hook_speed)
            self.mm.wait_until_not_moving()
            self.packet = False
            return
        else:
            self.mm.on(-self.hook_speed)
            self.mm.wait_until_not_moving()
            self.packet = True
            return

    def drive_forward():
        self.steer_pair.on(0, 50)

    def drive_backwards():
        self.steer_pair.on(0, -50)
    
    def turn_right():
        self.steer_pair.on(100, 25)

    def turn_left():
        self.steer_pair.on(-100, 25)

    def tank_stop():
        self.tank_pair.off()

    def color_sensor():
        for i in range(0,100):
            print(cs.value())
            time.sleep(0.5)
    
    def stop(self):
        self.steer_pair.off()
        
    def main(self):

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
        while not self.manual_control:

            if self.button.any(): exit()
            
            if self.ts.value():
                self.packet = True
                self.stop()
                self.hook()
                
            # package stuff
            distance = self.us.value()
            print("distance = ", distance)
            if distance < 40 and not self.packet:
                self.stop()
                self.hook()
            
            # PID stuff
            error = target_value - self.cs.value()
            
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
                self.steer_pair.on_for_seconds(0, self.speed, Ts, brake=False, block=False)
            else:
                if u < -100: u = -100
                elif u > 100: u = 100
                self.steer_pair.on_for_seconds(u, self.speed, Ts, brake=False, block=False)
                # tank_pair.on_for_seconds(speed * (1 + u/100), speed * (1 - u/100), Ts, brake=False, Block=False)
            previous_error = error

# Main
if __name__ == "__main__":
    robot = FollowLine()
    robot.main()
