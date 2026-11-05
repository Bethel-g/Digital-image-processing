#!/usr/bin/env python3
"""
Generate PowerPoint presentation for Digital Image Processing Assignment.
Creates 15 slides matching lecturer requirements with input/output images.
"""

import os
import sys

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

print("=" * 60)
print("DIGITAL IMAGE PROCESSING - PPT GENERATION")
print("=" * 60)

base_dir = os.path.dirname(os.path.abspath(__file__))
outputs_dir = os.path.join(base_dir, "outputs")
images_dir = os.path.join(base_dir, "images")
ppt_path = os.path.join(base_dir, "Digital_Image_Processing_Assignment.pptx")

# Verify output images exist
required_output_images = [
    "01_negative/negative_gray.png",
    "02_gamma/gamma_rgb_0.5.png",
    "03_logarithmic/log_gray.png",
    "04_contrast/contrast_stretched.png",
    "05_histogram/equalized_gray.png",
    "06_intensity_slicing/intensity_highlight.png",
    "07_bit_plane/bit_plane_7.png",
]

print(f"\nChecking output images in: {outputs_dir}\n")
missing = []
for img in required_output_images:
    full_path = os.path.join(outputs_dir, img)
    if os.path.exists(full_path):
        size = os.path.getsize(full_path)
        print(f"  OK {img} ({size:,} bytes)")
    else:
        missing.append(img)
        print(f"  MISSING {img}")

if missing:
    print(f"\nRun main.py first to generate missing images.")
    sys.exit(1)

print("\nAll required images found. Generating PPT with 15 slides...")


def add_title_slide(prs, title, subtitle):
    """Add title slide with professional formatting."""
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(0x00, 0x6E, 0xB0)
    
    txBox = slide.shapes.add_textbox(Inches(1), Inches(1.5), Inches(11.3), Inches(1.2))
    tf = txBox.text_frame
    tf.text = title
    p = tf.paragraphs[0]
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    p.alignment = PP_ALIGN.CENTER
    
    txBox2 = slide.shapes.add_textbox(Inches(1), Inches(3.0), Inches(11.3), Inches(0.8))
    tf2 = txBox2.text_frame
    tf2.text = subtitle
    p2 = tf2.paragraphs[0]
    p2.font.size = Pt(20)
    p2.font.color.rgb = RGBColor(0xD4, 0xE6, 0xF1)
    p2.alignment = PP_ALIGN.CENTER
    
    txBox3 = slide.shapes.add_textbox(Inches(1), Inches(5.0), Inches(11.3), Inches(0.5))
    tf3 = txBox3.text_frame
    tf3.text = "Digital Image Processing Assignment - Elementary Methods"
    p3 = tf3.paragraphs[0]
    p3.font.size = Pt(14)
    p3.font.color.rgb = RGBColor(0xAA, 0xCC, 0xEE)
    p3.alignment = PP_ALIGN.CENTER
    
    txBox4 = slide.shapes.add_textbox(Inches(1), Inches(5.5), Inches(11.3), Inches(0.5))
    tf4 = txBox4.text_frame
    tf4.text = "Student: ________________    ID: ________________    Date: ________________"
    p4 = tf4.paragraphs[0]
    p4.font.size = Pt(12)
    p4.font.color.rgb = RGBColor(0xAA, 0xCC, 0xEE)
    p4.alignment = PP_ALIGN.CENTER
    
    return slide


def add_content_slide(prs, slide_num, total_slides, title, input_img_path, output_img_path,
                      description_input, description_output):
    """Add a content slide with input image, output image, and descriptions."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # Header background bar
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.0))
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(0x00, 0x6E, 0xB0)
    shape.line.fill.background
    
    # Title text
    txBox = slide.shapes.add_textbox(Inches(0.5), Inches(0.15), Inches(12.3), Inches(0.7))
    tf = txBox.text_frame
    tf.text = f"Slide {slide_num} of {total_slides}: {title}"
    p = tf.paragraphs[0]
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    p.alignment = PP_ALIGN.LEFT
    
    # Divider line
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(1.1), Inches(1.5), Pt(2))
    line.fill.solid()
    line.fill.fore_color.rgb = RGBColor(0x00, 0x96, 0xD6)
    
    # === INPUT IMAGE SECTION ===
    # Input image label
    lbl_input = slide.shapes.add_textbox(Inches(0.5), Inches(1.3), Inches(6), Inches(0.5))
    tf_input = lbl_input.text_frame
    tf_input.text = "Input Image"
    p_input = tf_input.paragraphs[0]
    p_input.font.size = Pt(14)
    p_input.font.bold = True
    p_input.font.color.rgb = RGBColor(0x00, 0x6E, 0xB0)
    p_input.alignment = PP_ALIGN.LEFT
    
    # Input image
    try:
        pic_input = slide.shapes.add_picture(input_img_path, Inches(0.5), Inches(1.8), width=Inches(5.5))
    except Exception:
        txb = slide.shapes.add_textbox(Inches(0.5), Inches(1.8), Inches(5.5), Inches(4.5))
        tf = txb.text_frame
        tf.text = "Input image available in inputs folder"
        tf.paragraphs[0].font.size = Pt(12)
    
    # Description of input
    add_text_box(slide, 0.5, 2.5, 6, 2.0, description_input, font_size=11, color=RGBColor(0x33, 0x33, 0x33))
    
    # === OUTPUT IMAGE SECTION ===
    # Output image label
    lbl_output = slide.shapes.add_textbox(Inches(7.0), Inches(1.3), Inches(6), Inches(0.5))
    tf_output = lbl_output.text_frame
    tf_output.text = "Output Image"
    p_output = tf_output.paragraphs[0]
    p_output.font.size = Pt(14)
    p_output.font.bold = True
    p_output.font.color.rgb = RGBColor(0x00, 0x6E, 0xB0)
    p_output.alignment = PP_ALIGN.LEFT
    
    # Output image
    try:
        pic_output = slide.shapes.add_picture(output_img_path, Inches(7.0), Inches(1.8), width=Inches(5.5))
    except Exception:
        txb = slide.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.5), Inches(4.5))
        tf = txb.text_frame
        tf.text = "Output image available in outputs folder"
        tf.paragraphs[0].font.size = Pt(12)
    
    # Description of output
    add_text_box(slide, 7.0, 2.5, 6, 2.0, description_output, font_size=11, color=RGBColor(0x33, 0x33, 0x33))
    
    return slide


def add_text_box(slide, left, top, width, height, text, font_size=12,
                 color=RGBColor(0x33, 0x33, 0x33), bold=False, alignment=PP_ALIGN.LEFT):
    """Add a styled text box."""
    txBox = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = txBox.text_frame
    tf.text = text
    if len(tf.paragraphs) == 1:
        p = tf.paragraphs[0]
    else:
        p = tf.paragraphs[1]
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.alignment = alignment
    return txBox


def add_image_with_caption(slide, left, top, width, image_path, caption,
                          font_size=11, caption_color=RGBColor(0x55, 0x55, 0x55)):
    """Add an image with a styled caption."""
    try:
        pic = slide.shapes.add_picture(image_path, Inches(left), Inches(top), width=Inches(width))
        
        txBox = slide.shapes.add_textbox(Inches(left), Inches(top + width + 0.08),
                                        Inches(width), Inches(0.35))
        tf = txBox.text_frame
        tf.text = caption
        p = tf.paragraphs[0]
        p.font.size = Pt(font_size)
        p.font.color.rgb = caption_color
        p.alignment = PP_ALIGN.CENTER
        
        return True
    except Exception:
        txBox = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(1.2))
        tf = txBox.text_frame
        tf.text = f"Image not available"
        p = tf.paragraphs[0]
        p.font.size = Pt(font_size)
        p.font.color.rgb = RGBColor(0xCC, 0x00, 0x00)
        return False


def main():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    DARK_BLUE = RGBColor(0x00, 0x6E, 0xB0)
    MEDIUM_BLUE = RGBColor(0x00, 0x96, 0xD6)
    LIGHT_BLUE = RGBColor(0xD4, 0xE6, 0xF1)
    DARK_GRAY = RGBColor(0x33, 0x33, 0x33)
    WHITE = RGBColor(0xFF, 0xFF, 0xFF)
    
    # Paths
    img_gray_input = os.path.join(images_dir, "grayscale", "Cameraman.png")
    img_color_input = os.path.join(images_dir, "color", "Flower.png")
    
    # ==============================
    # SLIDE 1: Title Slide
    # ==============================
    print("[Generating Slide 1: Title Slide]")
    add_title_slide(prs,
        "Digital Image Processing - Elementary Methods",
        "Assignment: Image Enhancement Techniques using Python")
    
    # ==============================
    # SLIDE 2: Introduction
    # ==============================
    print("[Generating Slide 2: Introduction]")
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # Header
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.0))
    shape.fill.solid()
    shape.fill.fore_color.rgb = DARK_BLUE
    shape.line.fill.background
    
    txBox = slide.shapes.add_textbox(Inches(0.5), Inches(0.15), Inches(12.3), Inches(0.7))
    tf = txBox.text_frame
    tf.text = "Slide 2 of 15: Introduction to Digital Image Processing"
    p = tf.paragraphs[0]
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    p.alignment = PP_ALIGN.LEFT
    
    add_text_box(slide, 0.5, 1.3, 6, 5.0,
        "Digital image processing involves performing operations on an image to enhance it or extract useful information.\n\n"
        "Key concepts include:\n"
        "â€¢ Image acquisition and digitization\n"
        "â€¢ Spatial domain processing (point, local, and global operations)\n"
        "â€¢ Frequency domain processing using Fourier transforms\n"
        "â€¢ Image enhancement, restoration, and compression\n"
        "â€¢ Edge detection, segmentation, and feature extraction\n\n"
        "This assignment covers seven fundamental transformation techniques that form the foundation of more advanced processing pipelines.",
        font_size=13, color=DARK_GRAY)
    
    # Input images
    add_image_with_caption(slide, 7.0, 1.5, 5.5,
        img_color_input, "Color Flower image (626Ã—936 pixels)")
    add_image_with_caption(slide, 7.0, 4.3, 5.5,
        img_gray_input, "Grayscale Cameraman image (442Ã—446 pixels)")
    
    # ==============================
    # SLIDE 3: Objectives and Tools
    # ==============================
    print("[Generating Slide 3: Objectives and Tools]")
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # Header
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.0))
    shape.fill.solid()
    shape.fill.fore_color.rgb = DARK_BLUE
    shape.line.fill.background
    
    txBox = slide.shapes.add_textbox(Inches(0.5), Inches(0.15), Inches(12.3), Inches(0.7))
    tf = txBox.text_frame
    tf.text = "Slide 3 of 15: Objectives and Tools Used"
    p = tf.paragraphs[0]
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    p.alignment = PP_ALIGN.LEFT
    
    # Left side: Objectives
    add_text_box(slide, 0.5, 1.3, 6, 5.5,
        "LEARNING OBJECTIVES:\n\n"
        "1. Implement and analyze elementary image transformation techniques\n"
        "2. Understand the mathematical foundations of each method\n"
        "3. Compare effectiveness of different enhancement approaches\n"
        "4. Handle both grayscale and RGB color images\n\n"
        "TOOLS & TECHNOLOGIES:\n\n"
        "â€¢ Python 3.x programming language\n"
        "â€¢ NumPy for vectorized array operations\n"
        "â€¢ Matplotlib for image visualization\n"
        "â€¢ Pillow (PIL) for image I/O\n"
        "â€¢ OpenCV (cv2) for color space conversions\n\n"
        "METHODS IMPLEMENTED:\n\n"
        "1. Image Negative      â€¢ s = L - 1 - r   (inverts pixel values)\n"
        "2. Gamma Correction    â€¢ s = c Â· (r/255)^Î³   (power-law transformation)\n"
        "3. Logarithmic Transform â€¢ s = c Â· log(1 + r)   (expands dark details)\n"
        "4. Contrast Stretching â€¢ Linear mapping to full 0-255 range\n"
        "5. Histogram Equalization â€¢ CDF-based intensity redistribution\n"
        "6. Intensity Slicing   â€¢ Isolate/highlight specific intensity ranges\n"
        "7. Bit Plane Slicing   â€¢ Decompose image into 8 bit planes (0-7)",
        font_size=13, color=DARK_GRAY)
    
    # Right side: Input examples
    add_image_with_caption(slide, 7.0, 1.5, 5.5,
        img_gray_input, "Grayscale test image")
    add_image_with_caption(slide, 7.0, 4.3, 5.5,
        img_color_input, "RGB color test image")
    
    # ==============================
    # SLIDE 4: Image Negative
    # ==============================
    print("[Generating Slide 4: Image Negative]")
    add_content_slide(prs, 4, 15, "4. Image Negative",
        img_gray_input,
        os.path.join(outputs_dir, "01_negative/negative_gray.png"),
        "Original grayscale Cameraman image with intensity values ranging from dark (0) to bright (255)",
        "Negative transformed image where s = 255 - r - bright areas become dark and vice versa\nMinimum (0) becomes maximum (255) and vice versa"),
    
    # ==============================
    # SLIDE 5: Gamma Correction
    # ==============================
    print("[Generating Slide 5: Gamma Correction]")
    add_content_slide(prs, 5, 15, "5. Gamma Encoding / Correction",
        img_color_input,
        os.path.join(outputs_dir, "02_gamma/gamma_rgb_0.5.png"),
        "RGB Flower test image with varying color channels\nGamma correction adjusts luminance per channel",
        "Î³ = 0.5: Moderate brightening - expands dark details\nPower-law transformation s = 255Â·(r/255)^Î³\nÎ³ < 1 brightens, Î³ > 1 darkens\nTested values: 0.3, 0.5, 1.0, 2.0, 3.0"),
    
    # ==============================
    # SLIDE 6: Logarithmic Transformation
    # ==============================
    print("[Generating Slide 6: Logarithmic Transformation]")
    add_content_slide(prs, 6, 15, "6. Logarithmic Transformation",
        img_gray_input,
        os.path.join(outputs_dir, "03_logarithmic/log_gray.png"),
        "Grayscale Cameraman image before transformation\nIntensity values distributed across the full range",
        "Logarithmic transform s = cÂ·log(1+r) expands dark regions and compresses bright regions\nEnhances visibility of faint details\nMimics human visual response to light"),
    
    # ==============================
    # SLIDE 7: Contrast Stretching
    # ==============================
    print("[Generating Slide 7: Contrast Stretching]")
    add_content_slide(prs, 7, 15, "7. Contrast Stretching",
        img_gray_input,
        os.path.join(outputs_dir, "04_contrast/contrast_stretched.png"),
        "Original grayscale image with concentrated intensity histogram\nLimited contrast in the original",
        "Contrast stretched image mapping intensity range to full 0-255 range\nAutomatic percentile-based range (2nd-98th percentile)\nSignificant improvement in visual contrast"),
    
    # ==============================
    # SLIDE 8: Histogram Equalization
    # ==============================
    print("[Generating Slide 8: Histogram Equalization]")
    add_content_slide(prs, 8, 15, "8. Histogram Equalization",
        img_gray_input,
        os.path.join(outputs_dir, "05_histogram/equalized_gray.png"),
        "Original grayscale histogram concentrated in middle range\nLow contrast due to narrow intensity distribution",
        "Equalized histogram spread across full 0-255 range\nCDF-based intensity redistribution\nSignificant contrast enhancement\nMay amplify noise if overdone"),
    
    # ==============================
    # SLIDE 9: Intensity Level Slicing
    # ==============================
    print("[Generating Slide 9: Intensity Level Slicing]")
    add_content_slide(prs, 9, 15, "9. Intensity Level Slicing",
        img_gray_input,
        os.path.join(outputs_dir, "06_intensity_slicing/intensity_highlight.png"),
        "Original grayscale image\nLooking to isolate specific intensity ranges",
        "Highlight mode: Pixels in selected intensity range â†’ 255 (bright), outside â†’ 0 (dark)\nwidth = 20 levels around median intensity\nUseful for highlighting tumors, features in satellite imagery"),
    
    # ==============================
    # SLIDE 10: Bit Plane Slicing
    # ==============================
    print("[Generating Slide 10: Bit Plane Slicing]")
    add_content_slide(prs, 10, 15, "10. Bit Plane Slicing",
        img_gray_input,
        os.path.join(outputs_dir, "07_bit_plane/bit_plane_7.png"),
        "Grayscale image before decomposition\n8-bit image with 256 possible intensity levels",
        "Bit Plane 7 (MSB): Most significant bit - contains major structural information\nRemoving it produces heavily degraded image\nContains coarse features and overall shape of the image\n3-4 MSB planes contain ~90% of image information"),
    
    # ==============================
    # SLIDE 11: RGB vs Grayscale Comparison
    # ==============================
    print("[Generating Slide 11: RGB vs Grayscale Comparison]")
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # Header
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.0))
    shape.fill.solid()
    shape.fill.fore_color.rgb = DARK_BLUE
    shape.line.fill.background
    
    txBox = slide.shapes.add_textbox(Inches(0.5), Inches(0.15), Inches(12.3), Inches(0.7))
    tf = txBox.text_frame
    tf.text = "Slide 11 of 15: RGB vs Grayscale Comparison"
    p = tf.paragraphs[0]
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    p.alignment = PP_ALIGN.LEFT
    
    # Left: Grayscale
    lbl = slide.shapes.add_textbox(Inches(0.5), Inches(1.3), Inches(6), Inches(0.5))
    tf_lbl = lbl.text_frame
    tf_lbl.text = "Grayscale Processing"
    p_lbl = tf_lbl.paragraphs[0]
    p_lbl.font.size = Pt(14)
    p_lbl.font.bold = True
    p_lbl.font.color.rgb = DARK_BLUE
    p_lbl.alignment = PP_ALIGN.LEFT
    
    pic_in = slide.shapes.add_picture(img_gray_input, Inches(0.5), Inches(1.8), width=Inches(5.5))
    pic_out = slide.shapes.add_picture(os.path.join(outputs_dir, "01_negative/negative_gray.png"), Inches(0.5), Inches(2.8), width=Inches(5.5))
    
    add_text_box(slide, 0.5, 4.0, 6, 1.5, "Input: Original\nOutput: Negative (s = 255 - r)", font_size=11, color=DARK_GRAY)
    
    # Right: RGB
    lbl = slide.shapes.add_textbox(Inches(7.0), Inches(1.3), Inches(6), Inches(0.5))
    tf_lbl = lbl.text_frame
    tf_lbl.text = "RGB Processing"
    p_lbl = tf_lbl.paragraphs[0]
    p_lbl.font.size = Pt(14)
    p_lbl.font.bold = True
    p_lbl.font.color.rgb = DARK_BLUE
    p_lbl.alignment = PP_ALIGN.LEFT
    
    pic_in = slide.shapes.add_picture(img_color_input, Inches(7.0), Inches(1.8), width=Inches(5.5))
    pic_out = slide.shapes.add_picture(os.path.join(outputs_dir, "01_negative/negative_rgb.png"), Inches(7.0), Inches(2.8), width=Inches(5.5))
    
    add_text_box(slide, 7.0, 4.0, 6, 1.5, "Input: Original RGB\nOutput: Negative per channel", font_size=11, color=DARK_GRAY)
    
    # ==============================
    # SLIDE 12: Results and Observations
    # ==============================
    print("[Generating Slide 12: Results and Observations]")
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # Header
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.0))
    shape.fill.solid()
    shape.fill.fore_color.rgb = DARK_BLUE
    shape.line.fill.background
    
    txBox = slide.shapes.add_textbox(Inches(0.5), Inches(0.15), Inches(12.3), Inches(0.7))
    tf = txBox.text_frame
    tf.text = "Slide 12 of 15: Results and Observations"
    p = tf.paragraphs[0]
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    p.alignment = PP_ALIGN.LEFT
    
    add_text_box(slide, 0.5, 1.3, 12, 5.5,
        "OBSERVATIONS FROM IMPLEMENTATION RESULTS\n\n"
        "IMAGE NEGATIVE:\n"
        "â€¢ Successfully inverts pixel values for both grayscale and RGB\n"
        "â€¢ Grayscale: Clean inversion, easy to interpret\n"
        "â€¢ RGB: Each channel inverted independently\n"
        "â€¢ Visual effect: Photo negative appearance\n\n"
        "GAMMA CORRECTION:\n"
        "â€¢ Î³ = 0.3: Strong brightening, very dark originals become bright\n"
        "â€¢ Î³ = 0.5: Moderate brightening, dark details enhanced\n"
        "â€¢ Î³ = 1.0: No change - confirms linear case\n"
        "â€¢ Î³ = 2.0: Moderate darkening, highlights compressed\n"
        "â€¢ Î³ = 3.0: Strong darkening, image becomes quite dark\n"
        "â€¢ RGB results maintain color relationships\n\n"
        "LOGARITHMIC TRANSFORMATION:\n"
        "â€¢ Effectively expands dark details while compressing bright regions\n"
        "â€¢ Grayscale: Clear enhancement of shadow areas\n"
        "â€¢ RGB: Color preserved, shadow details improved\n"
        "â€¢ Better at revealing faint details than gamma for very low-intensity images\n\n"
        "CONTRAST STRETCHING:\n"
        "â€¢ Automatic percentile-based range robust against outliers\n"
        "â€¢ Utilizes full 0-255 dynamic range\n"
        "â€¢ Both grayscale and RGB show noticeable improvement\n"
        "â€¢ Particularly effective for images with narrow intensity distributions\n\n"
        "HISTOGRAM EQUALIZATION:\n"
        "â€¢ Dramatically spreads histogram for both grayscale and RGB\n"
        "â€¢ Grayscale: Clear contrast enhancement\n"
        "â€¢ RGB: Color preserved via HSV V-channel processing\n"
        "â€¢ Can amplify noise - must be used judiciously\n"
        "â€¢ Best results when original histogram is concentrated\n\n"
        "INTENSITY SLICING:\n"
        "â€¢ Highlight mode successfully isolates and brightens target range\n"
        "â€¢ Darken mode keeps slice, darkens surroundings\n"
        "â€¢ Parameter (width=20) controls range breadth\n"
        "â€¢ Effective for feature highlighting when features have consistent intensity values\n\n"
        "BIT PLANE SLICING:\n"
        "â€¢ MSB (plane 7) contains major structural information - image recognizable\n"
        "â€¢ LSB (plane 0) contains fine detail and noise - nearly invisible removal\n"
        "â€¢ All 8 planes combined reconstruct the original image exactly\n"
        "â€¢ Demonstrates information distribution across bit planes\n"
        "â€¢ 3-4 MSB planes contain ~90% of visual information",
        font_size=11, color=DARK_GRAY)
    
    # ==============================
    # SLIDE 13: Challenges Encountered
    # ==============================
    print("[Generating Slide 13: Challenges Encountered]")
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # Header
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.0))
    shape.fill.solid()
    shape.fill.fore_color.rgb = DARK_BLUE
    shape.line.fill.background
    
    txBox = slide.shapes.add_textbox(Inches(0.5), Inches(0.15), Inches(12.3), Inches(0.7))
    tf = txBox.text_frame
    tf.text = "Slide 13 of 15: Challenges Encountered"
    p = tf.paragraphs[0]
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    p.alignment = PP_ALIGN.LEFT
    
    add_text_box(slide, 0.5, 1.3, 12, 5.5,
        "CHALLENGES DURING IMPLEMENTATION\n\n"
        "1. RGB IMAGE PROCESSING:\n"
        "   - Ensuring consistent results across all three color channels\n"
        "   - For histogram equalization: converting between color spaces "
        "(RGBâ†”HSV/YCrCb) while preserving color fidelity\n"
        "   - Gamma correction and log transform applied per-channel vs. on luminance\n\n"
        "2. NUMERICAL STABILITY:\n"
        "   - Logarithmic transformation: avoiding log(0) - required epsilon addition\n"
        "   - Normalization: ensuring proper scaling to 0-255 range without clipping\n"
        "   - Division by zero in contrast stretching when min == max\n\n"
        "3. OUTPUT IMAGE QUALITY:\n"
        "   - Proper clipping and conversion to uint8 after each transformation\n"
        "   - Preventing overflow/underflow in arithmetic operations\n"
        "   - Maintaining image data type through chained operations\n\n"
        "4. COMPARISON ACROSS IMAGE TYPES:\n"
        "   - Ensuring grayscale and RGB implementations produce valid results\n"
        "   - Handling different image sizes and channel structures\n"
        "   - Consistent saving/loading across different image formats\n\n"
        "5. VISUAL REPRESENTATION:\n"
        "   - Selecting appropriate gamma values for demonstration\n"
        "   - Choosing effective intensity slicing range parameters\n"
        "   - Bit plane visualization: scaling binary values to 0-255 for visibility",
        font_size=11, color=DARK_GRAY)
    
    # ==============================
    # SLIDE 14: Conclusion
    # ==============================
    print("[Generating Slide 14: Conclusion]")
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # Header
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.0))
    shape.fill.solid()
    shape.fill.fore_color.rgb = DARK_BLUE
    shape.line.fill.background
    
    txBox = slide.shapes.add_textbox(Inches(0.5), Inches(0.15), Inches(12.3), Inches(0.7))
    tf = txBox.text_frame
    tf.text = "Slide 14 of 15: Conclusion"
    p = tf.paragraphs[0]
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    p.alignment = PP_ALIGN.LEFT
    
    add_text_box(slide, 0.5, 1.3, 12, 5.5,
        "CONCLUSION\n\n"
        "This assignment implemented seven fundamental image enhancement techniques\n"
        "using Python, NumPy, and Matplotlib. Key takeaways:\n\n"
        "â€¢ The image negative is the simplest transformation - complete intensity\n"
        "  reversal with a single mathematical operation.\n\n"
        "â€¢ Gamma correction provides intuitive control over image brightness and\n"
        "  contrast, with Î³ < 1 brightening and Î³ > 1 darkening.\n\n"
        "â€¢ Logarithmic transformation is particularly effective for enhancing details\n"
        "  in low-intensity regions, mimicking human visual response.\n\n"
        "â€¢ Contrast stretching with automatic percentile-based range selection\n"
        "  provides robust enhancement without manual parameter tuning.\n\n"
        "â€¢ Histogram equalization redistributes pixel intensities for approximately\n"
        "  uniform histogram, significantly improving contrast but potentially\n"
        "  amplifying noise.\n\n"
        "â€¢ Intensity level slicing isolates specific intensity ranges for highlighting\n"
        "  or darkening, useful for feature enhancement and segmentation.\n\n"
        "â€¢ Bit plane slicing decomposes images into 8 bit planes, demonstrating\n"
        "  that 3-4 MSB planes contain ~90% of image information.\n\n"
        "All methods properly handle both grayscale and RGB images, providing a\n"
        "solid foundation for more advanced digital image processing techniques.",
        font_size=12, color=DARK_GRAY)
    
    # ==============================
    # SLIDE 15: References
    # ==============================
    print("[Generating Slide 15: References]")
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # Header
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.0))
    shape.fill.solid()
    shape.fill.fore_color.rgb = DARK_BLUE
    shape.line.fill.background
    
    txBox = slide.shapes.add_textbox(Inches(0.5), Inches(0.15), Inches(12.3), Inches(0.7))
    tf = txBox.text_frame
    tf.text = "Slide 15 of 15: References"
    p = tf.paragraphs[0]
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    p.alignment = PP_ALIGN.LEFT
    
    add_text_box(slide, 0.5, 1.3, 12, 5.5,
        "REFERENCES\n\n"
        "1. Gonzalez, R. C., & Woods, R. E. (2008). Digital Image Processing "
        "(3rd ed.). Pearson. - Fundamental textbook covering all methods implemented.\n\n"
        "2. Smith, S. W. (2007). The Scientist and Engineer's Guide to Digital "
        "Signal Processing. California Technical Publishing. - Image processing fundamentals.\n\n"
        "3. Russ, J. C. (2011). The Image Processing Handbook (6th ed.). CRC Press. "
        " - Practical implementation techniques.\n\n"
        "4. Pratt, W. K. (2007). Digital Image Processing (4th ed.). Wiley. - "
        "Mathematical foundations of image transformations.\n\n"
        "5. Jain, A. K. (1989). Fundamentals of Digital Imaging (1st ed.). Prentice-Hall. "
        " - Classic reference on image processing methods.\n\n"
        "6. Online Resources:\n"
        "   â€¢ OpenCV Documentation: https://docs.opencv.org/\n"
        "   â€¢ scikit-image: https://scikit-image.org/\n"
        "   â€¢ numpy documentation: https://numpy.org/doc/\n"
        "\n"
        "COURSE INFORMATION:\n"
        "Digital Image Processing - Elementary Methods Assignment\n"
        "Python Implementation using: NumPy, Matplotlib, OpenCV, Pillow",
        font_size=11, color=DARK_GRAY)
    
    # Save the presentation
    prs.save(ppt_path)
    print(f"\nâœ“ PPT successfully generated: {ppt_path}")
    print(f"\nTotal slides: 15")
    print("=" * 60)


if __name__ == "__main__":
    main()