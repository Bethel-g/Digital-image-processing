#!/usr/bin/env python3
"""
Digital Image Processing - Elementary Methods
Gamma Encoding / Correction

Formula: s = 255 * (r/255)^gamma
Works for both grayscale and RGB using vectorized numpy operations.
"""

import numpy as np


def gamma_correction(arr, gamma, max_val=255):
    """
    Apply gamma correction/encoding.
    s = 255 * (r/255)^gamma
    Works for both grayscale and RGB using vectorized numpy operations.
    """
    # Normalize to [0,1]
    normalized = arr.astype(np.float64) / max_val

    # Apply gamma: power law transformation
    result = np.power(normalized, gamma) * max_val

    # Clip and convert back
    result = np.clip(result, 0, max_val)
    if arr.dtype == np.uint8:
        result = result.astype(np.uint8)
    return result