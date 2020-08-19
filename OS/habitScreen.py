"""
This file contains the habituation procedure

it is called by the main menu

"""


# Import required libraries
import RPi.GPIO as GPIO
from threading import Thread
import datetime
import random
import os 

import epd2in9
from PIL import Image

# Import custom modules
import drop
#import MPR121 as cap
import pin
    
def habit(name,test,start,canvas, device,font, fontT):
    from time import time as getsecs
    from time import sleep
    import picamera
   
    #%%#####################################################################%%#
    #-------------------------------DEFINITIONS-------------------------------#
    ###########################################################################
    ##** LOGFILE **##
    logname = 'subjs/'+name+'/logs/'+name+'_habitScreen_'+test+'.csv'
    time = (datetime.datetime.now()-start).total_seconds()                                    
    date = str(datetime.datetime.now())                                     
    with open(logname,'w') as log:
        log.write('datetime,time,event\n')                                     
        log.write(date+','+str(time)+',TestStart\n')   

    #make sure the back display is white
    epd = epd2in9.EPD()
    epd.init(epd.lut_full_update)
    image = Image.open('screenImages/W.bmp') 
    epd.set_frame_memory(image, 0, 0)
    epd.display_frame()

    #%%#####################################################################%%#
    #------------------------------STARTING PROGRAM---------------------------#
    #                                                                         #
    #State variables
    killing = False                                                           #
    delivering = False                                                        #
    dropPresent = False                                                       #                                                           #
    waitfordeliver = datetime.datetime.now() #count seconds until next delivery of drop
    
    #record with the piCamera
    cam = picamera.PiCamera()
    cam.resolution = (1296,972)
    cam.framerate = 5
    cam.start_recording('subjs/'+name+'/video/'+name+'_habitScreen_'+test+'.h264')
  
    #                                                                         #
    #-------------------------------------------------------------------------#
    ###########################################################################

    #pick a random time interval to wait before giving the drop. 
    timetowait = random.sample(range(45,91),1)[0]
    #%%########################################################################
    #--------------------------------MAIN LOOP--------------------------------#
    while (True):
        #%%/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/%%#
        #-------------------------FOR DELIVERING DROP-------------------------#
        #                                                                     #
        pos=0                                                                 #
        thismoment = datetime.datetime.now()                                  #
        waited = thismoment-waitfordeliver  #how much have I waited?
        
         # if I have waited more than timetowait and there is no drop nor i am delivering one
        if waited.total_seconds() >= timetowait and (not dropPresent or not delivering): 
            delivering = True # delivering state                              #
            #logging                                                          #
            time = (datetime.datetime.now()-start).total_seconds()            #
            date = str(datetime.datetime.now())                               #
            deliverer=Thread(name='Perist',target=drop.stepmove,              #
                        args=(pin.stp,pin.clk,0,19,pos))                      #
            deliverer.start() # deliver a drop                                #
            pos = drop.postrack(19,pos)
            waitfordeliver = datetime.datetime.now() #restart waiting         #
        #                                                                     #
        #/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/#

        #%%=================================================================%%#
        #--------------------if I am delivering the drop----------------------#
        #                                                                     #        
        if delivering:                                                        #
            if not deliverer.isAlive(): #when i have finished delivering      #
                print ('over')
                delivering = False
                #logging                                                      #
                time = (datetime.datetime.now()-start).total_seconds()        #
                date = str(datetime.datetime.now())  
                with open(logname,'a') as log:                                #
                    log.write(date+','+str(time)+',DropDeliv\n')              #
                dropPresent = True                                            #
                waitforRetract = getsecs() #start waiting for retraction      #
        #                                                                     #
        #---------------------------------------------------------------------#
        #=====================================================================#
                
        
        #%%*****************************************************************%%#
        #------------------------if the drop is present-----------------------#
        #                                                                     #
        if dropPresent:                                                       #
            now = getsecs() #now time                                         #
            nodrank = now-waitforRetract >= 35
            if nodrank: #if time is over
                #turn on dc motor in a new thread
                retracter=Thread(name='suck',target=drop.dcmove,              #
                                 args=(pin.dc,3))                             #
                retracter.start()                                             #
                dropPresent = False                                           #
                #logging                                                      #
                time = (datetime.datetime.now()-start).total_seconds()        #
                date = str(datetime.datetime.now())
                with open(logname,'a') as log:                                #
                    log.write(date+','+str(time)+',DropRetract\n')            #
                timetowait = random.sample(range(45,91),1)[0]
                
                waitfordeliver = datetime.datetime.now()                      #

        #                                                                     #
        #---------------------------------------------------------------------#        
        #*********************************************************************#
        
        if not killing: #killing keeps track of the button presses. if I am not killing the program:
            elapsed = str(datetime.datetime.now()-start) #count time
            elapsed = elapsed.split('.')[0]
            with canvas(device) as draw: #show on the screen elapsed time
                draw.text((0,0), name+'_habitS_'+test, font=fontT, fill="white")
                draw.text((23,24), str(elapsed), font=font, fill="white")
            if not GPIO.input(pin.ok): #check if I am pressing the rotary encoder
                killing=True #if so, it means I am killinkg
                waittoclose = getsecs() #start waiting and check if the user press again
                with canvas(device) as draw:
                    draw.text((0,0), name+'_habitS_'+test, font=fontT, fill="white")
                    draw.text((0,26), 'press again to quit', font=font, fill="white")
                    sleep(0.5)
        if killing: #if I have pressed once
            if getsecs()-waittoclose<15: #for 15 seconds
                if not GPIO.input(pin.ok): #if I press again, save
                    time = (datetime.datetime.now()-start).total_seconds()                                    
                    date = str(datetime.datetime.now())      
                    with open(logname,'a') as log:
                        log.write(date+','+str(time)+',TestOver\n')                 
                    cam.stop_recording()
                    cam.close()
                    with canvas(device) as draw:
                        draw.text((0,0), name+'_habitS_'+test, font=fontT, fill="white")
                        draw.text((0,26), 'cleanup...', font=font, fill="white")
                        draw.text((0,42), 'do not unplug', font=font, fill="white")
                    sleep(5)
                    break #terminate while loop
            else: #if 15 seconds elapse
                killing=False #exit from killing
    with canvas(device) as draw: #turn off
        draw.text((0,26), 'rebooting', font=font, fill="white")
        draw.text((0,42), 'do not unplug', font=font, fill="white")
    os.system("sudo reboot")
        
