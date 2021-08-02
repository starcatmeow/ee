#!/usr/bin/env python3

# %% Importing python packages
import numpy as np
import cv2
from scipy import fftpack

# %% Importing Image
img = cv2.imread('./Photos/sofa.bmp')
yuv_img = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)

# %% **DCT**

Y, Cr, Cb = cv2.split(yuv_img)

# %% split into 8x8 blocks
y, x = Y.shape
blocks = np.zeros([x * y // 64, 8, 8])

for i in range(y):
    for j in range(x):
        blocks[i//8*x//8 + j//8][(i) % 8][(j) % 8] = Y[i][j]

# normalize to zero (-128)
blocks -= 128

# %% DCT
for i in range(x*y//64):
    dctBlocks = fftpack.dct(blocks[i], axis=1)

# %% **Quantization**

