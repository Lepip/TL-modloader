import os
import subprocess
import threading
import time
import tkinter as tk
from tkinter import ttk
from settings import Args, SettingsEditor
from modloader import ModManager
import configparser
import pygetwindow as gw
import os
import logging

logging.basicConfig(
    filename='app.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='w'
)

CONFIG_FILE = 'window_config.ini'

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
    logging.info(f"Window position saved: {config['WINDOW']}")

def load_window_position():
    if not os.path.exists(CONFIG_FILE):
        logging.warning(f"Config file {CONFIG_FILE} does not exist.")
        return None

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    if 'WINDOW' in config:
        logging.info(f"Window position loaded: {config['WINDOW']}")
        return {
            'left': config.getint('WINDOW', 'left'),
            'top': config.getint('WINDOW', 'top'),
            'width': config.getint('WINDOW', 'width'),
            'height': config.getint('WINDOW', 'height')
        }
    return None

def populate_versions():
    versions_path = Args.get("versions_path")
    files = [f for f in os.listdir(versions_path)]
    return files

def restore(delay):
    logging.info(f"Waiting for {delay} seconds before restoring settings.")
    time.sleep(delay)
    logging.info("Reverting settings after delay.")
    SettingsEditor.restore()

def launch_game(root, version_var):
    version_var = version_var.get()
    logging.info(f"Launching...")
    SettingsEditor.set_version(version_var)
    logging.info(f"Version set to: {version_var}")
    SettingsEditor.modify_settings()
    logging.info("Settings modified for game launch")

    modpack_folder = Args.get("modpacks_path") + "\\" + version_var
    mods_folder = Args.get("mods_path")
    logging.info(f"Loading mods from: {modpack_folder} to {mods_folder}")
    ModManager.load_mods(modpack_folder, mods_folder)

    exe_path = Args.get("exe_path")
    subprocess.Popen(exe_path)
    logging.info(f"Game launched with executable: {exe_path}")

    delay = 30
    revert_thread = threading.Thread(target=restore, args=(delay,))
    revert_thread.start()

    on_closing(root)

NAME = "LMC Launcher"

window_position = None

def on_closing(root):
    global window_position
    window_position = get_window_position(gw.getWindowsWithTitle(NAME)[0])
    root.destroy()

def main():
    last_position = load_window_position()
    root = tk.Tk()
    root.title(NAME)
    root.geometry("400x200")
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))
    if last_position:
        root.geometry(f"{last_position['width']}x{last_position['height']}+{last_position['left']}+{last_position['top']}")

    versions = populate_versions()
    version_var = tk.StringVar(value=versions[0] if versions else "")
    version_menu = ttk.Combobox(root, textvariable=version_var)
    version_menu['values'] = versions
    version_menu.pack(pady=10)

    launch_button = tk.Button(root, text="Launch Minecraft", command=lambda: launch_game(root, version_var))
    launch_button.pack(pady=10)

    root.mainloop()
    logging.info("Launcher window closed, saving window position")
    if window_position is not None:
        save_window_position(window_position)
    else:
        windows = gw.getWindowsWithTitle(NAME)
        if windows:
            window = windows[0]
            save_window_position(get_window_position(window))
        else:
            logging.warning("Window not found, position not saved.")

if __name__ == "__main__":
    main()