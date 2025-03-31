from src.cleanup.window_manager import get_window_position, save_window_position
import logging
from src.utils.consts import NAME, Args
log = logging.getLogger(__name__)

def cleanup(root):
    window_position = {
        'left': root.winfo_x(),
        'top': root.winfo_y(),
        'width': root.winfo_width(),
        'height': root.winfo_height()
    }
    save_window_position(window_position)
    Args.save()
    log.info("Window position saved.")

def close_window(root):
    cleanup(root)
    root.destroy()