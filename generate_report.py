#!/usr/bin/env python3
"""
Generate PPT report for Digital Image Processing Elementary Methods.
Creates a PowerPoint presentation with input, output, and analysis for all 7 methods.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
import subprocess


def add_title_slide(prs, title, subtitle):
    """Add a title slide to the presentation."""
    slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(slide_layout)
    title_obj = slide.shapes.title
    subtitle_obj = slide.placeholders[1]
    title_obj.text = title
    subtitle_obj.text = subtitle
    return slide


def add_method_slide(prs, method_name, input_img_path, output_img_paths, descriptions):
    """Add a slide for one image processing method."""
    slide = prs.slides.add_slide(prs.slide_layouts[5])  # Title + content layout
    
    # Title
    title_shape = slide.shapes.title
    title_shape.text = f" {method_name}"
    
    # Place input image
    left = Inches(0.5)
    top = Inches(1.5)
    width = Inches(1.5)
    
    # Input image
    shp_input = slide.shapes.add_picture(input_img_path, left, top, width=width)
    
    # Title for input
    shp_input_title = slide.shapes.add_textbox(Inches(0.5), Inches(3.2), Inches(1.5), Inches(0.5))
    shp_input_title.text = "Input Image"
    shp_input_title.text_frame.paragraphs[0].font.size = Pt(10)
    
    # Output images grid
    n_outputs = len(output_img_paths)
    cols = min(3, n_outputs)
    rows = (n_outputs + cols - 1) // cols
    
    for i, (img_path, desc) in enumerate(zip(output_img_paths, descriptions)):
        col = i % cols
        row = i // cols
        
        left_img = Inches(0.5 + col * 1.7)
        top_img = Inches(1.5 + row * 1.8)
        width_img = Inches(1.65)
        
        try:
            shp = slide.shapes.add_picture(img_path, left_img, top_img, width=width_img)
            
            # Description textbox
            shp_desc = slide.shapes.add_textbox(Inches(0.5 + col * 1.7), Inches(3.0 + row * 1.8), Inches(1.65), Inches(0.6))
            tf = shp_desc.text_frame
            tf.text = desc
            tf.paragraphs[0].font.size = Pt(8)
        except Exception as e:
            # Skip if image doesn't exist
            pass
    
    return slide


def main():
    image_dir = os.path.join(os.path.dirname(__file__), 'images')
    os.makedirs(image_dir, exist_ok=True)
    
    prs = Presentation()
    
    # Set slide dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # ==============================
    # Title Slide
    # ==============================
    add_title_slide(prs, 
        "Digital Image Processing - Elementary Methods",
        "Assignment Implementation: Python Scripts & Results")
    
    # ==============================
    # Method 1: Image Negative
    # ==============================
    add_method_slide(prs, 
        "1. Image Negative",
        os.path.join(image_dir, 'circle_gray.png'),
        [os.path.join(image_dir, 'negative_gray.png')],
        ["Input: Grayscale circle image",
         "Output: Negative transformation s = 255 - r",
         "Bright areas become dark and vice versa"])
    
    # ==============================
    # Method 2: Gamma Encoding / Correction
    # ==============================
    add_method_slide(prs,
        "2. Gamma Encoding / Correction",
        os.path.join(image_dir, 'gamma_rgb_1.0.png'),
        [os.path.join(image_dir, 'gamma_rgb_0.3.png'),
         os.path.join(image_dir, 'gamma_rgb_0.5.png'),
         os.path.join(image_dir, 'gamma_rgb_2.0.png'),
         os.path.join(image_dir, 'gamma_rgb_3.0.png')],
        ["Input: RGB test image",
         "γ = 0.3: Brightening (over-emphasizes highlights)",
         "γ = 0.5: Moderate brightening",
         "γ = 1.0: No change (linear)",
         "γ = 2.0: Darkening (compresses highlights)",
         "γ = 3.0: Strong darkening"])
    
    # ==============================
    # Method 3: Logarithmic Transformation
    # ==============================
    add_method_slide(prs,
        "3. Logarithmic Transformation",
        os.path.join(image_dir, 'log_rgb.png'),
        [os.path.join(image_dir, 'log_gray.png')],
        ["Input: Grayscale circle image",
         "Output: Log transform s = c * log(1 + r)",
         "Expands dark regions, compresses bright regions",
         "Useful for enhancing details in low-intensity images"])
    
    # ==============================
    # Method 4: Contrast Stretching
    # ==============================
    add_method_slide(prs,
        "4. Contrast Stretching",
        os.path.join(image_dir, 'contrast_stretched.png'),
        [os.path.join(image_dir, 'contrast_stretched.png')],
        ["Input: Grayscale circle image",
         "Output: Automatic contrast stretching using percentiles",
         "Maps 2nd to 98th percentile range to full 0-255 range",
         "Enhances overall contrast of the image"])
    
    # ==============================
    # Method 5: Histogram Equalization
    # ==============================
    add_method_slide(prs,
        "5. Histogram Equalization",
        os.path.join(image_dir, 'equalized_rgb.png'),
        [os.path.join(image_dir, 'equalized_gray.png'),
         os.path.join(image_dir, 'histograms.png')],
        ["Input: Grayscale circle image (left) and RGB test (right)",
         "Output: Equalized grayscale histogram",
         "Histograms.png: Original vs Equalized histograms comparison",
         "Equalization spreads the histogram to cover full range",
         "Improves contrast by redistributing pixel intensities"])
    
    # ==============================
    # Method 6: Intensity Level Slicing
    # ==============================
    add_method_slide(prs,
        "6. Intensity Level Slicing",
        os.path.join(image_dir, 'intensity_highlight.png'),
        [os.path.join(image_dir, 'intensity_darken.png')],
        ["Input: Grayscale circle image",
         "Highlight Slice: Isolates and brightens a specific intensity range",
         "Darken Outside: Keeps slice, darkens everything else",
         "Parameters: width=20 around median intensity"])
    
    # ==============================
    # Method 7: Bit Plane Slicing
    # ==============================
    add_method_slide(prs,
        "7. Bit Plane Slicing",
        os.path.join(image_dir, 'bit_plane_7.png'),
        [os.path.join(image_dir, 'bit_plane_0.png')],
        ["Input: Grayscale circle image",
         "Bit Plane 0 (LSB): Least significant bit - contains fine detail/noise",
         "Bit Plane 7 (MSB): Most significant bit - contains major structural information",
         "Higher bit planes (7-5) contain most image information;",
         "Lower bit planes (4-0) contain progressively finer detail"])
    
    # ==============================
    # Summary Slide
    # ==============================
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.title.text = "Summary"
    
    textbox = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(12), Inches(5))
    tf = textbox.text_frame
    tf.text = "Completed Elementary Methods in Digital Image Processing\n\n"
    tf.text += "1. Image Negative: Inverts pixel values (s = L - 1 - r)\n"
    tf.text += "2. Gamma Correction: Power law transformation s = c * r^γ\n"
    tf.text += "3. Logarithmic Transformation: s = c * log(1 + r)\n"
    tf.text += "4. Contrast Stretching: Linear mapping to full range\n"
    tf.text += "5. Histogram Equalization: Redistributes histogram for max contrast\n"
    tf.text += "6. Intensity Level Slicing: Isolates specific intensity ranges\n"
    tf.text += "7. Bit Plane Slicing: Extracts individual bit planes from image\n\n"
    tf.text += "All methods handle both grayscale and RGB images.\n"
    tf.text += f"Output images saved to: {image_dir}"
    
    # Save presentation
    ppt_path = os.path.join(os.path.dirname(__file__), 'Digital_Image_Processing_Report.pptx')
    prs.save(ppt_path)
    print(f"PPT report saved to: {ppt_path}")
    
    # Try to open the PPT
    try:
        if os.name == 'nt':
            os.startfile(ppt_path)
    except:
        pass


if __name__ == '__main__':
    main()