from PIL import Image
import scipy
import numpy as np
from datetime import datetime


SCALE_R = 1/3
SCALE_G = 1/3
SCALE_B = 1/3

DOWNSCALE = 4

BASE = datetime.now()
print(" > Open Image ", end="")
img = Image.open("bnw.jpg")
img_array = np.array(img)
print(datetime.now() - BASE)

BASE = datetime.now()
print(f" > Resizing into 1/{DOWNSCALE**2} ", end="")
resize_array = np.zeros((img_array.shape[0]//DOWNSCALE, img_array.shape[1]//DOWNSCALE, img_array.shape[2]))
"""for x in range(0, img_array.shape[0], DOWNSCALE):
    for y in range(0, img_array.shape[1], DOWNSCALE):
        temp = np.zeros((1, 1, resize_array.shape[2]))

        for _x in range(DOWNSCALE):
            if x//DOWNSCALE + _x < resize_array.shape[0]:
                for _y in range(DOWNSCALE):
                    if y//DOWNSCALE + _y < resize_array.shape[1]:
                        a, b = x//DOWNSCALE + _x, y//DOWNSCALE + _y
                        temp += resize_array[x//DOWNSCALE + _x, y//DOWNSCALE + _y, :]//(DOWNSCALE**2)

        resize_array[x//DOWNSCALE, y//DOWNSCALE, :] = temp"""
resize_array = img_array
print(datetime.now() - BASE)

BASE = datetime.now()
print(" > Grayscale ", end="")
gray_array = resize_array[:, :, 0] * SCALE_R + resize_array[:, :, 1] * SCALE_G + resize_array[:, :, 2] * SCALE_B
print(datetime.now() - BASE)

BASE = datetime.now()
print(" > Calc Gradient ", end="")
mean = gray_array.mean()
gradient = np.zeros(gray_array.shape)

for x in range(gray_array.shape[0]):
    for y in range(gray_array.shape[1]):
        if x == gray_array.shape[0] - 1 or y == gray_array.shape[1] - 1:
                gradient[x, y] = 0

        else:
            if gray_array[x, y] >= mean:
                gradient[x, y] = 255
            else:
                gradient[x, y] = 0
print(datetime.now() - BASE)

BASE = datetime.now()
print(" > Calc Gradient scipy ", end="")
gradient_sci = scipy.ndimage.sobel(gray_array)
print(datetime.now() - BASE)

gradient_image = Image.fromarray(gradient)
gradient_image.show()
graydient_scipy_image = Image.fromarray(gradient_sci)
graydient_scipy_image.show()
