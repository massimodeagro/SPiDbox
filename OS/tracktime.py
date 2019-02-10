# -*- coding: utf-8 -*-
"""
SkinnerBox standalone version

tracktime module

@author: Massimo De Agrò
"""
import datetime

now = datetime.datetime.now

def timediff(start):
    s = now()-start
    s=s.total_seconds()
    return s

def currdatetime():
    dt = str(now)
    return dt

