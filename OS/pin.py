"""
SPiDbox 

this file contains the definition for all the pins of the system

@author: Massimo De Agro'
"""

import RPi.GPIO as GPIO #module that control the pins

dc = 37 #DC peristaltic pump pin
 
#Stepper peristaltic pump
stp = 15 #pin that drives motor steps
clk = 16 #pin for direction

# values to make the stepper motor do microsteps. These are generally turned off
M1 = 40
M2 = 38
M3 = 36

# rotary encoder
cl = 8 #clock pin of the rotary
dt = 10 #dt pin of the rotary
sw = 12 #switch. defined also as ok for clarity in some formulas
ok = 12

led = 35 # not used anymore

#photoresistors channels on i2c
photoL = 0
photoR = 1

GPIO.setmode(GPIO.BOARD) #set board mode

#set rotor pins as input
GPIO.setup(cl,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(dt,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(sw,GPIO.IN,pull_up_down=GPIO.PUD_UP)

GPIO.setup(led,GPIO.OUT) #not used anymore

# set dc motor as output and then put it low
GPIO.setup(dc,GPIO.OUT)
GPIO.output(dc,GPIO.LOW)

#set peristaltic as out and then put it low
GPIO.setup(stp,GPIO.OUT)
GPIO.output(stp,GPIO.LOW)

GPIO.setup(clk,GPIO.OUT)
GPIO.output(clk,GPIO.LOW)

#old photoresistor method. I keep it for transparency
#GPIO.setup(photoL, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(photoR, GPIO.IN, pull_up_down=GPIO.PUD_UP)
