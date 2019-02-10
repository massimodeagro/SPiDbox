""" complete program, launch this"""
# Import required libraries
import RPi.GPIO as GPIO
from threading import Thread
import datetime
import random
import os 

import epd2in9
import Image

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

    epd = epd2in9.EPD()
    epd.init(epd.lut_full_update)
    image = Image.open('screenImages/W.bmp') 
    epd.set_frame_memory(image, 0, 0)
    epd.display_frame()

    #%%#####################################################################%%#
    #------------------------------STARTING PROGRAM---------------------------#
    #                                                                         #
    killing = False                                                           #
    delivering = False                                                        #
    dropPresent = False                                                       #
    #drinking = False                                                          #
    #drank = False                                                             #
    waitfordeliver = datetime.datetime.now()
    cam = picamera.PiCamera()
    cam.resolution = (1296,972)
    cam.framerate = 5
    cam.start_recording('subjs/'+name+'/video/'+name+'_habitScreen_'+test+'.h264')
  
    #                                                                         #
    #-------------------------------------------------------------------------#
    ###########################################################################

    timetowait = random.sample(range(45,91),1)[0]
    #%%########################################################################
    #--------------------------------MAIN LOOP--------------------------------#
    while (True):
        #%%/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/%%#
        #-------------------------FOR DELIVERING DROP-------------------------#
        #   
        pos=0                                                                  #
        thismoment = datetime.datetime.now()                                  #
        waited = thismoment-waitfordeliver  
                                  #
        if waited.total_seconds() >= timetowait and (not dropPresent or not delivering):            
            delivering = True # delivering state                              #
            #logging                                                          #
            time = (datetime.datetime.now()-start).total_seconds()            #
            date = str(datetime.datetime.now())                               #
            deliverer=Thread(name='Perist',target=drop.stepmove,              #
                        args=(pin.stp,pin.clk,0,19,pos))                 #
            deliverer.start() # deliver a drop                                #
            pos = drop.postrack(19,pos)
                    
            waitfordeliver = datetime.datetime.now()                          #
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
                #drinking = False #setup drinking state                        #
                #drank = False #setup drank                                    #
                dropPresent = True                                            #
                #capmin,capmax,capmean = cap.readbase(cap.ELE0, #read cap.     #
                                                     #cap.bus,                 #
                                                     #cap.MPR121,              #
                                                     #30,10)                   #
                #logging.info('cap registered - min: '+str(capmin)+' max: '+str(capmax)+' mean: '+str(capmean))
                waitforRetract = getsecs() #start waiting for retraction      #
        #                                                                     #
        #---------------------------------------------------------------------#
        #=====================================================================#
                
        
        #%%*****************************************************************%%#
        #------------------------if the drop is present-----------------------#
        #                                                                     #
        if dropPresent:                                                       #
            #if not drinking: #not drinking                                    #
                
                #capREAD = cap.readvalue(cap.ELE0,cap.bus,cap.MPR121,10)       #
                #if capmin-capREAD > 2: #if he start drinking                  #
                    #capREAD = cap.readvalue(cap.ELE0,cap.bus,cap.MPR121,10)   #
                    #if capmin-capREAD > 2: #are you sure?                     #
                        #logging.info('touched drop: '+str(capREAD))
                        #drinking = True                                       #
                        #drank = True                                          #
                        ##logging                                              #
                        #time = (datetime.datetime.now()-start).total_seconds()#
                        #date = str(datetime.datetime.now())
                        #with open(logname,'a') as log:                        #
                            #log.write(date+','+str(time)+',DrinkStart\n')     #
                        #waitforRetract = getsecs() #restart waiting           #
            #if drinking:  #if is not drinking, ceck if it stops               #
                #capREAD = cap.readvalue(cap.ELE0,cap.bus,cap.MPR121,10)       #
                #if capmin-capREAD < 2:                                        #
                    #drinking = False                                          #
                    ##logging                                                  #
                    #time = (datetime.datetime.now()-start).total_seconds()    #
                    #date = str(datetime.datetime.now())
                    #with open(logname,'a') as log:                            #
                        #log.write(date+','+str(time)+',DrinkStop\n')          #
                
            now = getsecs() #now time                                         #
            nodrank = now-waitforRetract >= 35# and not drank                  #
            #dodrank = now-waitforRetract >= 3 and drank                       #
            if nodrank: #or dodrank: #if time is over
                #logging.info('retracting drop')                           #
                retracter=Thread(name='suck',target=drop.dcmove,              #
                                 args=(pin.dc,3))                           #
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
        if not killing:
            elapsed = str(datetime.datetime.now()-start)
            elapsed = elapsed.split('.')[0]
            with canvas(device) as draw:
                draw.text((0,0), name+'_habitS_'+test, font=fontT, fill="white")
                draw.text((23,24), str(elapsed), font=font, fill="white")
            if not GPIO.input(pin.ok):
                killing=True
                waittoclose = getsecs()
                with canvas(device) as draw:
                    draw.text((0,0), name+'_habitS_'+test, font=fontT, fill="white")
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
                        draw.text((0,0), name+'_habitS_'+test, font=fontT, fill="white")
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
        
