
"""
SPiDbox

@author: Massimo De Agro'
"""

#modules
from RPi import GPIO

#this formula read the state of both cl and dt, as well as starting from the old reading of those.
#a movement is detected based on the current state and the new state. If those two are different, it means that the rotor moved.
#Then, depending on the position, a clockwise (1) or counterclockwise (-1) rotation can be detected.
def rotation(cl,dt,outold): 
    a=GPIO.input(cl)
    b=GPIO.input(dt)
    out = str(a)+str(b)
    rotating = 0
    if out != outold:
        if outold == '11':
            if out == '10':
                rotating = 1
            if out == '01':
                rotating = -1
        if outold == '10':
            if out == '00':
                rotating = 1
            if out == '11':
                rotating = -1
        if outold == '00':
            if out == '01':
                rotating = 1
            if out == '10':
                rotating = -1
        if outold == '01':
            if out == '11':
                rotating = 1
            if out == '00':
                rotating = -1
        outold = out
    return rotating,outold

#this formula catches clicks
def button(sw):
    out = not GPIO.input(sw)
    return out
    
#hthis formula loops all together, continously catching cl and dt state, as well as checking if the button has been clicked
def rothread(cl,dt,sw):
    outold = '00'
    casechange = 0
    while -2<casechange<2:
        inc,outold = rotation(cl,dt,outold)
        butt = button(sw)
        casechange +=inc
        if butt == True:
            butt = button(sw)
            print ('click')
            if butt == True:
                casechange = 0
                break
    print ('rotated')
    return casechange/2

