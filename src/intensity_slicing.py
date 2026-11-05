#!/usr/bin/env python3
"""
Digital Image Processing - Elementary Methods
Intensity Level Slicing

Isolate a specific intensity range:
- Highlight mode: Pixels in range → 255, outside → 0
- Darken mode: Pixels in range → original, outside → 0
"""

import numpy as np


def intensity_level_slicing(arr, background=0, highlight=True, slice_level=None, width=10):
    """
    Intensity level slicing: isolate a specific intensity range.

    Parameters:
    - arr: input image array
    - background: background value for pixels outside the slice (0 or 255)
    - highlight: True to highlight the slice (set to 255/bright), False to darken outside
    - slice_level: (min, max) intensity range; if None, uses center range around mean
    - width: width of the intensity range around center (if slice_level not specified)

    Returns:
    - sliced image
    """
    if slice_level is not None:
        low, high = slice_level
    else:
        # Use center range around mean
        if arr.ndim == 2:
            mid = np.median(arr)
        else:
            mid = np.median(arr.mean(axis=2))
        low = max(0, int(mid) - width)
        high = min(255, int(mid) + width)

    result = arr.copy().astype(np.float64)

    if arr.ndim == 2:
        # Grayscale
        mask = (result >= low) & (result <= high)
        if highlight:
            # Keep slice at 255, set rest to background
            result[~mask] = background
            result[mask] = 255.0
        else:
            # Darken outside to background, keep slice values
            result[~mask] = background
            # Keep slice values as-is (already in result)
    else:
        # RGB - apply mask based on luminance or per-channel
        # Create a composite mask: a pixel is "in range" if ANY channel is in range
        # Or we can apply the slicing per channel
        for c in range(3):
            mask = (result[:, :, c] >= low) & (result[:, :, c] <= high)
            if highlight:
                result[:, :, c][~mask] = background
                result[:, :, c][mask] = 255.0
            else:
                result[:, :, c][~mask] = background

    return result.astype(np.uint8)