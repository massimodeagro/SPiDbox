""" complete program, launch this"""

import datetime

# Import required libraries
import RPi.GPIO as GPIO
from threading import Thread
import picamera
import os
from random import choice

import epd2in9
import Image

# Import custom modules
import drop
#import vibr
#import MPR121 as cap
import pin

def trainS(name,test,cshape,start,canvas, device,font, fontT):
    print ("in the function")
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
    c=0
    w=0                                                                         #
    killing = False
    Cpressed = False
    Wpressed = False
    CpressedWhilePresenting = False
    WpressedWhilePresenting = False

    pos = 0                                                                   #
    delivering = False                                                        #
    dropPresent = False                                                       #
    #drinking = False                                                          #
    #drank = False                                                             #
    waitfornewpic = getsecs()
    presenting = False
    howmuchtowait = 5
    #                                                                         #
    #-------------------------------------------------------------------------#
    ###########################################################################
    ###################################################################
    #-|-|-|-|-|-|-|-|-PRIME SCREEN AND BUTTONS|-|-|-|-|-|-|-|-|-|-|-|-#
    #                                                                 #
    XO = Image.open('screenImages/XO.bmp')
    OX = Image.open('screenImages/OX.bmp')
    W = Image.open('screenImages/W.bmp')
    B = Image.open('screenImages/B.bmp')
    photoCORRECT = choice([pin.photoL,pin.photoR])
    if photoCORRECT == pin.photoL:
        with open(logname,'a') as log:
            log.write(date+','+str(time)+',CLeft\n')           #
        photoWRONG = pin.photoR
        if cshape == "X":
            cpic = XO
        else:
            cpic = OX
    else:
        with open(logname,'a') as log:
            log.write(date+','+str(time)+',CRight\n')           #
        photoWRONG = pin.photoL
        if cshape == "X":
            cpic = OX
        else:
            cpic = XO
    
    epd.set_frame_memory(B, 0, 0)
    epd.display_frame()
    epd.set_frame_memory(B, 0, 0)
    epd.display_frame()        
    epd.set_frame_memory(cpic, 0, 0)
    epd.display_frame()
    epd.set_frame_memory(cpic, 0, 0)
    epd.display_frame()
    presenting = True

    #                                                                 #
    #-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-#
    #%%########################################################################
    #--------------------------------MAIN LOOP--------------------------------#
    while (True):
        now = getsecs()
        if now-waitfornewpic>howmuchtowait and not Cpressed and not Wpressed and not presenting and not dropPresent and not delivering:
            print ("change stim")
            ###################################################################
            #-|-|-|-|-|-|-|-|-PRIME SCREEN AND BUTTONS|-|-|-|-|-|-|-|-|-|-|-|-#
            #                                                                 #
            photoCORRECT = choice([pin.photoL,pin.photoR])
            if photoCORRECT == pin.photoL:
                with open(logname,'a') as log:
                    log.write(date+','+str(time)+',CLeft\n')           #
                photoWRONG = pin.photoR
                if cshape == "X":
                    cpic = XO
                else:
                    cpic = OX
            else:
                with open(logname,'a') as log:
                    log.write(date+','+str(time)+',CRight\n')           #
                photoWRONG = pin.photoL
                if cshape == "X":
                    cpic = OX
                else:
                    cpic = XO
                    
            epd.set_frame_memory(cpic, 0, 0)
            epd.display_frame()
            epd.set_frame_memory(cpic, 0, 0)
            epd.display_frame()
            presenting = True
            with open(logname,'a') as log:
                log.write(date+','+str(time)+','+cshape+'\n')           #
            #                                                                 #
            #-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-#
                                                                         
        #%%/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/%%#
        #-------------------------FOR CORRECT RESISTOR------------------------#
        #                                                                     #
        if not Cpressed:
            if GPIO.input(photoCORRECT):
                print ("Cpressed")
                Cpressed = True
                howmuchtowait = 5
                if presenting:
                    CpressedWhilePresenting = True
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
                                                                            #     #
                            deliverer=Thread(name='Perist',target=drop.stepmove,   #
                                        args=(pin.stp,pin.clk,0,19,pos))                    #     #
                            deliverer.start() # deliver a drop              #     #
                            pos = drop.postrack(19,pos)                     #     #
                        #                       end                         #     #                    
                        #   #   #   #   #   #   #   #   #   #   #   #   #   #     #                    
                   
        if Cpressed: #if is being pressed                                     #
           if not GPIO.input(photoCORRECT):
                print ("Crelease")
                Cpressed=False
                if CpressedWhilePresenting:
                    CpressedWhilePresenting=False                             #
                    #logging                                                  #
                    time = (datetime.datetime.now()-start).total_seconds()    #
                    date = str(datetime.datetime.now())                       #
                    with open(logname,'a') as log:
                        log.write(date+','+str(time)+',Crelease\n')           #
                    waitforRetract = getsecs() #start waiting for retraction  #                        
        #                                                                     #
        #---------------------------------------------------------------------#
        #/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/#
        
        
        #%%/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/%%#
        #--------------------------FOR WRONG RESISTOR-------------------------#
        #                                                                     #
        if not Wpressed:
            Wpressed=True
            print ("Wpressed")
            howmuchtowait = 60
            if presenting:
                WpressedWhilePresenting=True
                #logging                                                  #
                time = (datetime.datetime.now()-start).total_seconds()    #
                date = str(datetime.datetime.now())                       #
                with open(logname,'a') as log:
                    log.write(date+','+str(time)+',Wpressed\n')           #
                w+=1
                #   #   #   #   #   #   #   #   #   #   #   #   #   #     #
                #           wrong button has become pressed         #     #
                #                                                   #     #
                if presenting:
                    epd.set_frame_memory(W, 0, 0)
                    epd.display_frame()
                    epd.set_frame_memory(W, 0, 0)
                    epd.display_frame()
                    epd.set_frame_memory(B, 0, 0)
                    epd.display_frame()
                    epd.set_frame_memory(B, 0, 0)
                    epd.display_frame()
                    waitfornewpic = getsecs()
                    presenting = False
                if dropPresent:
                    retracter=Thread(name='suck',target=drop.dcmove,args=(pin.dc,3))                             #
                    retracter.start()                                             #
                    dropPresent = False
                #logging                                                      #
                time = (datetime.datetime.now()-start).total_seconds()        #
                date = str(datetime.datetime.now())                           #
                with open(logname,'a') as log:
                    log.write(date+','+str(time)+',DropRetract\n')            #
                waitfornewpic = getsecs()+5
                presenting = False
                #                                                   #     #                    
                #                       end                         #     #
                #   #   #   #   #   #   #   #   #   #   #   #   #   #     #
        if Wpressed: #if is being pressed                                     #
            if not GPIO.input(photoWRONG):
                Wpressed=False  
                print ("Wrelease")                                        #
                if WpressedWhilePresenting:
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
                #drinking = False #setup drinking state                        #
                #drank = False #setup drank                                    #
                dropPresent = True                                            #
                delivering = False                                            #
                #capmin,capmax,capmean = cap.readbase(cap.ELE0, #read cap.     #
                #                                     cap.bus,                 #
                #                                     cap.MPR121,              #
                #                                     30,10)                   #
                                   #
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
                        #drinking = True                                       #
                        #drank = True                                          #
                        #logging                                              #
                        #time = (datetime.datetime.now()-start).total_seconds()#
                        #date = str(datetime.datetime.now())                   #
                        #with open(logname,'a') as log:
                            #log.write(date+','+str(time)+',ContactStart\n')   #
                        #waitforRetract = getsecs() #restart waiting           #
            #elif drinking:  #if is not drinking, ceck if it stops               #
                #capREAD = cap.readvalue(cap.ELE0,cap.bus,cap.MPR121,10)       #
                #if capmin-capREAD < 2:                                        #
                    #drinking = False
                    #logging                                                  #
                    #time = (datetime.datetime.now()-start).total_seconds()    #
                    #date = str(datetime.datetime.now())                       #
                    #with open(logname,'a') as log:
                        #log.write(date+','+str(time)+',ContactStop\n')        #
                    
            now = getsecs() #now time                                         #
            nodrank = now-waitforRetract >= 30 #and not drank #
            #dodrank = now-waitforRetract >= 3 and drank      #
            if nodrank and not Cpressed: #if time is over          #
                retracter=Thread(name='suck',target=drop.dcmove,              #
                                 args=(pin.dc,3))                             #
                retracter.start()                                             #
                dropPresent = False
                epd.set_frame_memory(W, 0, 0)
                epd.display_frame()
                epd.set_frame_memory(W, 0, 0)
                epd.display_frame()                                           #
                #logging                                                      #
                time = (datetime.datetime.now()-start).total_seconds()        #
                date = str(datetime.datetime.now())                           #
                with open(logname,'a') as log:
                    log.write(date+','+str(time)+',DropRetract\n')            #
                waitfornewpic = getsecs()+5
                presenting = False
        #                                                                     #
        #---------------------------------------------------------------------#        
        #*********************************************************************#
        if not killing:
            elapsed = str(datetime.datetime.now()-start)
            elapsed = elapsed.split('.')[0]
            with canvas(device) as draw:
                draw.text((30,0), 'testing', font=fontT, fill="white")
                draw.text((23,48), str(elapsed), font=font, fill="white")
                draw.text((23,24), 'c: '+str(c)+'     w: '+str(w),font=font, fill="white")
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
