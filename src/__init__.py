# Digital Image Processing - Elementary Methods
from .image_negative import image_negative
from .gamma_correction import gamma_correction
from .logarithmic import logarithmic_transformation
from .contrast_stretching import contrast_stretching
from .histogram_equalization import histogram_equalization
from .intensity_slicing import intensity_level_slicing
from .bit_plane_slicing import bit_plane_slicing


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


def save_image(arr, path, mode=None):
    """Save a numpy array as an image file."""
    from PIL import Image
    if mode is None:
        mode = "RGB" if arr.ndim == 3 and arr.shape[2] == 3 else "L"
    img = Image.fromarray(arr, mode=mode)
    img.save(path)


def display_images(images, titles, rows=2, cols=3, figsize=(12, 8)):
    """Display multiple images in a grid."""
    import matplotlib.pyplot as plt

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


__all__ = [
    "image_negative",
    "gamma_correction",
    "logarithmic_transformation",
    "contrast_stretching",
    "histogram_equalization",
    "intensity_level_slicing",
    "bit_plane_slicing",
    "load_image",
    "save_image",
    "display_images",
]