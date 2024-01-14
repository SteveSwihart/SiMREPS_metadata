# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 13:20:48 2021

@author: Steve
"""

"""
Program to read all Tiff tags in an image and get a list of the tag, english description, and value
   Might be nice to module check/install for PSG and PIL
"""


"""
# Simple code to show an image

with Image.open("D:\\test\\DataSet\\Capture_00001.tif") as im:
    im.show()
"""

# Replace this path with your path to image
#ImageLoc='D:/test/DataSet/Capture/2/Capture_00001.tif'
ImageLoc='D:\\Capture_00001.tif'

# See this url for the tiff tags spec: https://www.loc.gov/preservation/digital/formats/content/tiff_tags.shtml
# See this url for TiffTags module docs: https://pillow.readthedocs.io/en/stable/reference/TiffTags.html
# and this for compression tag types: https://www.awaresystems.be/imaging/tiff/tifftags/compression.html
#   of interest to us based on Mike's testing are packbits (32773) and Adobe deflate (8)

# ListOfTags (list) = PIL.TiffTags.LIBTIFF_CORE # List of Supported Tags
# Tags for an image (dict) = PIL.TiffTags.TAGS_V2
# Human-readable tag data type names (dict) = PIL.TiffTags.TYPES

import PySimpleGUI as sg
import PIL
from PIL import Image
# import os

def tagRead(imgFile):
    img = Image.open(imgFile)
    
    print ('indef')
    # Get the tags used in the image
    # img = Image.open(ImageLoc) #used for standalone (no UI)
    TagsInImage=img.tag_v2
    # print('Tags in image:\n', TagsInImage)
    
    # A list of all tags supported by PIL
    ReadableTags=PIL.TiffTags.TAGS_V2 # a list of all supported tags
    # print('\nhuman readable tags:\n',ReadableTags) #uncomment to see all possible incl. type
    
    # For each tag in image, get tag name
    print('\nkey number, description, value\n')
    
    for key in TagsInImage:
        ReadableTagMultiFull=ReadableTags[key] # gives full set of multi-param tags that are present in image
        # print('TagMultiFull',ReadableTagMultiFull)
        
        ReadableTagSingleFull=str(ReadableTagMultiFull[1:2]) # gets just the 'name' tag, but with extra punctuation
        # print('TagSingleFull',ReadableTagSingleFull)
        
        ReadableTagSans=ReadableTagSingleFull[2:-3] # remove starting/ending parenthesis, single quotes and comma using positioning
        #print(ReadableTagSans)
        
        print(key,ReadableTagSans,TagsInImage[key],'\n')
        
    # Get the value of compression Tag, #259
    
    if 259 in TagsInImage: # this isn't possible with SharpCap, but ImageJ appears to not write that tag.
        compressionValue=(TagsInImage[259])
        #print('Compression of file is:',compressionValue)
        
        compressionType="Unknown"
        if compressionValue==1:
            compressionType="Uncompressed"
            
        if compressionValue==5:
            compressionType="LZW"
            
        if compressionValue==8:
            compressionType="Adobe Deflate"
        
        if compressionValue==32773:
            compressionType="Packbits"
        print('Compression of file is:',compressionValue,'. In English:',compressionType)
    else:
        print('Tag 259 (compression type) does not exist in image')
        
    img.close() # so user can rename, move, delete saved file.

"""
UI section
"""
theTip="This program reads tif tags in the file you specify\n\nSee CompressFolder.py for a util to compress or uncompress a folder of Tifs\n\nMake a folder with a single Tif to do 1 file."

sg.theme('Topanga') # Image with all themses: https://user-images.githubusercontent.com/46163555/71361827-2a01b880-2562-11ea-9af8-2c264c02c3e8.jpg

layout = [
            [sg.Frame(layout=[[sg.InputText('Choose file to get tags from',
                key='-FILE_LOCATION-',enable_events=True,tooltip=theTip),
                sg.FileBrowse(target='-FILE_LOCATION-',enable_events=True)]],title='File (Browse runs)',title_color='#ccaaea')],
            [sg.T('See console for tags',text_color='#ccaaea'),
             ],
         ]


window = sg.Window('Tiff Tag read',layout) 


#Start listening to the window
while True:             
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Cancel'):
        break
    if event =='-FILE_LOCATION-':      
        FL = values['-FILE_LOCATION-']
        imgFile=FL.replace('/','\\')
        print('File chosen:',imgFile)
                
        # try: # it's in a try in case user cancels browse, in which case you'd crash and get a FileNotFoundError.
        #     if img.endswith(".tif"):
        #             tifList.append(file)
        #     # Use the following to find all tiffs in subfolders too. This will find anything you've already compressed and 
        #     # for root, dirs, files in os.walk(Directory):
        #     #     for file in files:
        #     #         if file.endswith(".tif"):
        #     #             tifList.append(file)
        tagRead(imgFile)

        # except:
        #     sg.Popup('Select a file or I shall refuse to do anything')



window.close()
