"""
SPiDbox software

This file should be called by the Raspberry Pi automatically at startup. 
It contains the SPiDbox menu and is responsible for calling every other files

@author: Massimo De Agrò
"""
#importing general modules
import logging # for logging info and errors

import datetime #to be unified
import time #to be unified

import os #load folders


#modules for user screen control
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL import ImageFont #load fonts

#modules to input and output
import RPi.GPIO as GPIO
import Adafruit_ADS1x15 #read I2C analog to digital converter

#custom modules
import pin #contains definitions for every pin
import icons #contains pictures used in the menu
from lists import subjs, loadsubjs #formulas to load and create subjects
import photo #contains formula for reading photosensors
from rotary import rothread #reads the rotary encored

#training procedures
from habitScreen import habit #habituation phase. No sensors, only dispenser
from trainScreen import trainS #testing phase with pictures on the screen
from trainNoScreen import trainNS #testing phase without the screen. differently coloured sensors

#define I2C modules
serial = i2c(port=1, address=0x3C) #user screen
device = ssd1306(serial) #define user screen model
W, H = (128,64) #define user screen size

adc = Adafruit_ADS1x15.ADS1115(address=0x48) #photoresistor I2C


def pixelart (drawobj,pic,offset,neg): #to draw pictures on the user screen
    if neg ==1: #negative
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
  
#load fonts
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",16)
fontT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",15)



###%%% MAIN MENU %%%###

#menu entry names
tabs = ['launch','settings'] #main entry
tests = ['back','habituation','trainLR','trainXO'] #"launch" submenu
setups = ['back','prime','clean', 'resistors','subjs','turn off'] #"settings" submenu

#creating state variable used to navigate the menu
select = 0
case = 0    #keeps track of the current menu position. it changes by rotating the knob
casechange=0

with canvas(device) as draw: #draw startup logo
    pixelart(draw,icons.logo,(0,0),0)
time.sleep(2) #show for 2 seconds

while True: #enters in an infinite loop displaying the menu
    with canvas(device) as draw: #this writes line by line all the voices from the "tabs" list
        for n, line in enumerate(tabs):
             #text is drawn according to the current case: the selected one is on the centre, the other are moved on top or bottom 
            draw.text((17,24+(n*20)-(case*20)), line, font=font, fill="white") 
            pixelart(draw,icons.arrow,(0,26),0) #draw an arrow at the centre point
    tout = rothread(pin.cl,pin.dt,pin.sw) #read the knob. this will not output until something happens (rotated or clicked)
    #for a more complete explanation see rotary.py
    if tout!=0: #it it was rotated
        case+=tout #change the case
        logging.info('Rotated the knob')
        if case<0: #if the case is now a negative number however
            case=0 #put it back at 0
        elif case>len(tabs)-1: #also, if the case number is higher than the total cases we have
            case=len(tabs)-1 #put it at that number. In this case here it will be 1
    else: #if it was clicked
        logging.info('Clicked')
        time.sleep(0.3) #debounce
        
        #here we get in the case was currently selected when we clicked. it is a deep if/elif section, catching all the possible cases
        #and acting accordingly
        #%% launchables
        if case==0: #if we clicked case 0, we get into the "launch menu
            logging.info('Got in launch menu')
            case=0 #reset case number
            while True: #infinite loop to display the new menu
                #this works exactly like the main menu.
                with canvas(device) as draw:
                    for n, line in enumerate(tests):
                        draw.text((17,24+(n*20)-(case*20)), line, font=font, fill="white")
                        pixelart(draw,icons.arrow,(0,26),0)
                tout = rothread(pin.cl,pin.dt,pin.sw)
                if tout!=0:
                    logging.info('Rotated the knob')
                    case+=tout
                    if case<0:
                        case=0
                    elif case>len(tests)-1:
                        case=len(tests)-1
                else:
                    logging.info('Clicked')
                    time.sleep(0.3)
                    #if/elif section for the various cases
                    if case == 0: #now case 0 is "back". it breaks out of the current while loop and goes up to the previous menu
                        logging.info('Back to start menu')
                        case = 0
                        break
                    elif case ==1: #case 1 launch the habituation routine
                        logging.info('Got in screen habit mode')
                        case=0 #reset case
                        while True:
                            with canvas(device) as draw: #this shows all the avalable subjects
                                for n, line in enumerate(subjs):
                                    draw.rectangle(((0,0),(128,20)),"white")
                                    draw.text((6,0), 'subject', font=fontT, fill="black")
                                    draw.text((17,24+(n*20)-(case*20)), line, font=font, fill="white")
                                    pixelart(draw,icons.arrow,(0,26),0)
                            #Now we can choose the subject
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
                        if name!='back': #if we did not click on back
                            testnum = 1 #initialize test number
                            while True:
                                with canvas(device) as draw: #show number
                                    draw.rectangle(((0,0),(128,20)),"white")
                                    draw.text((6,0), 'habitS num', font=fontT, fill="Black")
                                    draw.text((60,26), str(testnum), font=font, fill="white")
                                tout = rothread(pin.cl,pin.dt,pin.sw) #rotating increase or decrease number
                                if tout!=0:
                                    logging.info('Rotated the knob')
                                    testnum+=tout
                                else: #clicking choses the number
                                    logging.info('Clicked')
                                    time.sleep(0.3)
                                    test = str(testnum)
                                    break
                            with canvas(device) as draw: #show the decisions made until now: training routine chosen, subject and number
                                draw.rectangle(((0,0),(128,64)),"white")
                                draw.text((0,20), name+'_habitS_'+str(testnum), font=font, fill="black")
                            time.sleep(2) #show for 2 seconds
                                        
                            logging.info('Starting Screen Habit')
                            start=datetime.datetime.now() #set starting time
                            habit(name,test,start,canvas, device,font, fontT) #start the experiment. see related file                     
                    
                    #same code is more or less repeated for the other training routines, with few variations related to the
                    #experiment's needs (like decide if left or right is the correct for the current subject
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
                    #third experimental routine
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
                            
        #%% settings section. the overall structure is similar to the launchables                      
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
                    
                    #if we choose back, break from this loop
                    if case == 0:
                        break
                    #pump priming. The pump rotates continously until prompted to stop
                    elif case ==1:
                        with canvas(device) as draw:
                            draw.rectangle(((0,0),(128,20)),fill='white')
                            draw.text((0,0), 'priming pump', font=fontT, fill="black")
                            draw.text((0,25), 'press ok to stop', font=font, fill="white") 
                        while True:
                            GPIO.output(pin.dc, GPIO.HIGH) #turn on DC pump to suck liquid away
                            
                            #do one stepper pump step
                            GPIO.output(pin.stp,GPIO.HIGH) 
                            time.sleep(0.001)
                            GPIO.output(pin.stp,GPIO.LOW)
                            time.sleep(0.001)
                            
                            #if rotary encoder is clicked
                            if not GPIO.input(pin.sw):
                                time.sleep(0.3)
                                GPIO.output(pin.dc, GPIO.LOW) #turn off sucking pump
                                break #and exit from this while
        
                        with canvas(device) as draw:
                            draw.rectangle(((0,0),(128,20)),fill='white')
                            draw.text((0,0), 'fine tune pump', font=fontT, fill="black")
                            draw.text((0,25), 'press ok to stop', font=font, fill="white") 
                        
                        while True: #now, rotating the encoder rotates the pump. we want to fine tune the pump until it is in the right position
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
                    
                    #cleaning the pump works exacly as priming, but it lacks the fine tuning
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
                    
                    # to test photosensor. for an explanation of the system see photo.py
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
                    #define new subjects
                    elif case == 4:
                        letters = ['a','b','c','d','e','f','g','h','i',
                                   'j','k','l','m','n','o','p','q','r',
                                   's','t','u','v','w','x','y','z','_'] #avalable charcters
                        currletter = 0 #like case
                        spot = 0 #in what character of the name are we
                        name='a' #starting name
                        while True:
                            name = list(name)
                            name[spot] = letters[currletter] #change the character of the name selecting among letters
                            name = ''.join(name) #put the name together
                            with canvas(device) as draw: #show
                                w, h = draw.textsize('new subj')
                                draw.text((25,0), 'new subj', font=fontT, fill="white")
                                w, h = draw.textsize(name)
                                draw.text(((W-w)/2,(H-h)/2), name, font=font, fill="white")
                            tout = rothread(pin.cl,pin.dt,pin.sw)
                            if tout[0]!=0: #if rotated, change currletter
                                currletter+=tout[0]
                                if currletter<0:
                                    currletter=len(letters)-1
                                elif currletter>len(letters)-1:
                                    currletter=0
                                name = list(name)
                                name[spot] = letters[currletter]
                                name = ''.join(name)
                            else: #if clicked
                                if letters[currletter] == '_': #if i selected _, end the name
                                    if name!='_': #if the name is not just a _, create the folder and exit
                                        name = name[0:-1]
                                        os.makedirs('subjs/'+name)
                                        os.makedirs('subjs/'+name+'/video')
                                        os.makedirs('subjs/'+name+'/logs')
                                        subjs = loadsubjs()
                                    time.sleep(0.3)
                                    
                                    break
                                else: #for any other letter
                                    spot += 1 #freeze the character and go ti the next
                                    if spot+1>len(name):
                                        name = name+'a' #and add a letter
                                        time.sleep(0.3)
                    #turn off
                    elif case == 5:
                        os.system('sudo shutdown')
