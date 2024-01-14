# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 08:54:14 2021

@author: Steve
"""

"""
  Version History
    2-Nov-21: initial ver. Would be nice to instead get a list.
"""

import sys
import subprocess

def checkModuleInstalled(moduleName):    
    print('name to check =',moduleName, type(moduleName))
    
    try:
        __import__(moduleName)
        print("module",moduleName, 'is installed')
        installed=True
        # print('True',installed) # I exist to give a msg from the true portion
        
    except ModuleNotFoundError:
        print("module",moduleName," is not installed")
        installed=False
        # print('false',installed) # I exist to give a msg from the false portion
    
    # print('installed after chk',installed) # I exist to print after the try/except is complete.
    
    if installed==False:   
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', moduleName], stdout=subprocess.DEVNULL)
    return installed

if __name__ == '__main__':
    checkModuleInstalled(moduleName)
    
"""
Need this code when file in subdir 'supporting' (tweak moduleName as needed):
    import sys
    sys.path.insert(0, './supporting') # Need this to allow function to be in a subdir
    import checkModule
    
    moduleName='simplejson'
    
    inst=checkModule.checkModuleInstalled(moduleName)
    print('module ',moduleName,'is installed?',inst)
"""
