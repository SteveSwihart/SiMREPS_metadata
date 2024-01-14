# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 14:39 2021

@author: Steve
"""

"""
Program to compress all tiff files in a folder
    ... has simple UI to choose folder. Once chosen, it will:
      Get path
      Identify files    
      Open files
      Compress
      Write preserving tags, in subfoler 'Compressed'
      Capture time statistics
    
    Later...
       ID files in folder (individual)
       Create version with packbits as option, all frames
"""


"""
# Simple code to show an image

with Image.open("D:\\test\\Compression\\Capture_00001.tif") as im:
    im.show()
"""

# To check that libtiff is loaded:
#    from PIL import features
#    print(features.check('libtiff'))

# See CompressionTest.py, TiffTaggRead.py and ImageDiff.py for more info on compression 
#   techniques, reading tiff tags, and verifying compression is lossless.

# import PIL
# from PIL import Image
import PySimpleGUI as sg
import os
from tifffile import imread, imsave
from datetime import datetime

#compressionValue=1 #which is the default, can be changed in UI using slider.

def compressTiff(Directory,tifList,compressionValue):
    print('in compressTiff\n')
    timeStart=datetime.now()
    print('time start = ',timeStart)
    tifQuantity=len(tifList)
    print('number of Tifs = ',tifQuantity)
    for tifFile in tifList:
        fileToCompress=Directory+r'\\'+tifFile
        print('file to compress: '+fileToCompress)
        img = imread(fileToCompress)
        #print('read the image')
        compressedImagePath=path+r'\\'+tifFile
        imsave(compressedImagePath,img,compress=compressionValue)
        print('compression value ',compressionValue)
        # print('compressed it')
      # compress = x is the slider for deflate compression time (all values give lossless compression)
      # 0 doesn't do anything, 9 takes all possible compute time.
      # definition of deflate (see Encoder/compressor for details on speed v size: 
          #https://en.wikipedia.org/wiki/Deflate
      # 6 gives the ~same result as matlab deflate:
          # original file 3753
          # matlab deflate 1690
          # tifffile 1 1787, 600 images in 1m00.4 sec, or .10 sec/image, 50.0% compression
          # tifffile 2 1765, 600 images in 1m6.47 sec, or 0.11 sec/image, 50.6% compression
          # tifffile 3 1746, 600 images in 1m 59 sec (119.42 sec), or 0.199 sec/image, 51.1% compression
          # tifffile 4 1754, 600 images in 1m 46 sec, or .176 sec/image, 50.9% compression
          # tifffile 5 1717, 600 images in 3m 24 sec (204.6 sec) or .341 sec/image, 51.9% compression
          # tifffile 6 1680, 600 images in 8m 55 sec (534.87 sec), or .891 sec/image, 52.9% compression
          # tifffile 7 1673, 600 images in 14m 12 sec (852.53 sec), or 1.421 sec/image, 53.2% compression
          # tifffile 8 1670, 600 images in 17m 50 sec (1069.69 sec), or 1.783 sec/image, 53.3% compression 
          # tifffile 9 1669, 600 images in 17m45.6 sec (1065.56 sec), or 1.776 sec/image, 53.3% compression 
          #
          # statistics are from runs with 'CompressFolder.py' on sample dataset:
          #     Hercules/users/Marketing/rawData/20210317/Capture/concentration1/c1.tif
          
    timeStop=datetime.now()    
    print('time start = ',timeStart)
    print('time stop = ',timeStop)
    elapsedTime=timeStop-timeStart
    print('elapsed time = ',elapsedTime)
    elapsedSeconds=elapsedTime.total_seconds()
    print('elapsed time in seconds = ',elapsedSeconds)
    secondsPerImage=elapsedSeconds/tifQuantity
    print('seconds per image = ',secondsPerImage)
      
"""
UI section
"""
theTip="This program finds tifs in the folder you specify,and compresses them with Adobe deflate,\na lossless compression scheme.\n\nYou control the amount of compression v compute time with an integer from 0 to 9.\n0 does nothing, 1 is the fastest, 9 is the slowest.\n\nExample:\na Tif file of 3.573MB compresses to:\n1.787 MB in 0.1 sec\n1.676 MB in 1.876 sec\n\nNote that it will overwrite any tifs in the Compressed subfolder."

sg.theme('DarkTeal4') # Image with all themses: https://user-images.githubusercontent.com/46163555/71361827-2a01b880-2562-11ea-9af8-2c264c02c3e8.jpg

layout = [
            [sg.Frame(layout=[[sg.InputText('Set The Directory to compress all tiffs in',
                key='-FILE_LOCATION-',enable_events=True,tooltip=theTip),
                sg.FolderBrowse(target='-FILE_LOCATION-',enable_events=True)]],title='Directory (Browse runs)',title_color='orange')],
            [sg.T('Degree of Compression \n(0=None, 9 max, recommend 1)',text_color='#ccaaea'),
             sg.Slider(range=(0,9),default_value=1,orientation='h',key='-COMPRESSION_AMOUNT-',text_color="orange",trough_color='#556088')],
         ]


window = sg.Window('Tiff Compress for Folder',layout) 


#Start listening to the window
while True:             
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Cancel'):
        break
    if event =='-FILE_LOCATION-':      
        compressionValue = int(values['-COMPRESSION_AMOUNT-'])
        FL = values['-FILE_LOCATION-']
        Directory=FL.replace('/','\\')
        print('Directory chosen:',Directory)
        path=os.path.join(Directory,'Compressed')
        try:
            os.mkdir(path)
            print('\n...created Compressed subfolder')
        except OSError as error:
            print(error)
        tifList=[]
        
        try: # it's in a try in case user cancels browse, in which case you'd crash and get a FileNotFoundError.
            for file in os.listdir(Directory):
                if file.endswith(".tif"):
                    tifList.append(file)
            # Use the following to find all tiffs in subfolders too. This will find anything you've already compressed and 
            # for root, dirs, files in os.walk(Directory):
            #     for file in files:
            #         if file.endswith(".tif"):
            #             tifList.append(file)
            print('\nList of Tiffs found:\n',tifList)
            if values['-COMPRESSION_AMOUNT-'] != "":
                 compressTiff(Directory,tifList,compressionValue)
            print('done compressing')
            print('compression value used = ',compressionValue)
        except:
            sg.Popup('Select a folder or I shall refuse to do anything')



window.close()



