# Digital Image Processing - Elementary Methods

## Assignment Overview

This repository contains Python implementations of seven elementary image processing methods, along with a PowerPoint report illustrating the results. The assignment covers fundamental techniques for image enhancement and analysis.

### Directory Structure

```
D:\Projects\Digital-image-processing\
├── images/                    # Input images
│   ├── color/                # Flower.png, Nature.jpg
│   └── grayscale/            # Cameraman.png, Fingerprint.png
├── outputs/                   # NEW: Output subfolders for each method
│   ├── 01_negative/          # Image Negative results
│   ├── 02_gamma/             # Gamma Correction (γ=0.3,0.5,1.0,2.0,3.0)
│   ├── 03_logarithmic/       # Logarithmic Transformation results
│   ├── 04_contrast/          # Contrast Stretching results
│   ├── 05_histogram/         # Histogram Equalization results
│   ├── 06_intensity_slicing/ # Intensity Level Slicing results
│   └── 07_bit_plane/         # Bit Plane Slicing results (8 planes)
├── src/                      # NEW: Individual method modules
│   ├── __init__.py           # Exports all 7 methods + utilities
│   ├── image_negative.py     # Image negative transformation
│   ├── gamma_correction.py   # Gamma correction/encoding
│   ├── logarithmic.py        # Logarithmic transformation
│   ├── contrast_stretching.py# Contrast stretching
│   ├── histogram_equalization.py # Histogram equalization
│   ├── intensity_slicing.py  # Intensity level slicing
│   └── bit_plane_slicing.py  # Bit plane slicing
├── main.py                   # Updated main script using src modules
├── generate_ppt.py           # PPT generation script (15 slides)
├── requirements.txt
├── README.md
└── .venv/                    # Python virtual environment
```

## Methods Implemented

All methods handle both grayscale (2D) and RGB (3D) images.

### 1. Image Negative
- **Formula**: s = L - 1 - r (for 8-bit: s = 255 - r)
- **Effect**: Inverts pixel values; bright areas become dark and vice versa
- **Applications**: Medical imaging, document processing, artistic effects
- **Output**: `outputs/01_negative/negative_gray.png`, `negative_rgb.png`

### 2. Gamma Encoding / Correction
- **Formula**: s = 255 · (r/255)^γ
- **Tested γ values**: 0.3, 0.5, 1.0, 2.0, 3.0
- **γ < 1**: Brightens image, expands dark regions
- **γ = 1**: No change (linear transformation)
- **γ > 1**: Darkens image, compresses highlights
- **Use case**: Display monitor calibration (γ ≈ 2.2)
- **Output**: `outputs/02_gamma/` with 5 gamma values for both grayscale and RGB

### 3. Logarithmic Transformation
- **Formula**: s = c · log(1 + r)
- **Effect**: Expands dark regions, compresses bright regions
- **Human vision**: Mimics logarithmic response of human eye to light
- **Applications**: Astronomy, radiography, low-light photography
- **Output**: `outputs/03_logarithmic/log_gray.png`, `log_rgb.png`

### 4. Contrast Stretching
- **Formula**: s = (r - r_min) / (r_max - r_min) · (s_max - s_min) + s_min
- **Automatic version**: Uses 2nd and 98th percentile for r_min, r_max
- **Effect**: Maps specified intensity range to full 0-255 range
- **Applications**: Medical imaging, satellite imagery, display enhancement
- **Output**: `outputs/04_contrast/contrast_stretched.png` (grayscale and RGB)

### 5. Histogram Equalization
- **Formula**: s_k = T(r_k) = (CDF(r_k) - CDF_min) / (N - CDF_min) · (L - 1)
- **For color images**: Applied to HSV V (value) channel
- **Effect**: Redistributes pixel intensities for approximately uniform histogram
- **Applications**: General contrast enhancement, medical imaging, photography
- **Output**: `outputs/05_histogram/equalized_gray.png`, `equalized_rgb.png`, `histograms.png`

### 6. Intensity Level Slicing
- **Two modes**:
  - **Highlight**: Pixels in range → 255, outside → 0
  - **Darken**: Pixels in range → original, outside → 0
- **Parameters**: Adjustable intensity range width
- **Applications**: Tumor highlighting, feature enhancement, segmentation
- **Output**: `outputs/06_intensity_slicing/intensity_highlight.png`, `intensity_darken.png`

### 7. Bit Plane Slicing
- **8 bit planes**: Plane 0 (LSB) to Plane 7 (MSB)
- **MSB (Plane 7)**: Contains major structural information
- **LSB (Plane 0)**: Contains fine detail and minor noise
- **Information theory**: Typically 3-4 MSB planes contain ~90% of image information
- **Applications**: Image compression analysis, watermarking, error detection
- **Output**: `outputs/07_bit_plane/bit_plane_0.png` (LSB), `bit_plane_7.png` (MSB), `bit_planes_all.png`

## File Structure

```
D:\Projects\Digital-image-processing\
├── .venv/                 # Python virtual environment
├── images/                # Input images (color + grayscale)
├── outputs/               # 7 method output folders (01-07)
├── src/                   # 7 method modules + utilities
│   ├── __init__.py
│   ├── image_negative.py
│   ├── gamma_correction.py
│   ├── logarithmic.py
│   ├── contrast_stretching.py
│   ├── histogram_equalization.py
│   ├── intensity_slicing.py
│   └── bit_plane_slicing.py
├── main.py                # Main script - runs all 7 methods
├── generate_ppt.py        # Generates 15-slide PPT report
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.x
- NumPy
- Matplotlib
- Pillow (PIL)
- OpenCV (cv2) - optional, used for color conversions

## Installation

```bash
pip install numpy matplotlib pillow opencv-python
```

## Usage

### Running the Main Script

```bash
python main.py
```

This will:
- Process both color (Flower.png) and grayscale (Cameraman.png) images
- Generate all 7 image processing methods
- Save outputs to `outputs/01_negative/` through `outputs/07_bit_plane/`

### Generating the PowerPoint Report

```bash
python generate_ppt.py
```

This will create `Digital_Image_Processing_Assignment.pptx` with 15 slides:
- Slide 1: Title and student information
- Slide 2: Introduction to Digital Image Processing
- Slide 3: Objectives and tools used
- Slides 4-10: Each of the 7 image processing methods with input/output images and descriptions
- Slide 11: RGB vs Grayscale comparison
- Slide 12: Results and observations (analysis of all 7 methods)
- Slide 13: Challenges encountered during implementation
- Slide 14: Conclusion
- Slide 15: References

### Using the src Modules

```python
from src import image_negative, gamma_correction, load_image, save_image

# Load image
arr, mode = load_image('images/grayscale/Cameraman.png', grayscale=True)

# Apply a method
result = image_negative(arr, max_val=255)

# Save result
save_image(result, 'outputs/01_negative/result.png', mode='L')
```

### Importing All Methods

```python
from src import (
    image_negative,
    gamma_correction,
    logarithmic_transformation,
    contrast_stretching,
    histogram_equalization,
    intensity_level_slicing,
    bit_plane_slicing,
    load_image,
    save_image,
    display_images
)
```

## Output Description

After running `main.py`, the `outputs/` directory contains:

| Folder | Contains |
|--------|----------|
| `01_negative/` | Image negative results (grayscale + RGB) |
| `02_gamma/` | Gamma-corrected images with γ=0.3, 0.5, 1.0, 2.0, 3.0 |
| `03_logarithmic/` | Log-transformed images (grayscale + RGB) |
| `04_contrast/` | Contrast-stretched images (auto percentile-based) |
| `05_histogram/` | Histogram-equalized images (grayscale + RGB + histograms) |
| `06_intensity_slicing/` | Intensity-sliced images (highlight + darken modes) |
| `07_bit_plane/` | Bit plane slices (LSB, MSB, and all 8 planes) |

## License

This is an individual assignment for Digital Image Processing course.