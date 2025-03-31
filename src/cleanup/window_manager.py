
import configparser
import logging
import os
from src.utils.consts import NAME

CONFIG_FILE = 'src/cleanup/window_config.ini'

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
    logging.info(f"Window position saved: {list(config['WINDOW'].items())}")

def load_window_position():
    if not os.path.exists(CONFIG_FILE):
        logging.warning(f"Config file {CONFIG_FILE} does not exist.")
        return None

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    if 'WINDOW' in config:
        logging.info(f"Window position loaded: {list(config['WINDOW'].items())}")
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
    window_position = load_window_position()
    if window_position:
        root.geometry(f"{window_position['width']}x{window_position['height']}+{window_position['left']}+{window_position['top']}")