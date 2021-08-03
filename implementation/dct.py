#!/usr/bin/env python3

# %% Importing python packages
import numpy as np
from scipy import fftpack

# %% Importing Image

# Import from new image
img = np.load('./arrays/img.npy')

uncompressed = np.load('./arrays/yuv_img.npz')  # Load uncompressed
data = np.load('./arrays/comp.npz')

# Y = uncompressed['Y']
# Cb = uncompressed['Cb']
# Cr = uncompressed['Cr']
Y = data['Y']
Cb = data['Cb']
Cr = data['Cr']

# %% split into 8x8 blocks
Yy, Yx = Y.shape
Yblocks = np.zeros([Yx * Yy // 64, 8, 8], dtype=int)

for i in range(Yy):
    for j in range(Yx):
        Yblocks[i//8*Yx//8 + j//8][(i) % 8][(j) % 8] = Y[i][j]

Cy, Cx = Cr.shape
Crblocks = np.zeros([Cx * Cy // 64, 8, 8], dtype=int)
Cbblocks = np.zeros([Cx * Cy // 64, 8, 8], dtype=int)

for i in range(Cy):
    for j in range(Cx):
        Crblocks[i//8*Cx//8 + j//8][(i) % 8][(j) % 8] = Cr[i][j]
        Cbblocks[i//8*Cx//8 + j//8][(i) % 8][(j) % 8] = Cb[i][j]

# normalize to zero (-128)
Yblocks -= 128
Crblocks -= 128
Cbblocks -= 128

# %% DCT
for i in range(Yx*Yy//64):
    dctBlocks = fftpack.dct(Yblocks[i], axis=1)

for i in range(Cx*Cy//64):
    CrBlocks = fftpack.dct(Crblocks[i], axis=1)
    CbBlocks = fftpack.dct(Cbblocks[i], axis=1)

# %% **Quantization**

# Importing Quantization Tables
ql = np.genfromtxt("./quantization table/ps010l.csv", delimiter=",", dtype=int)
qc = np.genfromtxt("./quantization table/ps010c.csv", delimiter=",", dtype=int)

# Quantization

qYblocks = np.rint(Yblocks/ql)
qCrblocks = np.rint(Crblocks/qc)
qCbblocks = np.rint(Cbblocks/qc)

np.savez("./arrays/qblocks", qYblocks=qYblocks, qCbblocks=qCbblocks, qCrblocks=qCrblocks)
