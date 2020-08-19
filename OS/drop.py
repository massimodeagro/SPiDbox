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
        #this catches the points in which the pumps sucks instead of pushing, fastly skipping 14 steps
        if position==19 or position==52 or position==119 or position==152: 
            for i in range(14):
                GPIO.output(step_pin,GPIO.HIGH)
                time.sleep(0.01)
                GPIO.output(step_pin,GPIO.LOW)
                time.sleep(0.01)
                position+=1
        if position==85 or position==185: #or 15 steps, since 100/3 is 33+33+34
            for i in range(15):
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
        if position==19 or position==52 or position==119 or position==152:
            for i in range(14):
                position+=1
        if position==85 or position==185:
            for i in range(15):
                position+=1
        if position==200:
            position=0
    return position

def onedrop(step_pin): #formula already specified to give one drop. However, it depends on the size of the holder, tubes, etc.
    for i in range(85):
        GPIO.output(step_pin,GPIO.HIGH)
        time.sleep(0.01)
        GPIO.output(step_pin,GPIO.LOW)
        time.sleep(0.01)
    for i in range(15):
        GPIO.output(step_pin,GPIO.HIGH)
        time.sleep(0.05)
        GPIO.output(step_pin,GPIO.LOW)
        time.sleep(0.05)
