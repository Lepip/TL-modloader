from src.cleanup.window_manager import get_window_position, save_window_position
import pygetwindow as gw
import logging
from src.utils.consts import NAME


def cleanup(root):
    windows = gw.getWindowsWithTitle(NAME)
    if not windows:
        logging.warning(f"No windows found named {NAME}.")
        return
    window_position = get_window_position(windows[0])
    save_window_position(window_position)
    logging.info("Window position saved.")

def close_window(root):
    cleanup(root)
    root.destroy()