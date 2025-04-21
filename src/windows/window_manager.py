
import configparser
import logging
import os
from src.utils.consts import NAME, Args
from src.utils.open_file import resource_path
from src.utils.media import load_cropped_background
import tkinter as tk

log = logging.getLogger(__name__)

CONFIG_FILE = resource_path('src\\windows\\window_config.ini')

def get_window_position(window):
    return {
        'left': str(window.left),
        'top': str(window.top),
        'width': str(window.width),
        'height': str(window.height)
    }

def save_window_position(window_position):
    config = configparser.ConfigParser()
    config['WINDOW'] = window_position
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)
    log.info(f"Window position saved: {list(config['WINDOW'].items())}")

def load_window_position():
    if not os.path.exists(CONFIG_FILE):
        log.warning(f"Config file {CONFIG_FILE} does not exist.")
        return None

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    if 'WINDOW' in config:
        log.info(f"Window position loaded: {list(config['WINDOW'].items())}")
        return {
            'left': config.getint('WINDOW', 'left'),
            'top': config.getint('WINDOW', 'top'),
            'width': config.getint('WINDOW', 'width'),
            'height': config.getint('WINDOW', 'height')
        }
    return None

def configure_window(root):
    root.title(NAME)
    root.geometry("400x200")
    fixed_window_size = Args.get('fixed_window_size')
    window_position = load_window_position()
    if window_position:
        root.geometry(f"{window_position['width']}x{window_position['height']}+{window_position['left']}+{window_position['top']}")
        width = window_position['width']
        height = window_position['height']
    if fixed_window_size:
        root.resizable(False, False)
        root.geometry(fixed_window_size)
        width, height = map(int, fixed_window_size.split('x'))
    
    blurred_image = load_cropped_background("media\\background.jpg", 0, 0, width, height)
    background_label = tk.Label(root, image=blurred_image)
    root.blurred_image = blurred_image
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

def configure_settings_window(settings_window, root):
    settings_window.title("Settings")
    settings_window.resizable(False, False)
    root_x = root.winfo_x()
    root_y = root.winfo_y()
    root_width = root.winfo_width()
    root_height = root.winfo_height()
    settings_width = 500
    settings_height = 200
    settings_x = root_x + (root_width // 2) - (settings_width // 2)
    settings_y = root_y + (root_height // 2) - (settings_height // 2)
    settings_window.geometry(f"{settings_width}x{settings_height}+{settings_x}+{settings_y}")
    settings_window.transient(root)

