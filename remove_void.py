import sys
import numpy as np
import tifffile as tif
import cv2 as cv
from matplotlib import pyplot as plt
from skimage.filters import threshold_multiotsu
from skimage.morphology import (area_opening,area_closing,erosion,dilation,remove_small_objects,remove_small_holes)
import porespy as ps
#import skimage
from skimage import measure,io,img_as_ubyte
from skimage import segmentation,morphology
from skimage.color import label2rgb
import tifffile as tif
from matplotlib import pyplot as plt
import numpy as np
import cv2
import pandas as pd
import datetime
import cv2
import tifffile as tif
import numpy as np
from skimage import morphology as mph
from matplotlib import pyplot as plt
import math
import os

def props_to_image(regionprops, shape, prop):
    im = np.zeros(shape=shape)
    for r in regionprops:
        if prop == 'convex':
            mask = r.convex_image
        else:
            mask = r.image
        temp = mask * r[prop]
        s = ps.tools.bbox_to_slices(r.bbox)
        im[s] += temp
    return im

def remove_void(crack):
    label_img=measure.label(crack)
    props = measure.regionprops(label_img)
    im_area=props_to_image(props, label_img.shape, 'area')
    im_d=props_to_image(props,label_img.shape,'perimeter')
    im_cir=np.where(im_area!=0,(im_d**2)/(4*math.pi*(im_area)),0)
    crk=np.where(((im_area>4000)&(im_cir<4)&(im_cir>0)),255,0)
    crk=np.where((im_area>20000),255,crk)
    return crk

infolder = sys.argv[1]
outfolder = sys.argv[2]
file_list = os.listdir(infolder)
file_names = [os.path.splitext(file) for file in file_list if file.endswith('.tif')]

for i in range(len(file_names)):
    img=tif.imread(os.path.join(infolder, file_names[i][0]+file_names[i][1]))
    img=np.where(img==1,255,0)
    open=remove_void(img)
    crk=np.where(open!=0,0,img)
    tif.imwrite(outfolder+'/Void/'+file_names[i][0]+'_v.tif',open.astype('uint8'))
    tif.imwrite(outfolder+'/Crk/'+file_names[i][0]+'_ck.tif',crk.astype('uint8'))
