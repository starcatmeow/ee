#!/usr/bin/env python3

# %% Importing python packages
import numpy as np
import cv2

# %% Importing Image
img = cv2.imread('./Photos/cube.bmp')
np.save("./arrays/img", img)

# %% **YCbCr**
# Convert to YCbCr
yuv_img = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
Y, Cr, Cb = cv2.split(yuv_img)
np.savez("./arrays/yuv_img", Y=Y, Cb=Cb, Cr=Cr)

# %% Defining Compression Functions


def comp422(inp):
    """4:2:2 chroma subsampling"""
    Y, Cr, Cb = cv2.split(inp)
    x, y = Y.shape
    comp_Cb = np.empty([x, y//2], dtype=np.uint8)
    comp_Cr = np.empty([x, y//2], dtype=np.uint8)

    for i in range(comp_Cb.shape[0]):
        for j in range(comp_Cb.shape[1]):
            comp_Cb[i][j] = Cb[i][j*2]

    for i in range(comp_Cr.shape[0]):
        for j in range(comp_Cr.shape[1]):
            comp_Cr[i][j] = Cr[i][j*2]

    return Y, comp_Cb, comp_Cr


def comp411(inp):
    """4:1:1 chroma subsampling"""
    Y, Cr, Cb = cv2.split(inp)
    x, y = Y.shape
    comp_Cb = np.empty([x, y//4], dtype=np.uint8)
    comp_Cr = np.empty([x, y//4], dtype=np.uint8)

    for i in range(comp_Cb.shape[0]):
        for j in range(comp_Cb.shape[1]):
            comp_Cb[i][j] = Cb[i][j*4]

    for i in range(comp_Cr.shape[0]):
        for j in range(comp_Cr.shape[1]):
            comp_Cr[i][j] = Cr[i][j*4]

    return Y, comp_Cb, comp_Cr


def comp420(inp):
    """4:2:0 chroma subsampling"""
    Y, Cr, Cb = cv2.split(inp)
    x, y = Y.shape
    comp_Cb = np.empty([x//2, y//2], dtype=np.uint8)
    comp_Cr = np.empty([x//2, y//2], dtype=np.uint8)

    for i in range(comp_Cb.shape[0]):
        for j in range(comp_Cb.shape[1]):
            comp_Cb[i][j] = Cb[i*2][j*2]

    for i in range(comp_Cr.shape[0]):
        for j in range(comp_Cr.shape[1]):
            comp_Cr[i][j] = Cr[i*2][j*2]

    return Y, comp_Cb, comp_Cr


# **Compressing**

Y, Cb, Cr = comp420(yuv_img)
np.savez("./arrays/comp", Y=Y, Cb=Cb, Cr=Cr)
