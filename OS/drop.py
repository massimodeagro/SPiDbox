#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
SkinnerBox standalone version

module of the drop control
This is called by main program

@author: Massimo De Agrò
"""

import RPi.GPIO as GPIO
import time

def dcmove(dcmotor_pin,howmuch):  
    GPIO.output(dcmotor_pin,GPIO.HIGH)
    time.sleep(howmuch)
    GPIO.output(dcmotor_pin,GPIO.LOW)
        
def stepmove(step_pin,dir_pin,reverse,steps,position):
    if reverse==1:
        GPIO.output(dir_pin,GPIO.HIGH)
    for i in range(steps):
        GPIO.output(step_pin,GPIO.HIGH)
        time.sleep(0.01)
        GPIO.output(step_pin,GPIO.LOW)
        time.sleep(0.01)
        position+=1
        if position==19 or position==52 or position==119 or position==152:
            for i in range(14):
                GPIO.output(step_pin,GPIO.HIGH)
                time.sleep(0.01)
                GPIO.output(step_pin,GPIO.LOW)
                time.sleep(0.01)
                position+=1
        if position==85 or position==185:
            for i in range(15):
                GPIO.output(step_pin,GPIO.HIGH)
                time.sleep(0.01)
                GPIO.output(step_pin,GPIO.LOW)
                time.sleep(0.01)
                position+=1
        if position==200:
            position=0

def postrack(steps, position):
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

def onedrop(step_pin):
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
