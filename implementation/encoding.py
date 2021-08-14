#!/usr/bin/env python3

# %% Importing python packages
import numpy as np

# %% Importing Data
data = np.load('./arrays/qblocks.npz')

qYblocks = data['qYblocks']
qCbblocks = data['qCbblocks']
qCrblocks = data['qCrblocks']

# %% Entropy Encoder
# This just works, very messy but works


def entropyData(array):
    output = np.zeros(64)
    y = x = 0
    i = 0

    output[i] = array[y][x]
    i += 1

    x += 1
    output[i] = array[y][x]
    i += 1

    for j in range(3):
        while x != 0:
            x -= 1
            y += 1
            output[i] = array[y][x]
            i += 1

        y += 1
        output[i] = array[y][x]
        i += 1

        while y != 0:
            x += 1
            y -= 1
            output[i] = array[y][x]
            i += 1

        x += 1
        output[i] = array[y][x]
        i += 1

    while x != 0:
        x -= 1
        y += 1
        output[i] = array[y][x]
        i += 1

    # Midpoint
    x += 1
    output[i] = array[y][x]
    i += 1

    for j in range(3):
        while x < 7:
            x += 1
            y -= 1
            output[i] = array[y][x]
            i += 1

        y += 1
        output[i] = array[y][x]
        i += 1

        while y < 7:
            x -= 1
            y += 1
            output[i] = array[y][x]
            i += 1

        x += 1
        output[i] = array[y][x]
        i += 1

    return output


def quantizationToStr(array):
    output = ""
    for i in range(64):
        output += str(int(array[i]))+','

    return output


# RLE every block
import rle
qYentropy = []

for i in range(qYblocks.shape[0]):
    qYentropy.append(rle.encode(entropyData(qYblocks[i])))

# %% Huffman
from dahuffman import HuffmanCodec
# https://pypi.org/project/dahuffman/
# Need to convert to string
