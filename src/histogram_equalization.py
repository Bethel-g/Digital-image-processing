#!/usr/bin/env python3
"""
Digital Image Processing - Elementary Methods
Histogram Equalization

For color images, convert to HSV, equalize V channel, convert back.
Uses numpy only - no external dependencies beyond what's available.
"""

import numpy as np


def histogram_equalization(arr):
    """
    Apply histogram equalization to grayscale or color images.
    For color images, convert to HSV, equalize V channel, convert back.
    """
    if arr.ndim == 2:
        # Grayscale histogram equalization
        img = arr.astype(np.float64)

        # Compute histogram
        hist, bins = np.histogram(img.ravel(), 256, [0.0, 256.0])

        # Compute CDF
        cdf = hist.cumsum()

        # Mask zeros and normalize
        cdf_masked = np.ma.masked_equal(cdf, 0)
        # Normalize CDF to [0, 255]
        if cdf_masked[-1] > 0:
            cdf_normalized = (cdf_masked - cdf_masked[0]) * 255 / (img.size - cdf_masked[0])
        else:
            cdf_normalized = cdf_masked

        # Fill back and use for mapping
        cdf_full = np.ma.filled(cdf_normalized, 0).astype(np.uint8)

        # Map using the CDF
        equalized = cdf_full[np.round(img).astype(np.uint8)]

        return equalized

    else:
        # RGB: convert to YCrCb, equalize Y channel, convert back
        img_float = arr.astype(np.float64)

        # RGB to YCrCb transformation (NTSC standard)
        # Y  = 0.299 R + 0.587 G + 0.114 B
        # Cr = 0.5 R - 0.168 G - 0.331 B + 128
        # Cb = -0.168 R - 0.331 G + 0.5 B + 128

        # Extract channels
        r = img_float[:, :, 0]
        g = img_float[:, :, 1]
        b = img_float[:, :, 2]

        # Compute Y (luminance)
        y = 0.299 * r + 0.587 * g + 0.114 * b

        # Equalize Y channel
        y_eq = histogram_equalization(y)

        # Compute inverse transformation
        # R = Y + 1.402 * (Cr - 128) where Cr = 0.5*R - 0.168*G - 0.331*B + 128
        # G = Y - 0.344136*(Cr-128) - 0.714136*(Cb-128) where Cb = -0.168*R - 0.331*G + 0.5*B + 128
        # B = Y + 1.772 * (Cb - 128)

        # Recover Cr and Cb from original
        cr = 0.5 * r - 0.168 * g - 0.331 * b + 128
        cb = -0.168 * r - 0.331 * g + 0.5 * b + 128

        # Recombine RGB
        r_eq = np.clip(y_eq + 1.402 * (cr - 128), 0, 255)
        g_eq = np.clip(y_eq - 0.344136 * (cr - 128) - 0.714136 * (cb - 128), 0, 255)
        b_eq = np.clip(y_eq + 1.772 * (cb - 128), 0, 255)

        result = np.stack([r_eq, g_eq, b_eq], axis=2).astype(np.uint8)
        return result