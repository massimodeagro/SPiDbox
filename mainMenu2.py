# -*- coding: utf-8 -*-
"""
SkinnerBox standalone version

starting Menu

@author: Massimo De Agrò
"""
import logging # for logging info and errors
import datetime

#modules for Screen
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL import ImageFont #load fonts
import Adafruit_ADS1x15 #read photo


import RPi.GPIO as GPIO

import time

#load folders
import os

#custom modules
import pin
import icons
from lists import subjs, loadsubjs
import photo

#programs
from habitScreen import habit
from trainScreen import trainS
from trainNoScreen import trainNS
from rotary import rothread

def pixelart (drawobj,pic,offset,neg):
    if neg ==1:
        col1="black"
        col2="white"
    else:
        col1="white"
        col2="black"
    for y, row in enumerate(pic):
        for x, cell in enumerate(row):
            if cell == 1:
                drawobj.point((x+1+offset[0],y+1+offset[1]), fill=col1)
            if cell == 0:
                drawobj.point((x+1+offset[0],y+1+offset[1]), fill=col2)
  
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",16)
fontT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",15)

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)
adc = Adafruit_ADS1x15.ADS1115(address=0x48) #photoresistor I2C


tabs = ['launch','settings']
testes = ['back','habituation','trainLR','trainXO']
setups = ['back','prime','clean', 'resistors','subjs','turn off']


W, H = (128,64)

select = 0
case = 0
casechange=0

with canvas(device) as draw:
    pixelart(draw,icons.logo,(0,0),0)
time.sleep(2)

while True:
    with canvas(device) as draw:
        for n, line in enumerate(tabs):
            draw.text((17,24+(n*20)-(case*20)), line, font=font, fill="white")
            pixelart(draw,icons.arrow,(0,26),0)
    tout = rothread(pin.cl,pin.dt,pin.sw)
    if tout!=0:
        case+=tout
        logging.info('Rotated the knob')
        if case<0:
            case=0
        elif case>len(tabs)-1:
            case=len(tabs)-1
    else:
        logging.info('Clicked')
        time.sleep(0.3)
        #%% launchables
        if case==0:
            logging.info('Got in launch menu')
            case=0
            while True:
                with canvas(device) as draw:
                    for n, line in enumerate(testes):
                        draw.text((17,24+(n*20)-(case*20)), line, font=font, fill="white")
                        pixelart(draw,icons.arrow,(0,26),0)
                tout = rothread(pin.cl,pin.dt,pin.sw)
                if tout!=0:
                    logging.info('Rotated the knob')
                    case+=tout
                    if case<0:
                        case=0
                    elif case>len(testes)-1:
                        case=len(testes)-1
                else:
                    logging.info('Clicked')
                    time.sleep(0.3)    
                    if case == 0:
                        logging.info('Back to start menu')
                        case = 0
                        break
                    elif case ==1:
                        logging.info('Got in screen habit mode')
                        case=0
                        while True:
                            with canvas(device) as draw:
                                for n, line in enumerate(subjs):
                                    draw.rectangle(((0,0),(128,20)),"white")
                                    draw.text((6,0), 'subject', font=fontT, fill="black")
                                    draw.text((17,24+(n*20)-(case*20)), line, font=font, fill="white")
                                    pixelart(draw,icons.arrow,(0,26),0)
                            tout = rothread(pin.cl,pin.dt,pin.sw)
                            if tout!=0:
                                logging.info('Rotated the knob')
                                case+=tout
                                if case<0:
                                    case=0
                                elif case>len(subjs)-1:
                                    case=len(subjs)-1
                            else:
                                logging.info('Clicked')
                                time.sleep(0.3)
                                name = subjs[case]
                                break
                        if name!='back':
                            testnum = 1
                            while True:
                                with canvas(device) as draw:
                                    draw.rectangle(((0,0),(128,20)),"white")
                                    draw.text((6,0), 'habitS num', font=fontT, fill="Black")
                                    draw.text((60,26), str(testnum), font=font, fill="white")
                                tout = rothread(pin.cl,pin.dt,pin.sw)
                                if tout!=0:
                                    logging.info('Rotated the knob')
                                    testnum+=tout
                                else:
                                    logging.info('Clicked')
                                    time.sleep(0.3)
                                    test = str(testnum)
                                    break
                            with canvas(device) as draw:
                                draw.rectangle(((0,0),(128,64)),"white")
                                draw.text((0,20), name+'_habitS_'+str(testnum), font=font, fill="black")
                            time.sleep(2)
                                        
                            logging.info('Starting Screen Habit')
                            start=datetime.datetime.now()
                            habit(name,test,start,canvas, device,font, fontT)                            
                    
                    elif case ==2:
                        logging.info('Got in left and right mode')
                        case=0
                        while True:
                            with canvas(device) as draw:
                                for n, line in enumerate(['left','right']):
                                    draw.rectangle(((0,0),(128,20)),"white")
                                    draw.text((6,0), 'correct side', font=fontT, fill="black")
                                    draw.text((17,24+(n*20)-(case*20)), line, font=font, fill="white")
                                    pixelart(draw,icons.arrow,(0,26),0)
                            tout = rothread(pin.cl,pin.dt,pin.sw)
                            if tout!=0:
                                logging.info('Rotated the knob')
                                case+=tout
                                if case<0:
                                    case=0
                                elif case>len(['left','right'])-1:
                                    case=len(['left','right'])-1
                            else:
                                logging.info('Clicked')
                                time.sleep(0.3)
                                side = ['left','right'][case]
                                break
                        while True:
                            with canvas(device) as draw:
                                for n, line in enumerate(subjs):
                                    draw.rectangle(((0,0),(128,20)),"white")
                                    draw.text((6,0), 'subject', font=fontT, fill="black")
                                    draw.text((17,24+(n*20)-(case*20)), line, font=font, fill="white")
                                    pixelart(draw,icons.arrow,(0,26),0)
                            tout = rothread(pin.cl,pin.dt,pin.sw)
                            if tout!=0:
                                logging.info('Rotated the knob')
                                case+=tout
                                if case<0:
                                    case=0
                                elif case>len(subjs)-1:
                                    case=len(subjs)-1
                            else:
                                logging.info('Clicked')
                                time.sleep(0.3)
                                name = subjs[case]
                                break
                        if name!='back':
                            testnum = 1
                            while True:
                                with canvas(device) as draw:
                                    draw.rectangle(((0,0),(128,20)),"white")
                                    draw.text((6,0), 'trainLR num', font=fontT, fill="Black")
                                    draw.text((60,26), str(testnum), font=font, fill="white")
                                tout = rothread(pin.cl,pin.dt,pin.sw)
                                if tout!=0:
                                    logging.info('Rotated the knob')
                                    testnum+=tout
                                else:
                                    logging.info('Clicked')
                                    time.sleep(0.3)
                                    test = str(testnum)
                                    break
                            with canvas(device) as draw:
                                draw.rectangle(((0,0),(128,64)),"white")
                                draw.text((0,20), name+'_trainLR_'+str(testnum), font=font, fill="black")
                            time.sleep(2)
                            
                            logging.info('Started train screen')
                            start=datetime.datetime.now()
                            trainNS(name,test,side,start,canvas, device,font, fontT)  
                    elif case ==3:
                        logging.info('Got in X and O mode')
                        case=0
                        while True:
                            with canvas(device) as draw:
                                for n, line in enumerate(['X','O']):
                                    draw.rectangle(((0,0),(128,20)),"white")
                                    draw.text((6,0), 'correct shape', font=fontT, fill="black")
                                    draw.text((17,24+(n*20)-(case*20)), line, font=font, fill="white")
                                    pixelart(draw,icons.arrow,(0,26),0)
                            tout = rothread(pin.cl,pin.dt,pin.sw)
                            if tout!=0:
                                logging.info('Rotated the knob')
                                case+=tout
                                if case<0:
                                    case=0
                                elif case>len(['X','O'])-1:
                                    case=len(['X','O'])-1
                            else:
                                logging.info('Clicked')
                                time.sleep(0.3)
                                shape = ['X','O'][case]
                                break
                        while True:
                            with canvas(device) as draw:
                                for n, line in enumerate(subjs):
                                    draw.rectangle(((0,0),(128,20)),"white")
                                    draw.text((6,0), 'subject', font=fontT, fill="black")
                                    draw.text((17,24+(n*20)-(case*20)), line, font=font, fill="white")
                                    pixelart(draw,icons.arrow,(0,26),0)
                            tout = rothread(pin.cl,pin.dt,pin.sw)
                            if tout!=0:
                                logging.info('Rotated the knob')
                                case+=tout
                                if case<0:
                                    case=0
                                elif case>len(subjs)-1:
                                    case=len(subjs)-1
                            else:
                                logging.info('Clicked')
                                time.sleep(0.3)
                                name = subjs[case]
                                break
                        if name!='back':
                            testnum = 1
                            while True:
                                with canvas(device) as draw:
                                    draw.rectangle(((0,0),(128,20)),"white")
                                    draw.text((6,0), 'trainXO num', font=fontT, fill="Black")
                                    draw.text((60,26), str(testnum), font=font, fill="white")
                                tout = rothread(pin.cl,pin.dt,pin.sw)
                                if tout!=0:
                                    logging.info('Rotated the knob')
                                    testnum+=tout
                                else:
                                    logging.info('Clicked')
                                    time.sleep(0.3)
                                    test = str(testnum)
                                    break
                            with canvas(device) as draw:
                                draw.rectangle(((0,0),(128,64)),"white")
                                draw.text((0,20), name+'_trainXO_'+str(testnum), font=font, fill="black")
                            time.sleep(2)
                            
                            logging.info('Started train screen')
                            start=datetime.datetime.now()
                            trainS(name,test,shape,start,canvas, device,font, fontT)               
        #%% settings                       
        elif case==1:
            case=0
            while True:
                with canvas(device) as draw:
                    for n, line in enumerate(setups):
                        draw.text((17,24+(n*20)-(case*20)), line, font=font, fill="white")
                        pixelart(draw,icons.arrow,(0,26),0)
                tout = rothread(pin.cl,pin.dt,pin.sw)
                if tout!=0:
                    case+=tout
                    if case<0:
                        case=0
                    elif case>len(setups)-1:
                        case=len(setups)-1
                else:
                    time.sleep(0.3) 
                    if case == 0:
                        case = 0
                        break
                    elif case ==1:
                        with canvas(device) as draw:
                            draw.rectangle(((0,0),(128,20)),fill='white')
                            draw.text((0,0), 'priming pump', font=fontT, fill="black")
                            draw.text((0,25), 'press ok to stop', font=font, fill="white") 
                        while True:
                            GPIO.output(pin.dc, GPIO.HIGH)
                            GPIO.output(pin.stp,GPIO.HIGH)
                            time.sleep(0.001)
                            GPIO.output(pin.stp,GPIO.LOW)
                            time.sleep(0.001)
                            if not GPIO.input(pin.sw):
                                time.sleep(0.3)
                                GPIO.output(pin.dc, GPIO.LOW)
                                break
        
                        with canvas(device) as draw:
                            draw.rectangle(((0,0),(128,20)),fill='white')
                            draw.text((0,0), 'fine tune pump', font=fontT, fill="black")
                            draw.text((0,25), 'press ok to stop', font=font, fill="white") 
                        
                        while True:
                            tout = rothread(pin.cl,pin.dt,pin.sw)
                            if tout!=0:
                                if tout>0:
                                    GPIO.output(pin.stp,GPIO.HIGH)
                                    time.sleep(0.001)
                                    GPIO.output(pin.stp,GPIO.LOW)
                                    time.sleep(0.001)
                                elif tout<0:
                                    GPIO.output(pin.clk,GPIO.HIGH)
                                    GPIO.output(pin.stp,GPIO.HIGH)
                                    time.sleep(0.001)
                                    GPIO.output(pin.stp,GPIO.LOW)
                                    time.sleep(0.001)
                                    GPIO.output(pin.clk,GPIO.LOW)
                            else:
                                time.sleep(0.3)
                                break  
                        GPIO.output(pin.dc, GPIO.HIGH)
                        time.sleep(0.8)
                        GPIO.output(pin.dc, GPIO.LOW)
                        
                    elif case ==2:
                        with canvas(device) as draw:
                            draw.rectangle(((0,0),(128,20)),fill='white')
                            draw.text((0,0), 'cleaning pump', font=fontT, fill="black")
                            draw.text((0,25), 'press ok to stop', font=font, fill="white") 
                        while True:
                            GPIO.output(pin.dc, GPIO.HIGH)
                            GPIO.output(pin.stp,GPIO.HIGH)
                            time.sleep(0.001)
                            GPIO.output(pin.stp,GPIO.LOW)
                            time.sleep(0.001)
                            if not GPIO.input(pin.sw):
                                time.sleep(0.3)
                                GPIO.output(pin.dc, GPIO.LOW)
                                break                            
                    elif case == 3:
                        adc_filtL = adc.read_adc(pin.photoL, gain=1)
                        adc_EavgL = adc_filtL*1.0
                        adc_filtR = adc.read_adc(pin.photoR, gain=1)
                        adc_EavgR = adc_filtR*1.0
                        while True:
                            L, adc_filtL = photo.binphoto (adc, pin.photoL, photo.filt_c,photo.tresh_c,adc_filtL,adc_EavgL)
                            R, adc_filtR = photo.binphoto (adc, pin.photoR, photo.filt_c,photo.tresh_c,adc_filtR,adc_EavgR)
                            if L == 0:
                                adc_EavgL = photo.Eavgcalc(adc_filtL, adc_EavgL,photo.Eavg_c)
                                print("gothere")
                            if R == 0:
                                adc_EavgR = photo.Eavgcalc(adc_filtR, adc_EavgR,photo.Eavg_c)
                            
                            print (str(adc_filtL)+" - "+str(adc_EavgL)+" - "+str(L) )

                            with canvas(device) as draw:
                                draw.rectangle(((0,0),(128,20)),fill='white')
                                draw.text((0,0), 'Testing Resistors', font=fontT, fill="black")
                                draw.text((20,25), 'L', font=font, fill="white") 
                                draw.text((108,25), 'R', font=font, fill="white") 
                                draw.text((20,50), str(L), font=font, fill="white") 
                                draw.text((108,50), str(R), font=font, fill="white") 
                            if not GPIO.input(pin.sw):
                                time.sleep(0.3)
                                break  
                    elif case == 4:
                        letters = ['a','b','c','d','e','f','g','h','i',
                                   'j','k','l','m','n','o','p','q','r',
                                   's','t','u','v','w','x','y','z','_']
                        currletter = 0
                        spot = 0
                        name='a'
                        while True:
                            name = list(name)
                            name[spot] = letters[currletter]
                            name = ''.join(name)
                            with canvas(device) as draw:
                                w, h = draw.textsize('new subj')
                                draw.text((25,0), 'new subj', font=fontT, fill="white")
                                w, h = draw.textsize(name)
                                draw.text(((W-w)/2,(H-h)/2), name, font=font, fill="white")
                            tout = rothread(pin.cl,pin.dt,pin.sw)
                            if tout[0]!=0:
                                currletter+=tout[0]
                                if currletter<0:
                                    currletter=len(letters)-1
                                elif currletter>len(letters)-1:
                                    currletter=0
                                name = list(name)
                                name[spot] = letters[currletter]
                                name = ''.join(name)
                            else:
                                if letters[currletter] == '_':
                                    if name!='_':
                                        name = name[0:-1]
                                        os.makedirs('subjs/'+name)
                                        os.makedirs('subjs/'+name+'/video')
                                        os.makedirs('subjs/'+name+'/logs')
                                        subjs = loadsubjs()
                                    time.sleep(0.3)
                                    
                                    break
                                else:
                                    spot += 1
                                    if spot+1>len(name):
                                        name = name+'a'
                                        time.sleep(0.3)
                                    
                    elif case == 5:
                        os.system('sudo shutdown')