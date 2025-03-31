from PIL import Image, ImageTk, ImageFilter
from src.utils.consts import Args
from src.utils.open_file import resource_path
import logging
log = logging.getLogger(__name__)

def load_background(image_path):
    blur_radius = int(Args.get("background_blur_radius"))
    log.info(f"Loading background image with path: {resource_path(image_path)}")
    original_image = Image.open(resource_path(image_path))
    blurred_image = original_image.filter(ImageFilter.GaussianBlur(blur_radius))
    blurred_image = blurred_image.transform(blurred_image.size, Image.AFFINE, (1, 0, -100, 0, 1, 0))
    return ImageTk.PhotoImage(blurred_image)

def load_icon(image_path, size):
    icon = Image.open(resource_path(image_path))
    icon = icon.resize(size)
    return ImageTk.PhotoImage(icon)