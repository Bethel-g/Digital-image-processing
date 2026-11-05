#!/usr/bin/env python3
"""
Digital Image Processing - Elementary Methods
Image Negative Transformation

Formula: s = L - 1 - r (for 8-bit: s = 255 - r)
Works for both grayscale (2D) and RGB (3D) images.
"""

import numpy as np


def image_negative(arr, max_val=255):
    """
    Apply image negative transformation.
    s = L - 1 - r  (for 8-bit: L=255)
    Works for both grayscale (2D) and RGB (3D) images.
    """
    # Vectorized: invert pixel values
    result = max_val - arr

    # Clip and convert to uint8 if needed
    if arr.dtype == np.uint8:
        result = np.clip(result, 0, 255).astype(np.uint8)
    return result