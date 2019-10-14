"""
SPiDbox standalone version

module of the photoresistor reading

V0.1 of photoresistor voltage reading after the comparator working
This is called by main program and single tests. for a complete explanation of the system see the paper

@author: Massimo De Agrò
"""

#%%general variables

filt_c = 0.8   #filtering constant. how smoothed the raw data get
tresh_c = 0.11 #treshold constant. how much lower of the median average is the treshold, expressed in proportion
Eavg_c = 0.03  #averaging constant

def binphoto (adc, channel, filt_c,tresh_c,adc_filt,adc_Eavg): #calculate if the sensor has been covered, comparing treshold, raw reading, moving average

    adc_raw = adc.read_adc(channel, gain=1)
    
    adc_filt = (filt_c * adc_raw) + (( 1 - filt_c ) * adc_filt)
    
    if adc_filt<adc_Eavg-adc_Eavg*tresh_c: 
        covered = 1
    else:
        covered = 0
  
    return covered, adc_filt

def Eavgcalc(adc_filt, adc_Eavg, Eavg_c): #moving average formula
    adc_Eavg = (Eavg_c * adc_filt) + (( 1 - Eavg_c ) * adc_Eavg)
    return adc_Eavg
