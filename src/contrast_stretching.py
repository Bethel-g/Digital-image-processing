#!/usr/bin/env python3
"""
Digital Image Processing - Elementary Methods
Contrast Stretching

Formula: s = (r - r_min) / (r_max - r_min) * (s_max - s_min) + s_min
Automatic range detection using percentiles if not specified.
"""

import numpy as np


def contrast_stretching(arr, min_in=None, max_in=None, min_out=0, max_out=255):
    """
    Apply contrast stretching (linearization).
    Maps input range [min_in, max_in] to [min_out, max_out].
    Automatic range detection using percentiles if not specified.
    """
    # Determine input range using percentiles for robustness
    if min_in is None:
        min_in = np.percentile(arr, 2)
    if max_in is None:
        max_in = np.percentile(arr, 98)

    # Avoid division by zero
    if max_in == min_in:
        return np.full_like(arr, min_out, dtype=np.uint8 if arr.dtype == np.uint8 else arr.dtype)

    # Apply linear mapping: s = min_out + ((r - min_in) / (max_in - min_in)) * (max_out - min_out)
    normalized = (arr.astype(np.float64) - min_in) / (max_in - min_in)
    result = min_out + normalized * (max_out - min_out)
    result = np.clip(result, min_out, max_out)
    if arr.dtype == np.uint8:
        result = result.astype(np.uint8)
    return result