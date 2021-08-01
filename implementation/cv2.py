#!/usr/bin/eval python3

# %% Importing python packages
import numpy as np
import cv2

# Convenient Function


def merge(a, b, c):
    """merge three seperate arrays into one"""
    x, y = a.shape
    output = np.empty([x, y, 3], dtype=np.uint8)

    for i in range(x):
        for j in range(y):
            output[i][j][0] = a[i][j]
            output[i][j][1] = b[i][j]
            output[i][j][2] = c[i][j]

    return output


# %% Importing Image
img = cv2.imread('./Photos/cube.bmp')

# %% Split image into RGB

greenChannel = np.zeros(img.shape, dtype=np.uint8)
for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        greenChannel[i][j][1] = img[i][j][1]

redChannel = np.zeros(img.shape, dtype=np.uint8)
for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        redChannel[i][j][2] = img[i][j][2]

blueChannel = np.zeros(img.shape, dtype=np.uint8)
for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        blueChannel[i][j][0] = img[i][j][0]

cv2.imwrite('./experiment/red.png', redChannel)
cv2.imwrite('./experiment/green.png', greenChannel)
cv2.imwrite('./experiment/blue.png', blueChannel)

# %% Convert to YCbCr
yuv_img = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)

# %% Displaying YCbCr

# splitting YCbCr
YChannel = np.empty(yuv_img.shape, dtype=np.uint8)
for i in range(yuv_img.shape[0]):
    for j in range(yuv_img.shape[1]):
        YChannel[i][j][0] = yuv_img[i][j][0]
        YChannel[i][j][1] = 128
        YChannel[i][j][2] = 128

CbChannel = np.empty(yuv_img.shape, dtype=np.uint8)
for i in range(yuv_img.shape[0]):
    for j in range(yuv_img.shape[1]):
        CbChannel[i][j][0] = 128
        CbChannel[i][j][1] = 128
        CbChannel[i][j][2] = yuv_img[i][j][2]

CrChannel = np.empty(yuv_img.shape, dtype=np.uint8)
for i in range(yuv_img.shape[0]):
    for j in range(yuv_img.shape[1]):
        CrChannel[i][j][0] = 128
        CrChannel[i][j][1] = yuv_img[i][j][1]
        CrChannel[i][j][2] = 128

# Exporting Image
YChannelRGB = cv2.cvtColor(YChannel, cv2.COLOR_YCR_CB2BGR)
cv2.imwrite('./experiment/Y.png', YChannelRGB)

CbChannelRGB = cv2.cvtColor(CbChannel, cv2.COLOR_YCR_CB2BGR)
cv2.imwrite('./experiment/Cb.png', CbChannelRGB)

CrChannelRGB = cv2.cvtColor(CrChannel, cv2.COLOR_YCR_CB2BGR)
cv2.imwrite('./experiment/Cr.png', CrChannelRGB)

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


def uncomp422(Y, Cb, Cr):
    """uncompresses 4:2:2 chroma subsampling"""
    y, x = Y.shape
    output = np.empty([y, x, 3], dtype=np.uint8)

    for i in range(y):
        for j in range(x):
            output[i][j][0] = Y[i][j]
            output[i][j][1] = Cr[i][j//2]
            output[i][j][2] = Cb[i][j//2]

    return output


def uncomp411(Y, Cb, Cr):
    """uncompresses 4:1:1 chroma subsampling"""
    y, x = Y.shape
    output = np.empty([y, x, 3], dtype=np.uint8)

    for i in range(y):
        for j in range(x):
            output[i][j][0] = Y[i][j]
            output[i][j][1] = Cr[i][j//4]
            output[i][j][2] = Cb[i][j//4]

    return output


def uncomp420(Y, Cb, Cr):
    """uncompresses 4:2:0 chroma subsampling"""
    y, x = Y.shape
    output = np.empty([y, x, 3], dtype=np.uint8)

    for i in range(y):
        for j in range(x):
            output[i][j][0] = Y[i][j]
            output[i][j][1] = Cr[i//2][j//2]
            output[i][j][2] = Cb[i//2][j//2]

    return output


# %% Compressing

# 4:2:0
a, b, c = comp420(yuv_img)
output = uncomp420(a, b, c)
outputRGB = cv2.cvtColor(output, cv2.COLOR_YCR_CB2BGR)
cv2.imwrite('./experiment/420.png', outputRGB)

# 4:2:2
a, b, c = comp422(yuv_img)
output = uncomp422(a, b, c)
outputRGB = cv2.cvtColor(output, cv2.COLOR_YCR_CB2BGR)
cv2.imwrite('./experiment/422.png', outputRGB)

# 4:1:1
a, b, c = comp411(yuv_img)
output = uncomp411(a, b, c)
outputRGB = cv2.cvtColor(output, cv2.COLOR_YCR_CB2BGR)
cv2.imwrite('./experiment/411.png', outputRGB)
