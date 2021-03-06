# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 08:52:48 2021

@author: mleong
"""

import _pickle as cPickle 
import gc


def load(file_name):
    file = open(file_name,'rb')
    
    # disable garbage collector
    gc.disable()
    
    output = cPickle.load(file)
    
    # enable garbage collector
    gc.enable()
    file.close()
    return output
    
def dump(dump_object, file_name):
    with open(file_name,'wb') as file:
        cPickle.dump(dump_object,file)
    