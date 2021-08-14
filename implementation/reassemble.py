#!/usr/bin/env python3

# %% import python packages
import numpy as np
from scipy import fftpack
import cv2

# %% Importing Data
data = np.load('./arrays/qblocks.npz')

qYblocks = data['qYblocks']
qCbblocks = data['qCbblocks']
qCrblocks = data['qCrblocks']

comp = np.load('./arrays/comp.npz')

Y_comp = comp['Y']
Cb_comp = comp['Cb']
Cr_comp = comp['Cr']

# %% Quantization

ql = np.genfromtxt("./quantization table/ps010l.csv", delimiter=",", dtype=int)
qc = np.genfromtxt("./quantization table/ps010c.csv", delimiter=",", dtype=int)

Yblocks = qYblocks * ql
Crblocks = qCrblocks * qc
Cbblocks = qCbblocks * qc

# %% DCT
Yy, Yx = Y_comp.shape
for i in range(Yx*Yy//64):
    dctBlocks = fftpack.idct(Yblocks[i], axis=1)

Cy, Cx = Cb_comp.shape
for i in range(Cx*Cy//64):
    CrBlocks = fftpack.dct(Crblocks[i], axis=1)
    CbBlocks = fftpack.dct(Cbblocks[i], axis=1)

# Normalize
Yblocks += 128
Crblocks += 128
Cbblocks += 128

# %% Merge blocks into picture

Y = np.zeros([Yx * 8, Yy * 8], dtype=int)
Cr = np.zeros([Cx * 8, Cy * 8], dtype=int)
Cb = np.zeros([Cx * 8, Cy * 8], dtype=int)

for i in range(Yy):
    for j in range(Yx):
        Y[i][j] = Yblocks[i//8*Yx//8 + j//8][(i) % 8][(j) % 8]

for i in range(Cy):
    for j in range(Cx):
        Cr[i][j] = Crblocks[i//8*Cx//8 + j//8][(i) % 8][(j) % 8]
        Cb[i][j] = Cbblocks[i//8*Cx//8 + j//8][(i) % 8][(j) % 8]

# %% Chroma Subsampling
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


# uncompressing
comp_img = uncomp420(Y, Cb, Cr)

# %% Outputting Image
output_comp = cv2.cvtColor(comp_img, cv2.COLOR_YCR_CB2BGR)
cv2.imwrite('./experiment/compressed.png', output_comp)

# This is currentally fucked btw
