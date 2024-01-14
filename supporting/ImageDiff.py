# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 11:22

@author: Steve
"""

"""
Program to compare 2 Tiffs
"""


"""
# Simple code to show an image

with Image.open("D:\\test\\Compression\\Capture_00001.tif") as im:
    im.show()
"""

# To check that libtiff is loaded:
#    from PIL import features
#    print(features.check('libtiff'))

# Replace this path with your paths to images to compare
Image1Loc='D:/test/Compression/Capture_00001.tif'
Image2Loc='D:/test/Compression/Capture_00001_tifffile_adobeDeflate9.tif'


from PIL import Image
import numpy as np
# from PIL import ImageChops

img1=np.asarray(Image.open(Image1Loc))
img2=np.asarray(Image.open(Image2Loc))

diffArray=img1-img2
print('\ndifference array:\n',diffArray)
diff=np.sum(diffArray)
print('\ndifference betw all px in images:\n',diff)

"""
An attempt with Image Channel Ops of Pillow - it's just that ... an attempt.
"""
# img1=Image.open(Image1Loc)

# img2=Image.open(Image2Loc)

# Diff = ImageChops.difference(img1,img2)
# Diff.show()
# print(Diff)