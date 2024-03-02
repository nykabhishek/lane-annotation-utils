import numpy as np
import cv2
import glob






# Recursively print png images in folder C:\Users\admin\
for filepath in glob.iglob(r'./30ft_gap/**/*.jpg', recursive=True):
    # print(filepath)
    im = cv2.imread(filepath)
    im_height = im.shape[0]
    im_width = im.shape[1]
    # print(im_height, im_width)
    cropL = im[0:int(im_height), 0:int(0.45*im_width)]
    cropR = im[0:int(im_height), int(0.45*im_width):int(im_width)]
    filepathL = filepath.replace('/30ft_gap', '/left/30ft_gap')
    filepathR = filepath.replace('/30ft_gap', '/right/30ft_gap')
    # print(filepathL, filepathR)
    cv2.imwrite(filepathL, cropL)
    cv2.imwrite(filepathR, cropR)
    # cv2.waitKey(2) 

