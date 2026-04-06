import numpy as np
import cv2
from scipy.signal import wiener
from bm3d import bm3d



# -----------------------------
# DENOISING FUNCTIONS
# -----------------------------
def apply_wiener(img):
    return wiener(img, (5,5))


def apply_bm3d(img):
    return bm3d(img, sigma_psd=0.05)


# -----------------------------
# MAIN PROCESS FUNCTION
# -----------------------------
def process_image(file_path):

    img = cv2.imread(
        file_path,
        cv2.IMREAD_GRAYSCALE
    )

    img = img / 255.0

    # Apply filters
    wiener_img = apply_wiener(img)
    bm3d_img = apply_bm3d(img)


    return img, wiener_img, bm3d_img 