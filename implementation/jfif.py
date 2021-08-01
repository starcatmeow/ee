#!/usr/bin/eval python3

# %%
# Importing libraries
import numpy as np
from matplotlib import pyplot as plt
import imageio as im

# %%
# Importing image
image = im.imread("./Photos/cables.bmp")
# image = im.imread('imageio:astronaut.png')

# Image Dimentions
print(f'Size: {image.size}')
print(f'Shape: {image.shape}')

# Vertifying rgb bit size
print(f'Max: {image.max()}, Min: {image.min()}')

# %%
# Plotting Image
plt.imshow(image)
plt.show()

# %% Showing R Channel
redChannel = np.zeros(image.shape, dtype=np.uint8)
for i in range(image.shape[0]):
    for j in range(image.shape[1]):
        redChannel[i][j][0] = image[i][j][0]

plt.title('R channel')
plt.ylabel('Height {}'.format(image.shape[0]))
plt.xlabel('Width {}'.format(image.shape[1]))

plt.imshow(redChannel)
plt.show()

# %% Showing G Channel
greenChannel = np.zeros(image.shape, dtype=np.uint8)
for i in range(image.shape[0]):
    for j in range(image.shape[1]):
        greenChannel[i][j][1] = image[i][j][1]

plt.title('G channel')
plt.ylabel('Height {}'.format(image.shape[0]))
plt.xlabel('Width {}'.format(image.shape[1]))

plt.imshow(greenChannel)
plt.show()

# %% Showing B Channel
blueChannel = np.zeros(image.shape, dtype=np.uint8)
for i in range(image.shape[0]):
    for j in range(image.shape[1]):
        blueChannel[i][j][2] = image[i][j][2]

plt.title('B channel')
plt.ylabel('Height {}'.format(image.shape[0]))
plt.xlabel('Width {}'.format(image.shape[1]))

plt.imshow(blueChannel)
plt.show()
