#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
SkinnerBox standalone version

module of the pumps control
This is called by main program

@author: Massimo De Agro'
"""

#load modules
import RPi.GPIO as GPIO
import time

def dcmove(dcmotor_pin,howmuch):  #move the DC pump for a given amount of time
    GPIO.output(dcmotor_pin,GPIO.HIGH)
    time.sleep(howmuch)
    GPIO.output(dcmotor_pin,GPIO.LOW)
        
        
def stepmove(step_pin,dir_pin,reverse,steps,position): #move the stepper motor for a given number of steps
    if reverse==1:
        GPIO.output(dir_pin,GPIO.HIGH)
    for i in range(steps):
        GPIO.output(step_pin,GPIO.HIGH)
        time.sleep(0.01)
        GPIO.output(step_pin,GPIO.LOW)
        time.sleep(0.01)
        position+=1
        #if you are at third 3 of 6 or 6 of 6, do another step, as 200/6 is not a whole number
        if position==99 or position==199: 
            GPIO.output(step_pin,GPIO.HIGH)
            time.sleep(0.01)
            GPIO.output(step_pin,GPIO.LOW)
            time.sleep(0.01)
            position+=1
        if position==200:
            position=0

def postrack(steps, position): #this formula does the same exact steps without moving the motor. It is used to count the steps
    for i in range(steps):
        position+=1
        if position==99 or position==199:
            position+=1
        if position==200:
            position=0
    return position
