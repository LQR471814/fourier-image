import cv2
import imageio.v3 as iio
import numpy as np
from matplotlib import pyplot as plt
from scipy import ndimage
from skimage import feature, io

roberts_cross_v = np.array([[1, 0],
                            [0, -1]])

roberts_cross_h = np.array([[0, 1],
                            [-1, 0]])


def denoise(img, strength):
    return cv2.fastNlMeansDenoising(img, strength, strength, 7, 21)


def contrast(img, gate_at):
    mask = cv2.inRange(img, np.array(
        [0]), np.array([gate_at])).astype('float64')
    return cv2.subtract(img, mask)


def roberts_cross(
    input: string,
    output: string,
    denoise_strength=10,
    brightness_boost=2,
    brightness_gate=100,
):
    img = denoise(cv2.imread(input, 0), denoise_strength)
    img = img.astype('float64')

    img /= 255.0
    vertical = ndimage.convolve(img, roberts_cross_v)
    horizontal = ndimage.convolve(img, roberts_cross_h)

    edged_img = np.sqrt(np.square(horizontal) + np.square(vertical))
    edged_img *= 255
    edged_img = edged_img**brightness_boost
    edged_img = contrast(edged_img, brightness_gate)
    cv2.imwrite(output, edged_img)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Preprocess',
        description='Runs edge detection and brightness gating on images.')

    parser.add_argument('-i', '--input', required=True)
    parser.add_argument('-o', '--output', default="output.png")

    args = parser.parse_args()
    roberts_cross(args.input, args.output)
