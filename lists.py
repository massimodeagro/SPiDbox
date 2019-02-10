# -*- coding: utf-8 -*-
"""
SkinnerBox standalone version

subject list and other saved informations

@author: Massimo De Agrò
"""

from os import listdir

def loadsubjs():
    subjs = listdir('subjs/')
    subjs = ['back']+subjs
    return subjs
    
subjs = loadsubjs()