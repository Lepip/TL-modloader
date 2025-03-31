
import configparser
import logging
import os
from src.utils.consts import NAME, Args
from src.utils.open_file import resource_path

log = logging.getLogger(__name__)

CONFIG_FILE = resource_path('src\\cleanup\\window_config.ini')

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
    if fixed_window_size:
        root.resizable(False, False)
        root.geometry(fixed_window_size)