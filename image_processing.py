#!/usr/bin/env python3
"""
Digital Image Processing - Elementary Methods
Implements: Image Negative, Gamma Correction, Logarithmic Transformation,
Contrast Stretching, Histogram Equalization, Intensity Level Slicing,
Bit Plane Slicing.

Works with both RGB and grayscale images.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import math


def load_image(path):
    """Load an image from file, returning as numpy array."""
    img = Image.open(path)
    arr = np.array(img)
    return arr, img.mode


def save_image(arr, path, mode=None):
    """Save a numpy array as an image file."""
    if mode is None:
        mode = "RGB" if arr.ndim == 3 and arr.shape[2] == 3 else "L"
    img = Image.fromarray(arr, mode=mode)
    img.save(path)


def display_images(images, titles, rows=2, cols=3, figsize=(12, 8)):
    """Display multiple images in a grid."""
    plt.figure(figsize=figsize)
    for i, (img, title) in enumerate(zip(images, titles)):
        plt.subplot(rows, cols, i + 1)
        if img.ndim == 2:
            plt.imshow(img, cmap='gray')
        else:
            plt.imshow(img)
        plt.title(title)
        plt.axis('off')
    plt.tight_layout()
    plt.show()


# ==============================
# 1. Image Negative
# ==============================
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


# ==============================
# 2. Gamma Encoding / Correction
# ==============================
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


# ==============================
# 3. Logarithmic Transformation
# ==============================
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


# ==============================
# 4. Contrast Stretching
# ==============================
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


# ==============================
# 5. Histogram Equalization
# ==============================
def histogram_equalization(arr):
    """
    Apply histogram equalization to grayscale or color images.
    For color images, convert to HSV, equalize V channel, convert back.
    Uses numpy only - no external dependencies beyond what's available.
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


# ==============================
# 6. Intensity Level Slicing
# ==============================
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


# ==============================
# 7. Bit Plane Slicing
# ==============================
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


# ==============================
# Main execution - process images
# ==============================
def main():
    # Create output directory
    image_dir = os.path.join(os.path.dirname(__file__), 'images')
    os.makedirs(image_dir, exist_ok=True)

    # Create synthetic test images if they don't exist
    image_files_to_create = []
    type_map = {
        'circle_gray.png': 'circle',
        'rgb_test.png': 'rgb_test',
        'gradient.png': 'gradient',
    }
    for f in ['circle_gray.png', 'rgb_test.png', 'gradient.png']:
        path = os.path.join(image_dir, f)
        if not os.path.exists(path):
            image_files_to_create.append(f)

    if image_files_to_create:
        for f in image_files_to_create:
            img_type = type_map[f]
            create_synthetic_image(os.path.join(image_dir, f), img_type=img_type)
        print(f"Created synthetic images in {image_dir}")

    # Load images
    img_gray_path = os.path.join(image_dir, 'circle_gray.png')
    img_rgb_path = os.path.join(image_dir, 'rgb_test.png')

    arr_gray, mode_gray = load_image(img_gray_path)
    arr_rgb, mode_rgb = load_image(img_rgb_path)

    print(f"Grayscale image: shape={arr_gray.shape}, mode={mode_gray}")
    print(f"RGB image: shape={arr_rgb.shape}, mode={mode_rgb}")

    # ==============================
    # 1. Image Negative
    # ==============================
    print("\n=== 1. Image Negative ===")
    neg_gray = image_negative(arr_gray.copy(), max_val=255)
    neg_rgb = image_negative(arr_rgb.copy(), max_val=255)

    # Save negatives
    save_image(neg_gray, os.path.join(image_dir, 'negative_gray.png'), mode='L')
    save_image(neg_rgb, os.path.join(image_dir, 'negative_rgb.png'), mode='RGB')

    # ==============================
    # 2. Gamma Correction
    # ==============================
    print("\n=== 2. Gamma Correction ===")
    gamma_vals = [0.3, 0.5, 1.0, 2.0, 3.0]

    # Grayscale gamma - vectorized, fast
    gamma_images_gray = []
    for g in gamma_vals:
        gamma_gray = gamma_correction(arr_gray, gamma=g)
        gamma_images_gray.append(gamma_gray)

    # Save gamma corrected images
    for g, img in zip(gamma_vals, gamma_images_gray):
        save_image(img, os.path.join(image_dir, f'gamma_gray_{g}.png'), mode='L')

    # RGB gamma - vectorized, fast
    gamma_images_rgb = []
    for g in gamma_vals:
        gamma_rgb = gamma_correction(arr_rgb, gamma=g)
        gamma_images_rgb.append(gamma_rgb)

    # Save RGB gamma corrected images
    for g, img in zip(gamma_vals, gamma_images_rgb):
        save_image(img, os.path.join(image_dir, f'gamma_rgb_{g}.png'), mode='RGB')

    # ==============================
    # 3. Logarithmic Transformation
    # ==============================
    print("\n=== 3. Logarithmic Transformation ===")
    log_gray = logarithmic_transformation(arr_gray.copy())
    log_rgb = logarithmic_transformation(arr_rgb.copy())

    # Save log transformed images
    save_image(log_gray, os.path.join(image_dir, 'log_gray.png'), mode='L')
    save_image(log_rgb, os.path.join(image_dir, 'log_rgb.png'), mode='RGB')

    # ==============================
    # 4. Contrast Stretching
    # ==============================
    print("\n=== 4. Contrast Stretching ===")
    # Automatic contrast stretching
    contrast_auto_gray = contrast_stretching(arr_gray.copy())
    contrast_auto_rgb = contrast_stretching(arr_rgb.copy())

    # Save contrast stretched images
    save_image(contrast_auto_gray, os.path.join(image_dir, 'contrast_stretched.png'), mode='L')

    # ==============================
    # 5. Histogram Equalization
    # ==============================
    print("\n=== 5. Histogram Equalization ===")
    eq_gray = histogram_equalization(arr_gray.copy())
    eq_rgb = histogram_equalization(arr_rgb.copy())

    # Save equalized images
    save_image(eq_gray, os.path.join(image_dir, 'equalized_gray.png'), mode='L')
    save_image(eq_rgb, os.path.join(image_dir, 'equalized_rgb.png'), mode='RGB')

    # ==============================
    # 6. Intensity Level Slicing
    # ==============================
    print("\n=== 6. Intensity Level Slicing ===")
    # Highlight a range (keep slice, darken rest)
    slicing_highlight = intensity_level_slicing(arr_gray.copy(), background=0, highlight=True, width=20)
    # Darken outside, keep slice
    slicing_darken = intensity_level_slicing(arr_gray.copy(), background=0, highlight=False, width=20)
    # RGB version
    slicing_rgb = intensity_level_slicing(arr_rgb.copy(), background=0, highlight=True, width=30)

    # Save intensity level slicing results
    save_image(slicing_highlight, os.path.join(image_dir, 'intensity_highlight.png'), mode='L')
    save_image(slicing_darken, os.path.join(image_dir, 'intensity_darken.png'), mode='L')

    # ==============================
    # 7. Bit Plane Slicing
    # ==============================
    print("\n=== 7. Bit Plane Slicing ===")
    # Get all bit planes for grayscale
    bit_planes = bit_plane_slicing(arr_gray.copy(), show_all=True)

    # Save bit planes - save MSB (plane 7) and LSB (plane 0)
    save_image(bit_planes[0], os.path.join(image_dir, 'bit_plane_0.png'), mode='L')
    save_image(bit_planes[7], os.path.join(image_dir, 'bit_plane_7.png'), mode='L')  # MSB

    print("\n=== All methods completed successfully! ===")
    print(f"Output images saved to: {image_dir}")


def create_synthetic_image(path, img_type='circle', size=256):
    """Create synthetic test images for demonstration."""
    if img_type == 'circle':
        # Create a circular grayscale image
        img = np.zeros((size, size), dtype=np.uint8)
        y, x = np.ogrid[:size, :size]
        center = size // 2
        radius = size // 3
        mask = (x - center)**2 + (y - center)**2 <= radius**2
        img[mask] = 200  # Bright circle on dark background
        # Add some variation (safe way)
        noise = np.random.randint(0, 30, size=(size, size), dtype=np.int16)
        img_temp = img.astype(np.int16) + noise
        img = np.clip(img_temp, 0, 255).astype(np.uint8)
        Image.fromarray(img, mode='L').save(path)
        return img

    elif img_type == 'rgb_test':
        # Create an RGB test image with varying colors - fully vectorized
        i = np.arange(128)[:, np.newaxis]  # shape (128, 1)
        j = np.arange(128)[np.newaxis, :]  # shape (1, 128)
        img = np.zeros((128, 128, 3), dtype=np.uint8)
        img[:, :, 0] = (i * 2) % 256
        img[:, :, 1] = (j * 2) % 256
        img[:, :, 2] = ((i + j) * 2) % 256
        Image.fromarray(img, mode='RGB').save(path)
        return img

    elif img_type == 'gradient':
        # Create a gradient grayscale image
        img = np.arange(256, dtype=np.uint8).reshape(256, 1)
        # Tile it
        img = np.tile(img, (1, 256))
        # Add another gradient perpendicular
        img2 = np.arange(256, dtype=np.uint8).reshape(1, 256)
        img2 = np.tile(img2, (256, 1))
        img = (img + img2) // 2
        Image.fromarray(img, mode='L').save(path)
        return img


if __name__ == '__main__':
    main()