import logging
import subprocess
import threading
import time
from src.utils.consts import Args
from src.settings import SettingsEditor
from src.utils.modloader import ModManager
from src.cleanup.closing import close_window

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

    close_window(root)