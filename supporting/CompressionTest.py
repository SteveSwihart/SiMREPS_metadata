# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 13:20:48 2021

@author: Steve
"""

"""
Program to compress a tiff file (unstacked) using Adobe deflate:
    Open file
    Compress
    Write preserving tags, appending PB to filename
    
    ... alter "compress=" value from 1-9 (0 does not compress). Trades compute time for file size.
    
    Later...
       ID files in folder (individual)
       Create version with packbits, all frames
       Write preserving tags, appending PB to filename
"""


"""
# Simple code to show an image

with Image.open("D:\\test\\Compression\\Capture_00001.tif") as im:
    im.show()
"""

# To check that libtiff is loaded:
#    from PIL import features
#    print(features.check('libtiff'))

# Replace this path with your path to image
ImageLoc='D:\test\Compression\FullSetConcentration1\Capture_00343.tif'

# See this url for the tiff tags spec: https://www.loc.gov/preservation/digital/formats/content/tiff_tags.shtml
# See this url for TiffTags module docs: https://pillow.readthedocs.io/en/stable/reference/TiffTags.html
# and this for compression tag types: https://www.awaresystems.be/imaging/tiff/tifftags/compression.html
#   of interest to us based on Mike's testing are packbits (32773) and Adobe deflate (8)

# ListOfTags (list) = PIL.TiffTags.LIBTIFF_CORE # List of Supported Tags
# Tags for an image (dict) = PIL.TiffTags.TAGS_V2
# Human-readable tag data type names (dict) = PIL.TiffTags.TYPES

import PIL
from PIL import Image

# Get the tags used in the image

# A list of all tags supported by PIL
ReadableTags=PIL.TiffTags.TAGS_V2 # a list of all supported tags
# print('\nhuman readable tags:\n',ReadableTags) #uncomment to see all possible incl. type

im=Image.open(ImageLoc)
TagsInImage=im.tag_v2
# print('Tags in image:\n', TagsInImage)


#For each tag in image, get tag name
print('\nkey number, description, value\n')

for key in TagsInImage:
    ReadableTagMultiFull=ReadableTags[key] # gives full set of multi-param tags that are present in image
    # print('TagMultiFull',ReadableTagMultiFull)
    
    ReadableTagSingleFull=str(ReadableTagMultiFull[1:2]) # gets just the 'name' tag, but with extra punctuation
    # print('TagSingleFull',ReadableTagSingleFull)
    
    ReadableTagSans=ReadableTagSingleFull[2:-3] # remove starting/ending parenthesis, single quotes and comma using positioning
    #print(ReadableTagSans)
    
    print(key,ReadableTagSans,TagsInImage[key],'\n')

# import numpy as np
# pxArray=np.asarray(im)
# img=Image.fromarray(pxArray)

#im.show()
im.close()

"""
 The various compression options are 
   PIL/Pillow, which I couldn't make work, 
   PythonMagick, which doesn't support deflate or packbits
   Scikit-image using FreeImage library, 
   and tifffile, which only uses deflate, and which appears to work.
""" 

# from PythonMagick import Image, CompressionType
# im = Image('tiger-rgb-strip-contig-16.tif')
# im.compressType(CompressionType.ZipCompression)
# im.write("tiger-rgb-strip-contig-16-zip.tif")
# compressiontypes in PythonMagick: https://imagemagick.org/script/command-line-options.php#compress
#   None, BZip, Fax, Group4, JPEG, JPEG2000, Lossless, LZW, RLE or Zip


"""
  tifffile method
"""

from tifffile import imread, imsave
img = imread('D:/test/Compression/Capture_00001.tif')
imsave("", img, compress=1)
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
      # statistics are from runs with 'CompressFolder.py' on sample dataset:
          # Hercules/users/Marketing/rawData/20210317/Capture/concentration1/c1.tif
      

"""
  skimage and freeimage method
  I didn't get it to work thus far
"""
# im.save('D:/test/Compression/blah.tif',"tiff",optimize=True,compression="packbits")
#import skimage.io._plugins.freeimage_plugin as fi
# import skimage
# #from skimage import data_dir
# img = skimage.read(ImageLoc)
# io.write('D:/test/Compression/Capture_skimage_deflate.tif',
#          io.IO_FLAGS.TIFF_ADOBE_DEFLATE)

"""
  Pillow, used to get all Tif tags and display with english language description
"""

# with Image.open(ImageLoc) as im:
#     img=im.load()
#     TagsInImage=im.tag_v2
#     # For each tag in image, get tag name
#     print('\nkey number, description, value\n')
    
    
#     for key in TagsInImage:
#         ReadableTagMultiFull=ReadableTags[key] # gives full set of multi-param tags that are present in image
#         # print('TagMultiFull',ReadableTagMultiFull)
        
#         ReadableTagSingleFull=str(ReadableTagMultiFull[1:2]) # gets just the 'name' tag, but with extra punctuation
#         # print('TagSingleFull',ReadableTagSingleFull)
        
#         ReadableTagSans=ReadableTagSingleFull[2:-3] # remove starting/ending parenthesis, single quotes and comma using positioning
#         #print(ReadableTagSans)
        
#         print(key,ReadableTagSans,TagsInImage[key],'\n')

"""
   Pillow, which I can't make work (no file size change)
"""
#     img.save('D:/test/Compression/c3compressed.tif',compression="deflate")    

 



