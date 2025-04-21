from PIL import Image, ImageTk, ImageFilter
from src.utils.consts import Args
from src.utils.open_file import resource_path
from src.utils import Save
import logging
log = logging.getLogger(__name__)

cached_images = {}

def load_cropped_background(image_path, x, y, width, height):
    if image_path in cached_images:
        blurred_image = cached_images[image_path]
    else:
        blur_radius = int(Args.get("background_blur_radius"))
        log.info(f"Loading background image with path: {resource_path(image_path)}")
        original_image = Image.open(resource_path(image_path))
        blurred_image = original_image.filter(ImageFilter.GaussianBlur(blur_radius))
        back_x, back_y = map(int, Args.get("background_pos").split("x"))
        blurred_image = blurred_image.transform(blurred_image.size, Image.AFFINE, (1, 0, back_x, 0, 1, back_y))
        cached_images[image_path] = blurred_image
    blurred_image = blurred_image.crop((x, y, x + width, y + height))
    return ImageTk.PhotoImage(blurred_image)

def load_icon(image_path, size):
    icon = Image.open(resource_path(image_path))
    icon = icon.resize(size)
    return Save(ImageTk.PhotoImage(icon))