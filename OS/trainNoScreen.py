"""
This file contains the habituation procedure
it is called by the main menu
"""

# Import required libraries
import RPi.GPIO as GPIO
from threading import Thread
import picamera
import os
import datetime

import epd2in9
from PIL import Image

# Import custom modules
import drop
#import vibr
#import MPR121 as cap
import pin

#training procedure with the two sensors
def trainNS(name,test,cside,start,canvas, device,font, fontT):
    print ("in the function") #to debug
    from time import time as getsecs
    from time import sleep
    #%%#####################################################################%%#
    #-------------------------------DEFINITIONS-------------------------------#
    ###########################################################################
    ##** LOGFILE **##
    print ("after import")
    logname = 'subjs/'+name+'/logs/'+name+'_test_'+test+'.csv'
    time = (datetime.datetime.now()-start).total_seconds()                                    
    date = str(datetime.datetime.now())
    with open(logname,'w') as log:
        log.write('datetime,time,event\n')                                     
        log.write(date+','+str(time)+',TestStart\n')    
    print ("after logfile")
    
    #start the video
    cam = picamera.PiCamera()
    cam.resolution = (1296,972)
    cam.framerate = 5
    cam.start_recording('subjs/'+name+'/video/'+name+'_test_'+test+'.h264')

    epd = epd2in9.EPD()
    epd.init(epd.lut_partial_update)
    image = Image.open('screenImages/W.bmp') 
    epd.set_frame_memory(image, 0, 0)
    epd.display_frame()
    #%%#####################################################################%%#
    #------------------------------STARTING PROGRAM---------------------------#
    #
    #definition of state variables
    c=0
    w=0                                                                       #
    killing = False
    Cpressed = False
    Wpressed = False

    pos = 0  #current motor position                                          #
    delivering = False                                                        #
    dropPresent = False                                                       #
    stepsnum = 19 #number of steps for a drop
    #                                                                         #
    #-------------------------------------------------------------------------#
    ###########################################################################
    
    ###################################################################
    #-|-|-|-|-|-|-|-|-PRIME SCREEN AND BUTTONS|-|-|-|-|-|-|-|-|-|-|-|-#
    #                                                                 #
    #make sure the screen is white
    W = Image.open('screenImages/W.bmp')
    B = Image.open('screenImages/B.bmp')
    if cside == 'left':
        photoCORRECT = pin.photoL
        photoWRONG = pin.photoR
    else:
        photoCORRECT = pin.photoR
        photoWRONG = pin.photoL
    epd.set_frame_memory(B, 0, 0)
    epd.display_frame()
    epd.set_frame_memory(B, 0, 0)
    epd.display_frame()        
    epd.set_frame_memory(W, 0, 0)
    epd.display_frame()
    epd.set_frame_memory(W, 0, 0)
    epd.display_frame()

    #                                                                 #
    #-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-#
    
    #%%########################################################################
    #--------------------------------MAIN LOOP--------------------------------#
    while (True):
        now = getsecs()
        #%%/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/%%#
        #-------------------------FOR CORRECT RESISTOR------------------------#
        #                                                                     #
        if not Cpressed: #if currently the correct button was not being pressed
            if GPIO.input(photoCORRECT): #but now it is
                print ("Cpressed")
                Cpressed = True #change state
                #logging                                                  #
                time = (datetime.datetime.now()-start).total_seconds()    #
                date = str(datetime.datetime.now())                       #
                with open(logname,'a') as log:
                    log.write(date+','+str(time)+',Cpressed\n')           #
                    c+=1
                    #   #   #   #   #   #   #   #   #   #   #   #   #   #     #
                    #          correct button has become pressed        #     #
                    #                                                   #     #
                    if not delivering and not dropPresent:              #     #
                        delivering = True # delivering state            #     #
                        #deliver the drop                               #     #
                        deliverer=Thread(name='Perist',target=drop.stepmove,  #
                                    args=(pin.stp,pin.clk,0,stepsnum,pos))    # 
                        deliverer.start() # deliver a drop              #     #
                        pos = drop.postrack(stepsnum,pos)               #     #
                    #                       end                         #     #                    
                    #   #   #   #   #   #   #   #   #   #   #   #   #   #     #                    
                   
        if Cpressed: #if is being pressed                                     #
           if not GPIO.input(photoCORRECT): #but then is not
                print ("Crelease")
                Cpressed=False
                #logging                                                      #
                time = (datetime.datetime.now()-start).total_seconds()        #
                date = str(datetime.datetime.now())                           #
                with open(logname,'a') as log:
                    log.write(date+','+str(time)+',Crelease\n')               #
                waitforRetract = getsecs() #start waiting for retraction      #                        
        #                                                                     #
        #---------------------------------------------------------------------#
        #/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/#
        
        
        #%%/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/%%#
        #--------------------------FOR WRONG RESISTOR-------------------------#
        #                                                                     #
        #if the wrong is pressed you need to do nothing but remove the drop if is currently present
        if not Wpressed:                                                      #
            if GPIO.input(photoWRONG):                                        #
                Wpressed=True                                                 #
                print ("Wpressed")                                            #
                time = (datetime.datetime.now()-start).total_seconds()        #
                date = str(datetime.datetime.now())                           #
                with open(logname,'a') as log:                                #
                    log.write(date+','+str(time)+',Wpressed\n')               #
                w+=1
                #   #   #   #   #   #   #   #   #   #   #   #   #   #         #
                #           wrong button has become pressed         #         #
                #                                                   #         #
                if dropPresent: #if drop is present, remove
                    retracter=Thread(name='suck',target=drop.dcmove,args=(pin.dc,3))
                    retracter.start()                                         #
                    dropPresent = False                                       #
                    #logging                                                  #
                    time = (datetime.datetime.now()-start).total_seconds()    #
                    date = str(datetime.datetime.now())                       #
                    with open(logname,'a') as log:
                        log.write(date+','+str(time)+',DropRetract\n')        #
                #                                                   #         #                    
                #                       end                         #         #
                #   #   #   #   #   #   #   #   #   #   #   #   #   #         #
        if Wpressed: #if is being pressed                                     #
            if not GPIO.input(photoWRONG): #and then is not
                Wpressed=False   #change state
                print ("Wrelease")                                        #
                #logging                                                  #
                time = (datetime.datetime.now()-start).total_seconds()    #
                date = str(datetime.datetime.now())                       #
                with open(logname,'a') as log:
                    log.write(date+','+str(time)+',Wrelease\n')           #
                    
        #                                                                     #
        #---------------------------------------------------------------------#
        #/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/#
        
        
        #%%=================================================================%%#
        #--------------------if I am delivering the drop----------------------#
        #                                                                     #        
        if delivering:                                                        #
            if not deliverer.isAlive(): #when i have finished delivering      #
                print ("delivered")
                #logging                                                      #
                time = (datetime.datetime.now()-start).total_seconds()        #
                date = str(datetime.datetime.now())                           #
                with open(logname,'a') as log:
                    log.write(date+','+str(time)+',DropDeliv\n')              #
                dropPresent = True                                            #
                delivering = False                                            #
                waitforRetract = getsecs() #start waiting for retraction      #
        #                                                                     #
        #---------------------------------------------------------------------#
        #=====================================================================#
                
        
        #%%*****************************************************************%%#
        #------------------------if the drop is present-----------------------#
        #                                                                     #
        if dropPresent:                                                       #
            now = getsecs() #now time                                         #
            nodrank = now-waitforRetract >= 30                                #
            if nodrank and not Cpressed: #if time is over                     #
                retracter=Thread(name='suck',target=drop.dcmove,              #
                                 args=(pin.dc,3))                             #
                retracter.start()                                             #
                dropPresent = False
                #logging                                                      #
                time = (datetime.datetime.now()-start).total_seconds()        #
                date = str(datetime.datetime.now())                           #
                with open(logname,'a') as log:
                    log.write(date+','+str(time)+',DropRetract\n')            #
        #                                                                     #
        #---------------------------------------------------------------------#        
        #*********************************************************************#
        #see habituation file for an explanation of the following lines. they control the turning off routine
        if not killing:
            elapsed = str(datetime.datetime.now()-start)
            elapsed = elapsed.split('.')[0]
            with canvas(device) as draw:
                draw.text((30,0), 'testing', font=fontT, fill="white")
                draw.text((23,48), str(elapsed), font=font, fill="white")
                draw.text((23,24), 'c: '+str(c)+' w: '+str(w),font=font, fill="white")
            if not GPIO.input(pin.ok):
                killing=True
                waittoclose = getsecs()
                with canvas(device) as draw:
                    draw.text((30,0), 'testing', font=fontT, fill="white")
                    draw.text((0,26), 'press again to quit', font=font, fill="white")
                    sleep(0.5)
        if killing:
            if getsecs()-waittoclose<15:
                if not GPIO.input(pin.ok):
                    time = (datetime.datetime.now()-start).total_seconds()                                    
                    date = str(datetime.datetime.now())      
                    with open(logname,'a') as log:
                        log.write(date+','+str(time)+',TestOver\n')                 
                    cam.stop_recording()
                    cam.close()
                    with canvas(device) as draw:
                        draw.text((30,0), 'testing', font=fontT, fill="white")
                        draw.text((0,26), 'cleanup...', font=font, fill="white")
                        draw.text((0,42), 'do not unplug', font=font, fill="white")
                    sleep(5)
                    break
            else:
                killing=False

    with canvas(device) as draw:
        draw.text((0,26), 'rebooting', font=font, fill="white")
        draw.text((0,42), 'do not unplug', font=font, fill="white")
    os.system("sudo reboot")
