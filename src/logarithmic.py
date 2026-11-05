#!/usr/bin/env python3
"""
Digital Image Processing - Elementary Methods
Logarithmic Transformation

Formula: s = c * log(1 + r)
Expands dark regions, compresses bright regions.
Works for both grayscale and RGB.
"""

import numpy as np
import math


def logarithmic_transformation(arr, c=None, eps=1e-3):
    """
    Apply logarithmic transformation: s = c * log(1 + r)
    Works for both grayscale and RGB.
    """
    if c is None:
        # For 8-bit images, set c to maximize output range
        c = 255 / math.log(1 + 255) if arr.dtype == np.uint8 else 1.0

    # Apply log transformation with epsilon to avoid log(0)
    result = c * np.log(1 + arr.astype(np.float64) + eps - eps)

    # Normalize to 0-255 range
    result = (result - result.min()) / (result.max() - result.min()) * 255
    result = np.clip(result, 0, 255).astype(np.uint8)
    return result