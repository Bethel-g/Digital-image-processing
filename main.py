# Digital Image Processing - Elementary Methods
# Main script using src module structure

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

# Add src to path
sys.path.insert(0, os.path.dirname(__file__))

from src import (
    image_negative,
    gamma_correction,
    logarithmic_transformation,
    contrast_stretching,
    histogram_equalization,
    intensity_level_slicing,
    bit_plane_slicing,
)
from src.__init__ import load_image, save_image, display_images


def main():
    # Create output directories
    outputs = [
        "outputs/01_negative",
        "outputs/02_gamma",
        "outputs/03_logarithmic",
        "outputs/04_contrast",
        "outputs/05_histogram",
        "outputs/06_intensity_slicing",
        "outputs/07_bit_plane",
    ]
    for out_dir in outputs:
        os.makedirs(out_dir, exist_ok=True)

    # Load images
    base_dir = os.path.dirname(__file__)
    img_color_path = os.path.join(base_dir, "images", "color", "Flower.png")
    img_gray_path = os.path.join(base_dir, "images", "grayscale", "Cameraman.png")

    # Load color image (RGB)
    arr_color, mode_color = load_image(img_color_path)
    if arr_color is None:
        raise FileNotFoundError("Color image not found!")

    # Load grayscale image
    arr_gray, mode_gray = load_image(img_gray_path, grayscale=True)
    if arr_gray is None:
        raise FileNotFoundError("Grayscale image not found!")

    print(f"Color image: shape={arr_color.shape}, mode={mode_color}")
    print(f"Grayscale image: shape={arr_gray.shape}, mode={mode_gray}")

    # ==============================
    # 1. Image Negative
    # ==============================
    print("\n=== 1. Image Negative ===")
    neg_gray = image_negative(arr_gray.copy(), max_val=255)
    neg_rgb = image_negative(arr_color.copy(), max_val=255)

    # Save negatives
    save_image(neg_gray, os.path.join("outputs", "01_negative", "negative_gray.png"), mode="L")
    save_image(neg_rgb, os.path.join("outputs", "01_negative", "negative_rgb.png"), mode="RGB")
    print("Saved: outputs/01_negative/negative_gray.png")
    print("Saved: outputs/01_negative/negative_rgb.png")

    # ==============================
    # 2. Gamma Correction
    # ==============================
    print("\n=== 2. Gamma Correction ===")
    gamma_vals = [0.3, 0.5, 1.0, 2.0, 3.0]

    # Grayscale gamma
    print("Processing grayscale gamma corrections...")
    for g in gamma_vals:
        gamma_gray = gamma_correction(arr_gray, gamma=g)
        save_image(
            gamma_gray,
            os.path.join("outputs", "02_gamma", f"gamma_gray_{g:.1f}.png"),
            mode="L",
        )
        print(f"  gamma={g}: saved")

    # RGB gamma
    print("Processing RGB gamma corrections...")
    for g in gamma_vals:
        gamma_rgb = gamma_correction(arr_color, gamma=g)
        save_image(
            gamma_rgb,
            os.path.join("outputs", "02_gamma", f"gamma_rgb_{g:.1f}.png"),
            mode="RGB",
        )
        print(f"  gamma={g}: saved")

    # ==============================
    # 3. Logarithmic Transformation
    # ==============================
    print("\n=== 3. Logarithmic Transformation ===")
    log_gray = logarithmic_transformation(arr_gray.copy())
    log_rgb = logarithmic_transformation(arr_color.copy())

    # Save log transformed images
    save_image(log_gray, os.path.join("outputs", "03_logarithmic", "log_gray.png"), mode="L")
    save_image(log_rgb, os.path.join("outputs", "03_logarithmic", "log_rgb.png"), mode="RGB")
    print("Saved: outputs/03_logarithmic/log_gray.png")
    print("Saved: outputs/03_logarithmic/log_rgb.png")

    # ==============================
    # 4. Contrast Stretching
    # ==============================
    print("\n=== 4. Contrast Stretching ===")
    # Automatic contrast stretching
    contrast_auto_gray = contrast_stretching(arr_gray.copy())
    contrast_auto_rgb = contrast_stretching(arr_color.copy())

    # Save contrast stretched images
    save_image(contrast_auto_gray, os.path.join("outputs", "04_contrast", "contrast_stretched.png"), mode="L")
    save_image(contrast_auto_rgb, os.path.join("outputs", "04_contrast", "contrast_stretched_rgb.png"), mode="RGB")
    print("Saved: outputs/04_contrast/contrast_stretched.png")
    print("Saved: outputs/04_contrast/contrast_stretched_rgb.png")

    # ==============================
    # 5. Histogram Equalization
    # ==============================
    print("\n=== 5. Histogram Equalization ===")
    eq_gray = histogram_equalization(arr_gray.copy())
    eq_rgb = histogram_equalization(arr_color.copy())

    # Save equalized images
    save_image(eq_gray, os.path.join("outputs", "05_histogram", "equalized_gray.png"), mode="L")
    save_image(eq_rgb, os.path.join("outputs", "05_histogram", "equalized_rgb.png"), mode="RGB")
    print("Saved: outputs/05_histogram/equalized_gray.png")
    print("Saved: outputs/05_histogram/equalized_rgb.png")

    # ==============================
    # 6. Intensity Level Slicing
    # ==============================
    print("\n=== 6. Intensity Level Slicing ===")
    # Highlight a range (keep slice, brighten)
    slicing_highlight = intensity_level_slicing(arr_gray.copy(), background=0, highlight=True, width=20)
    # Darken outside, keep slice
    slicing_darken = intensity_level_slicing(arr_gray.copy(), background=0, highlight=False, width=20)
    # RGB version
    slicing_rgb = intensity_level_slicing(arr_color.copy(), background=0, highlight=True, width=30)

    # Save intensity level slicing results
    save_image(slicing_highlight, os.path.join("outputs", "06_intensity_slicing", "intensity_highlight.png"), mode="L")
    save_image(slicing_darken, os.path.join("outputs", "06_intensity_slicing", "intensity_darken.png"), mode="L")
    save_image(slicing_rgb, os.path.join("outputs", "06_intensity_slicing", "intensity_rgb.png"), mode="RGB")
    print("Saved: outputs/06_intensity_slicing/intensity_highlight.png")
    print("Saved: outputs/06_intensity_slicing/intensity_darken.png")
    print("Saved: outputs/06_intensity_slicing/intensity_rgb.png")

    # ==============================
    # 7. Bit Plane Slicing
    # ==============================
    print("\n=== 7. Bit Plane Slicing ===")
    # Get all bit planes for grayscale
    bit_planes = bit_plane_slicing(arr_gray.copy(), show_all=True)

    # Save bit planes - save LSB (plane 0) and MSB (plane 7)
    save_image(bit_planes[0], os.path.join("outputs", "07_bit_plane", "bit_plane_0.png"), mode="L")
    save_image(bit_planes[7], os.path.join("outputs", "07_bit_plane", "bit_plane_7.png"), mode="L")  # MSB
    print("Saved: outputs/07_bit_plane/bit_plane_0.png (LSB)")
    print("Saved: outputs/07_bit_plane/bit_plane_7.png (MSB)")

    # Also save all bit planes as a grid
    # Create a combined image showing all 8 bit planes
    fig, axes = plt.subplots(2, 4, figsize=(12, 6))
    for i in range(8):
        row = i // 4
        col = i % 4
        axes[row, col].imshow(bit_planes[i], cmap="gray")
        axes[row, col].set_title(f"Plane {i} (2^{i})")
        axes[row, col].axis("off")
    plt.tight_layout()
    plt.savefig(os.path.join("outputs", "07_bit_plane", "bit_planes_all.png"), dpi=100)
    plt.close()
    print("Saved: outputs/07_bit_plane/bit_planes_all.png")

    print("\n=== All methods completed successfully! ===")
    print("Output images saved to: outputs/")


def load_image(path, grayscale=False):
    """Load an image from file, returning as numpy array and mode."""
    from PIL import Image
    import cv2

    if grayscale:
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            # Try PIL
            pil_img = Image.open(path)
            img = np.array(pil_img.convert("L"))
        return img, "L"
    else:
        img = cv2.imread(path)
        if img is None:
            # Try PIL
            pil_img = Image.open(path)
            img = np.array(pil_img.convert("RGB"))
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # OpenCV reads BGR
        return img, "BGR" if img.ndim == 3 else "L"


if __name__ == "__main__":
    main()