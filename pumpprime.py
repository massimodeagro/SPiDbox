# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 19:50:43 2017

@author: frogmax
"""
import RPi.GPIO as GPIO
import time

import pin
def pumpprime(canvas, device, font, fontT, dc,stp,clk):
    GPIO.output(dc, GPIO.HIGH)
    with canvas(device) as draw:
        draw.text((20,0), 'priming pump', font=fontT, fill="white")
        draw.text((23,24), 'press O to stop', font=font, fill="white")
            
    while True:
        GPIO.output(stp,GPIO.HIGH)
        time.sleep(0.0025)
        GPIO.output(stp,GPIO.LOW)
        time.sleep(0.0025)
        if not GPIO.input(pin.ok):
            break
    GPIO.output(dc, GPIO.LOW)
def finetune(canvas, device, font, fontT, dc, stp, clk):
    with canvas(device) as draw:
        draw.text((20,0), 'fine tuneing', font=fontT, fill="white")
        draw.text((15,16), '^ = 1 step fwd', font=font, fill="white")
        draw.text((15,33), 'v = 1 step bkw', font=font, fill="white")
        draw.text((22,50), 'O to quit', font=font, fill="white")
    while True:
        if not GPIO.input(pin.down):
            GPIO.output(clk,GPIO.HIGH)
            GPIO.output(stp,GPIO.HIGH)
            time.sleep(0.05)
            GPIO.output(stp,GPIO.LOW)
            time.sleep(0.05)
            GPIO.output(clk,GPIO.LOW)
        if not GPIO.input(pin.up):
            GPIO.output(stp,GPIO.HIGH)
            time.sleep(0.05)
            GPIO.output(stp,GPIO.LOW)
            time.sleep(0.05)
        if not GPIO.input(pin.ok):
            break
    