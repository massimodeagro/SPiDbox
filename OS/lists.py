"""
SPiDbox standalone version

subject list and other saved informations

@author: Massimo De Agrò
"""

from os import listdir

def loadsubjs(): #simply, the formula reads the folders in /home/subjs/. This is also where videos and csvs are saved
    subjs = listdir('subjs/')
    subjs = ['back']+subjs #the word "back" is added to the subject list, in order for the main menu to be able to go back
    return subjs
    
subjs = loadsubjs() #also, create the list
