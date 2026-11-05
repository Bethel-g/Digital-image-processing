#!/usr/bin/env python3
"""
Digital Image Processing - Elementary Methods
Bit Plane Slicing

Extract bit planes from an image.
8 bit planes: Plane 0 (LSB) to Plane 7 (MSB).
"""

import numpy as np


def bit_plane_slicing(arr, plane=None, show_all=False):
    """
    Extract bit planes from an image.

    Parameters:
    - arr: input image (grayscale or RGB)
    - plane: specific bit plane index (0-7 for 8-bit), None to show all
    - show_all: if True and plane is None, return all 8 bit planes

    Returns:
    - bit plane(s) as image array(s) - each scaled to 0-255 for visibility
    """
    # Ensure uint8
    if arr.dtype != np.uint8:
        arr = arr.astype(np.uint8)

    if arr.ndim == 2:
        # Grayscale
        bit_planes = []
        for i in range(8):
            # Extract i-th bit: (arr >> i) & 1, then scale to 0-255
            plane_img = ((arr >> i) & 1) * 255
            bit_planes.append(plane_img.astype(np.uint8))

        if show_all:
            return bit_planes
        elif plane is not None:
            if 0 <= plane <= 7:
                return bit_planes[plane]
            else:
                raise ValueError("Plane index must be between 0 and 7")
        else:
            return bit_planes[0]  # default to first

    else:
        # RGB - extract bit planes from each channel combined
        bit_planes = []
        for i in range(8):
            # For each bit plane, OR together the contribution from all three channels
            # Each channel contributes 0 or 255 at position i
            plane_img = np.zeros((arr.shape[0], arr.shape[1]), dtype=np.uint8)
            for c in range(3):
                plane_img += (((arr[:, :, c] >> i) & 1) * 255)
            bit_planes.append(plane_img.astype(np.uint8))

        if show_all:
            return bit_planes
        elif plane is not None:
            if 0 <= plane <= 7:
                return bit_planes[plane]
            else:
                raise ValueError("Plane index must be between 0 and 7")
        else:
            return bit_planes[0]  # default to first