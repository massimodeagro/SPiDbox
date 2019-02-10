""" complete program, launch this"""

import datetime

# Import required libraries
import RPi.GPIO as GPIO
from threading import Thread
import picamera
import os

import epd2in9
import Image

# Import custom modules
import drop
#import vibr
#import MPR121 as cap
import pin

import Adafruit_ADS1x15 #read photo
import photo

adc = Adafruit_ADS1x15.ADS1115(address=0x48) #photoresistor I2C

def trainNS(name,test,cside,start,canvas, device,font, fontT):
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

    pos = 0                                                                   #
    delivering = False                                                        #
    dropPresent = False                                                       #
    stepsnum = 19
    #drinking = False                                                         #
    #drank = False                                                            #
    #                                                                         #
    #-------------------------------------------------------------------------#
    ###########################################################################
    ###################################################################
    #-|-|-|-|-|-|-|-|-PRIME SCREEN AND BUTTONS|-|-|-|-|-|-|-|-|-|-|-|-#
    #                                                                 #
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
    
    #Prime Photoresistors
    adc_filtC = adc.read_adc(photoCORRECT, gain=1)
    adc_EavgC = adc_filtC*1.0
    adc_filtW = adc.read_adc(photoWRONG, gain=1)
    adc_EavgW = adc_filtW*1.0
    #                                                                 #
    #-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-#
    #%%########################################################################
    #--------------------------------MAIN LOOP--------------------------------#
    while (True):
        now = getsecs()
        #%%/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/%%#
        #-------------------------FOR CORRECT RESISTOR------------------------#
        #     
        C, adc_filtC = photo.binphoto (adc, photoCORRECT, photo.filt_c,photo.tresh_c,adc_filtC,adc_EavgC)

        if not Cpressed:
            if C == 1:
                print ("Cpressed")
                Cpressed = True
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
                                    args=(pin.stp,pin.clk,0,stepsnum,pos))                    #     #
                        deliverer.start() # deliver a drop              #     #
                        pos = drop.postrack(stepsnum,pos)                     #     #
                    #                       end                         #     #                    
                    #   #   #   #   #   #   #   #   #   #   #   #   #   #     #                    
            else:
                adc_EavgC = photo.Eavgcalc(adc_filtC, adc_EavgC,photo.Eavg_c)

        if Cpressed: #if is being pressed                                     #
           if C == 0:
                print ("Crelease")
                Cpressed=False
                #logging                                                  #
                time = (datetime.datetime.now()-start).total_seconds()    #
                date = str(datetime.datetime.now())                       #
                with open(logname,'a') as log:
                    log.write(date+','+str(time)+',Crelease\n')           #
                waitforRetract = getsecs() #start waiting for retraction  #
                
                adc_EavgC = photo.Eavgcalc(adc_filtC, adc_EavgC,photo.Eavg_c)
                        
        #                                                                     #
        #---------------------------------------------------------------------#
        #/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/#
        
        
        #%%/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/%%#
        #--------------------------FOR WRONG RESISTOR-------------------------#
        # 
        W, adc_filtW = photo.binphoto (adc, pin.photoW, photo.filt_c,photo.tresh_c,adc_filtW,adc_EavgW)                                                                    #
        if not Wpressed:
            if W == 1:
                Wpressed=True
                print ("Wpressed")
                time = (datetime.datetime.now()-start).total_seconds()    #
                date = str(datetime.datetime.now())                       #
                with open(logname,'a') as log:
                    log.write(date+','+str(time)+',Wpressed\n')           #
                w+=1
                #   #   #   #   #   #   #   #   #   #   #   #   #   #     #
                #           wrong button has become pressed         #     #
                #                                                   #     #
                if dropPresent:
                    retracter=Thread(name='suck',target=drop.dcmove,args=(pin.dc,3))                             #
                    retracter.start()                                             #
                    dropPresent = False
                    #logging                                                      #
                    time = (datetime.datetime.now()-start).total_seconds()        #
                    date = str(datetime.datetime.now())                           #
                    with open(logname,'a') as log:
                        log.write(date+','+str(time)+',DropRetract\n')            #
                #                                                   #     #                    
                #                       end                         #     #
                #   #   #   #   #   #   #   #   #   #   #   #   #   #     #
            else:
                adc_EavgW = photo.Eavgcalc(adc_filtW, adc_EavgW,photo.Eavg_c)

        if Wpressed: #if is being pressed                                     #
            if W == 0:
                Wpressed=False  
                print ("Wrelease")                                        #
                #logging                                                  #
                time = (datetime.datetime.now()-start).total_seconds()    #
                date = str(datetime.datetime.now())                       #
                with open(logname,'a') as log:
                    log.write(date+','+str(time)+',Wrelease\n')           #
                
                adc_EavgC = photo.Eavgcalc(adc_filtC, adc_EavgC,photo.Eavg_c)
                    
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
                #logging                                                      #
                time = (datetime.datetime.now()-start).total_seconds()        #
                date = str(datetime.datetime.now())                           #
                with open(logname,'a') as log:
                    log.write(date+','+str(time)+',DropRetract\n')            #
        #                                                                     #
        #---------------------------------------------------------------------#        
        #*********************************************************************#
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