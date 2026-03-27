import cv2
import tifffile as tif
import numpy as np
from skimage import morphology as mph
from matplotlib import pyplot as plt
import os
import sys

infolder = sys.argv[1]
outfolder = sys.argv[2]

os.makedirs(outfolder, exist_ok=True)

file_list = os.listdir(infolder)
file_names = [os.path.splitext(file) for file in file_list if file.endswith('.tif')]
def denoise(im):
    closed=mph.area_opening(im,80)
    opened=mph.area_opening(closed,80)
    return opened
for i in range(len(file_names)):
    img=tif.imread(os.path.join(infolder, file_names[i][0]+file_names[i][1]))
    open=denoise(img)
    tif.imwrite(outfolder+'/'+file_names[i][0]+'_dn.tif',open.astype('uint8'))
# Load images
#images = [cv2.imread(f'image_{i}.jpg') for i in range(10)]

# Normalize images
#normalized_images = normalize_images(images)
