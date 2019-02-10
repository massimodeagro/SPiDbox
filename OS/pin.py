# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 19:14:13 2017

@author: frogmax
"""

import RPi.GPIO as GPIO
dc = 37
    
stp = 15
clk = 16

#
M1 = 40
M2 = 38
M3 = 36

# rotary
cl = 8
dt = 10
sw = 12
ok = 12

led = 35

#photoresistors channels on i2c
photoL = 0
photoR = 1

GPIO.setmode(GPIO.BOARD) #set board

#set buttons
GPIO.setup(cl,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(dt,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(sw,GPIO.IN,pull_up_down=GPIO.PUD_UP)

GPIO.setup(led,GPIO.OUT)
# set dc motors
GPIO.setup(dc,GPIO.OUT)
GPIO.output(dc,GPIO.LOW)

#set peristaltic
GPIO.setup(stp,GPIO.OUT)
GPIO.output(stp,GPIO.LOW)

GPIO.setup(clk,GPIO.OUT)
GPIO.output(clk,GPIO.LOW)

#setphoto
#GPIO.setup(photoL, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(photoR, GPIO.IN, pull_up_down=GPIO.PUD_UP)
