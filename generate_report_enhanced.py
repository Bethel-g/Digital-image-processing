#!/usr/bin/env python3
"""
Generate an attractive and descriptive PPT report for Digital Image Processing Elementary Methods.
Creates a professional PowerPoint presentation with input, output, and detailed analysis for all 7 methods.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
import subprocess


def set_slide_background(slide, color=RGBColor(0xF8, 0xF8, 0xF8)):
    """Set slide background color."""
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_textbox(slide, left, top, width, height, text, font_size=12, bold=False, color=RGBColor(0x33, 0x33, 0x33), alignment=PP_ALIGN.LEFT):
    """Add a styled text box."""
    txBox = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = txBox.text_frame
    tf.text = text
    p = tf.paragraphs[0]
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.alignment = alignment
    return txBox


def add_image_with_caption(slide, left, top, width, image_path, caption, caption_size=9):
    """Add an image with a caption below it."""
    try:
        # Add image
        pic = slide.shapes.add_picture(Inches(image_path) if False else image_path,
                                       Inches(left), Inches(top), width=Inches(width))
        
        # Add caption
        add_textbox(slide, left, top + width + 0.1, width, 0.4, caption, 
                    font_size=caption_size, color=RGBColor(0x55, 0x55, 0x55))
        return True
    except Exception as e:
        # Add placeholder if image missing
        add_textbox(slide, left, top, width, 1.5, f"Image not available: {caption}", 
                    font_size=10, color=RGBColor(0xCC, 0x00, 0x00))
        return False


def add_section_header(slide, text, font_size=28, color=RGBColor(0x00, 0x6E, 0xB0)):
    """Add a styled section header."""
    add_textbox(slide, 0.5, 0.3, 12, 0.6, text, font_size=font_size, 
                bold=True, color=color, alignment=PP_ALIGN.LEFT)


def add_method_title(slide, text, font_size=20, color=RGBColor(0x00, 0x6E, 0xB0)):
    """Add a method title."""
    add_textbox(slide, 0.5, 1.1, 12, 0.4, text, font_size=font_size,
                bold=True, color=color)


def main():
    image_dir = os.path.join(os.path.dirname(__file__), 'images')
    os.makedirs(image_dir, exist_ok=True)
    
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Color scheme
    DARK_BLUE = RGBColor(0x00, 0x6E, 0xB0)
    MEDIUM_BLUE = RGBColor(0x00, 0x96, 0xD6)
    LIGHT_BLUE = RGBColor(0xD4, 0xE6, 0xF1)
    DARK_GRAY = RGBColor(0x33, 0x33, 0x33)
    MEDIUM_GRAY = RGBColor(0x66, 0x66, 0x66)
    ACCENT_ORANGE = RGBColor(0xE8, 0x6C, 0x00)
    WHITE = RGBColor(0xFF, 0xFF, 0xFF)
    
    # ==============================
    # SLIDE 1: Title Slide
    # ==============================
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout
    set_slide_background(slide, LIGHT_BLUE)
    
    # Large title
    add_textbox(slide, 1.5, 1.5, 10.5, 1.5,
                "Digital Image Processing", font_size=44, bold=True, color=DARK_BLUE,
                alignment=PP_ALIGN.CENTER)
    
    add_textbox(slide, 1.5, 2.8, 10.5, 1.0,
                "Elementary Methods - Assignment Implementation", font_size=28, 
                bold=False, color=MEDIUM_BLUE, alignment=PP_ALIGN.CENTER)
    
    # Divider line
    shape = slide.shapes.add_shape(1, Inches(4.5), Inches(3.9), Inches(4.5), Pt(2))
    shape.fill.solid()
    shape.fill.fore_color.rgb = DARK_BLUE
    
    add_textbox(slide, 1.5, 4.3, 10.5, 0.6,
                "C: Digital Image Processing Assignment", font_size=16, 
                color=MEDIUM_GRAY, alignment=PP_ALIGN.CENTER)
    
    add_textbox(slide, 1.5, 5.0, 10.5, 0.6,
                "Methods: Image Negative, Gamma Correction, Log Transform, Contrast Stretching,",
                font_size=14, color=MEDIUM_GRAY, alignment=PP_ALIGN.CENTER)
    add_textbox(slide, 1.5, 5.2, 10.5, 0.6,
                "Histogram Equalization, Intensity Slicing, Bit Plane Slicing", font_size=14, 
                color=MEDIUM_GRAY, alignment=PP_ALIGN.CENTER)
    
    # ==============================
    # SLIDE 2: Overview / Table of Contents
    # ==============================
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, WHITE)
    add_section_header(slide, "Methods Overview")
    
    methods = [
        ("1", "Image Negative", "Pixel value inversion: s = L - 1 - r"),
        ("2", "Gamma Correction", "Power-law transformation: s = c·r^γ"),
        ("3", "Logarithmic Transform", "Logarithmic mapping: s = c·log(1+r)"),
        ("4", "Contrast Stretching", "Linear scaling to full 0-255 range"),
        ("5", "Histogram Equalization", "CDF-based histogram redistribution"),
        ("6", "Intensity Level Slicing", "Isolate and enhance specific intensity ranges"),
        ("7", "Bit Plane Slicing", "Extract individual bit planes (0-7) from image")
    ]
    
    for i, (num, name, desc) in enumerate(methods):
        y = 1.5 + i * 0.8
        # Number circle
        shape = slide.shapes.add_shape(9, Inches(1.5), Inches(y), Inches(0.5), Inches(0.5))  # OVAL
        shape.fill.solid()
        shape.fill.fore_color.rgb = DARK_BLUE
        shape.line.fill.background
        tf = shape.text_frame
        tf.text = num
        tf.paragraphs[0].font.size = Pt(16)
        tf.paragraphs[0].font.bold = True
        tf.paragraphs[0].font.color.rgb = WHITE
        tf.paragraphs[0].alignment = PP_ALIGN.CENTER
        
        # Name and description
        add_textbox(slide, 2.3, y - 0.05, 5, 0.5, name, font_size=16, bold=True, color=DARK_GRAY)
        add_textbox(slide, 2.3, y + 0.45, 8, 0.4, desc, font_size=11, color=MEDIUM_GRAY)
    
    # ==============================
    # SLIDE 3: Method 1 - Image Negative
    # ==============================
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, WHITE)
    add_section_header(slide, "1. Image Negative")
    add_method_title(slide, "Pixel Value Inversion")
    
    # Description on left
    add_textbox(slide, 0.5, 1.7, 6, 4.5,
                "The image negative (or photographic negative) is obtained by subtracting each pixel value\n"
                "from the maximum possible value L-1 (for 8-bit images, L=255).\n\n"
                "Formula: s = 255 - r\n\n"
                "Effect: Bright areas become dark and vice versa. Creates a photographic negative effect.\n\n"
                "Applications:\n"
                "• Medical imaging for examining transparent structures\n"
                "• Document processing and OCR preprocessing\n"
                "• Artistic image effects\n"
                "• Quick visual inspection of image dynamics",
                font_size=12, color=DARK_GRAY)
    
    # Input image
    add_image_with_caption(slide, 7, 1.7, 5.5,
                           os.path.join(image_dir, 'circle_gray.png'),
                           "Input: Grayscale circle image\nOriginal pixel values range from dark center to bright edges")
    
    # Output image
    add_image_with_caption(slide, 7, 4.2, 5.5,
                           os.path.join(image_dir, 'negative_gray.png'),
                           "Output: Negative transformation\ns = 255 - r - bright areas become dark and vice versa")
    
    # Key properties
    add_textbox(slide, 0.5, 6.3, 12, 0.8,
                "Key Property: Complete reversal of intensity ordering. Minimum becomes maximum, maximum becomes minimum.",
                font_size=11, bold=True, color=ACCENT_ORANGE)
    
    # ==============================
    # SLIDE 4: Method 2 - Gamma Correction
    # ==============================
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, WHITE)
    add_section_header(slide, "2. Gamma Encoding / Correction")
    add_method_title(slide, "Power-Law Transformation")
    
    # Description
    add_textbox(slide, 0.5, 1.7, 6, 4.5,
                "Gamma correction applies a power-law function to adjust the luminance of an image.\n\n"
                "Formula: s = 255 · (r/255)^γ\n\n"
                "γ < 1 (e.g., 0.3, 0.5): Brightens the image, expands dark regions\n"
                "γ = 1: No change (linear)\n"
                "γ > 1 (e.g., 2.0, 3.0): Darkens the image, compresses highlights\n\n"
                "Use Cases:\n"
                "• γ < 1: Enhancing dark details in medical/satellite images\n"
                "• γ > 1: Compressing bright skies or overexposed areas\n"
                "• Calibration for display monitors with gamma ~2.2",
                font_size=12, color=DARK_GRAY)
    
    # Show 5 gamma values
    add_textbox(slide, 0.5, 5.5, 6, 1.5,
                "Tested Gamma Values:",
                font_size=14, bold=True, color=DARK_BLUE)
    add_textbox(slide, 0.5, 5.9, 6, 1.0,
                "γ = 0.3: Strong brightening  •  γ = 0.5: Moderate brightening  •  γ = 1.0: No change\n"
                "γ = 2.0: Moderate darkening  •  γ = 3.0: Strong darkening",
                font_size=12, color=MEDIUM_GRAY)
    
    # Input image
    add_image_with_caption(slide, 7, 1.7, 5.5,
                           os.path.join(image_dir, 'gamma_rgb_1.0.png'),
                           "Input: RGB test image (γ = 1.0, no correction)")
    
    # Output samples - show 2 gamma values
    add_image_with_caption(slide, 7, 4.2, 5.5,
                           os.path.join(image_dir, 'gamma_rgb_0.5.png'),
                           "γ = 0.5: Moderate brightening - expands dark details")
    
    add_image_with_caption(slide, 7, 5.4, 5.5,
                           os.path.join(image_dir, 'gamma_rgb_2.0.png'),
                           "γ = 2.0: Moderate darkening - compresses highlights")
    
    # ==============================
    # SLIDE 5: Method 3 - Logarithmic Transformation
    # ==============================
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, WHITE)
    add_section_header(slide, "3. Logarithmic Transformation")
    add_method_title(slide, "Logarithmic Pixel Mapping")
    
    add_textbox(slide, 0.5, 1.7, 6, 4.5,
                "The logarithmic transformation expands pixel values in the dark range while compressing\n"
                "values in the bright range. This is particularly useful for enhancing details in\n"
                "low-intensity images.\n\n"
                "Formula: s = c · log(1 + r)\n\n"
                "Where c is a scaling constant chosen to maximize the output range.\n\n"
                "Key Advantages:\n"
                "• Expands small differences in dark regions\n"
                "• Compresses large differences in bright regions\n"
                "• Enhances visibility of faint details\n"
                "• Useful for astronomy, radiography, low-light photography\n\n"
                "Unlike gamma correction, logarithmic transformation has an infinite dynamic range\n"
                "compression characteristic that mimics human visual response to light.",
                font_size=12, color=DARK_GRAY)
    
    add_image_with_caption(slide, 7, 1.7, 5.5,
                           os.path.join(image_dir, 'log_gray.png'),
                           "Output: Logarithmic transformed grayscale image\nDetails in shadows are enhanced")
    
    add_image_with_caption(slide, 7, 4.2, 5.5,
                           os.path.join(image_dir, 'log_rgb.png'),
                           "Output: Logarithmic transformed RGB image\nColor image with enhanced shadow details")
    
    # ==============================
    # SLIDE 6: Method 4 - Contrast Stretching
    # ==============================
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, WHITE)
    add_section_header(slide, "4. Contrast Stretching")
    add_method_title(slide, "Linear Intensity Scaling")
    
    add_textbox(slide, 0.5, 1.7, 6, 4.5,
                "Contrast stretching (also called normalization) maps the range of pixel intensity\n"
                "values to the full available range (e.g., 0-255 for 8-bit images). This enhances\n"
                "the overall contrast of the image.\n\n"
                "Formula: s = (r - r_min) / (r_max - r_min) · (s_max - s_min) + s_min\n\n"
                "Automatic version uses percentiles (e.g., 2nd and 98th percentile) to determine\n"
                "r_min and r_max, making it robust to outliers.\n\n"
                "Applications:\n"
                "• Enhancing images with washed-out or dark backgrounds\n"
                "• Preparing images for display on monitors\n"
                "• Medical imaging enhancement\n"
                "• Satellite and remote sensing imagery",
                font_size=12, color=DARK_GRAY)
    
    add_image_with_caption(slide, 7, 1.7, 5.5,
                           os.path.join(image_dir, 'contrast_stretched.png'),
                           "Output: Contrast stretched grayscale image\nFull 0-255 range utilized")
    
    # ==============================
    # SLIDE 7: Method 5 - Histogram Equalization
    # ==============================
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, WHITE)
    add_section_header(slide, "5. Histogram Equalization")
    add_method_title(slide, "CDF-Based Intensity Redistribution")
    
    add_textbox(slide, 0.5, 1.7, 6, 4.5,
                "Histogram equalization improves image contrast by redistributing the pixel intensity\n"
                "values so that the resulting histogram is approximately uniform. It uses the Cumulative\n"
                "Distribution Function (CDF) of the original image to map old pixel values to new ones.\n\n"
                "Formula: s_k = T(r_k) = (CDF(r_k) - CDF_min) / (N - CDF_min) · (L - 1)\n\n"
                "Where:\n"
                "• CDF(r_k) = cumulative sum of histogram up to r_k\n"
                "• N = total number of pixels\n"
                "• CDF_min = CDF value at minimum intensity\n"
                "• L = number of intensity levels (256 for 8-bit)\n\n"
                "For color images, the process is applied to the V (value) channel in HSV color space,\n"
                "preserving color while enhancing contrast.\n\n"
                "Note: Over-enhancement can create noise amplification and unnatural appearances.",
                font_size=12, color=DARK_GRAY)
    
    # Before/After histograms
    add_image_with_caption(slide, 7, 1.7, 5.5,
                           os.path.join(image_dir, 'equalized_gray.png'),
                           "Output: Equalized grayscale histogram\nHistogram spread across full range")
    
    add_image_with_caption(slide, 7, 4.2, 5.5,
                           os.path.join(image_dir, 'histograms.png'),
                           "Comparison: Original vs Equalized histograms\nLeft: original concentrated histogram  Right: equalized uniform histogram")
    
    # ==============================
    # SLIDE 8: Method 6 - Intensity Level Slicing
    # ==============================
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, WHITE)
    add_section_header(slide, "6. Intensity Level Slicing")
    add_method_title(slide, "Isolate Specific Intensity Ranges")
    
    add_textbox(slide, 0.5, 1.7, 6, 4.5,
                "Intensity level slicing isolates a specific range of gray levels in an image and\n"
                "either highlights them or darkens the remaining levels. This is useful for revealing\n"
                "features within a particular intensity band.\n\n"
                "Two modes:\n\n"
                "1. HIGHLIGHT mode: Pixels within the selected range are set to maximum brightness (255),\n"
                "   pixels outside are set to background (0).\n\n"
                "2. DARKEN mode: Pixels within the selected range retain their original values,\n"
                "   pixels outside are darkened to background (0).\n\n"
                "Parameters used: width = 20 intensity levels around the median intensity\n\n"
                "Applications:\n"
                "• Highlighting tumors in medical images\n"
                "• Enhancing specific features in satellite imagery\n"
                "• Artistic effects and image segmentation\n"
                "• Inspecting specific gray level bands",
                font_size=12, color=DARK_GRAY)
    
    add_image_with_caption(slide, 7, 1.7, 5.5,
                           os.path.join(image_dir, 'intensity_highlight.png'),
                           "Highlight mode: Isolated intensity range brightened to 255")
    
    add_image_with_caption(slide, 7, 4.2, 5.5,
                           os.path.join(image_dir, 'intensity_darken.png'),
                           "Darken mode: Selected range kept, outside darkened")
    
    # ==============================
    # SLIDE 9: Method 7 - Bit Plane Slicing
    # ==============================
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, WHITE)
    add_section_header(slide, "7. Bit Plane Slicing")
    add_method_title(slide, "Extract Individual Bit Planes")
    
    add_textbox(slide, 0.5, 1.7, 6, 4.5,
                "An 8-bit image can be decomposed into 8 bit planes. Bit plane 0 is the least significant\n"
                "bit (LSB) and bit plane 7 is the most significant bit (MSB).\n\n"
                "Bit Plane Significance:\n\n"
                "• Bit Plane 7 (MSB): Contains the major structural information of the image.\n"
                "  Removing it produces a heavily degraded image. Contains the coarse features.\n\n"
                "• Bit Planes 6-5: Contain important structural details. Image is recognizable but\n"
                "  with reduced contrast.\n\n"
                "• Bit Planes 4-3: Contain finer details. Image becomes sketchy.\n\n"
                "• Bit Planes 2-1: Contain fine details and noise.\n\n"
                "• Bit Plane 0 (LSB): Contains the finest detail and noise. If removed, image appears\n"
                "  almost unchanged - the LSB contributes minimally to overall visual appearance.\n\n"
                "Visual Demonstration:\n"
                "The bit plane slices show how much information each plane contributes to the overall\n"
                "image. Typically, 3-4 MSB planes contain ~90% of the image information.",
                font_size=12, color=DARK_GRAY)
    
    # Show LSB and MSB
    add_image_with_caption(slide, 7, 1.7, 5.5,
                           os.path.join(image_dir, 'bit_plane_0.png'),
                           "Bit Plane 0 (LSB): Least significant bit\nContains fine detail and minor noise")
    
    add_image_with_caption(slide, 7, 4.2, 5.5,
                           os.path.join(image_dir, 'bit_plane_7.png'),
                           "Bit Plane 7 (MSB): Most significant bit\nContains major structural image information")
    
    # ==============================
    # SLIDE 10: Summary
    # ==============================
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, LIGHT_BLUE)
    add_section_header(slide, "Summary")
    
    summary_text = (
        "Digital Image Processing - Elementary Methods Summary\n\n"
        "1. Image Negative (s = 255 - r): Complete reversal of intensity ordering. "
        "Quick visual inspection tool.\n\n"
        "2. Gamma Correction (s = 255·(r/255)^γ): Power-law adjustment. γ < 1 brightens, "
        "γ > 1 darkens. Display monitors typically use γ ≈ 2.2.\n\n"
        "3. Logarithmic Transform (s = c·log(1+r)): Expands dark details, compresses bright. "
        "Mimics human vision. Useful for low-light and scientific imagery.\n\n"
        "4. Contrast Stretching: Maps specified intensity range to full 0-255. Automatic "
        "version uses percentiles for robustness. Enhances overall contrast.\n\n"
        "5. Histogram Equalization: CDF-based redistribution for uniform histogram. "
        "Maximizes contrast. Can amplify noise if overdone.\n\n"
        "6. Intensity Level Slicing: Isolates/highlights or darkens specific intensity ranges. "
        "Useful for feature enhancement and segmentation.\n\n"
        "7. Bit Plane Slicing: Decomposes 8-bit image into 8 bit planes. MSB (7-5) contains "
        "structural info; LSB (0) contains fine detail/noise. Information compression insight.\n\n"
        "All methods properly handle both grayscale and RGB images."
    )
    
    add_textbox(slide, 0.5, 1.5, 12.5, 5.5,
                summary_text, font_size=14, color=RGBColor(0x22, 0x33, 0x44))
    
    # Save presentation
    ppt_path = os.path.join(os.path.dirname(__file__), 'Digital_Image_Processing_Report_Enhanced.pptx')
    prs.save(ppt_path)
    print(f"Enhanced PPT saved to: {ppt_path}")
    
    # Try to open
    try:
        if os.name == 'nt':
            os.startfile(ppt_path)
    except:
        pass


if __name__ == '__main__':
    main()