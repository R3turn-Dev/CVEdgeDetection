from PIL import Image
import argparse
import numpy as np


parser = argparse.ArgumentParser(description="Convert image into a grayscale image.")
parser.add_argument("image", nargs="*", help="Path to a specific image file.")


SCALE_R = 1/3
SCALE_G = 1/3
SCALE_B = 1/3


def main(images):
    for image in images:
        process(image)


def process(image):
    img = Image.open(image)
    # img.show()
    img_array = np.array(img)
    gray_array = img_array[:, :, 0]*SCALE_R + img_array[:, :, 1]*SCALE_G + img_array[:, :, 2]*SCALE_B
    gray_image = Image.fromarray(gray_array)
    # gray_image.show()

    print(gray_array)


if __name__ == "__main__":
    args = parser.parse_args()
    images = args.image

    if not images:
        print("Please specify a path to an image file.")
        exit(-1)

    main(images)
