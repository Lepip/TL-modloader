import logging
import subprocess
import threading
import time
import os
from src.utils.consts import Args
from src.settings import SettingsEditor
from src.utils.modloader import ModManager
from src.cleanup.closing import close_window
from src.utils.open_file import resource_path
log = logging.getLogger(__name__)

def restore(delay):
    log.info(f"Waiting for {delay} seconds before restoring settings.")
    time.sleep(delay)
    log.info("Reverting settings after delay.")
    SettingsEditor.restore()

def launch_game(version_var):
    version_var = version_var.get()
    log.info(f"Launching...")
    SettingsEditor.set_version(version_var)
    log.info(f"Version set to: {version_var}")
    SettingsEditor.modify_settings()
    log.info("Settings modified for game launch")

    modpack_folder = Args.get("modpacks_path") + "\\" + version_var
    mods_folder = Args.get("mods_path")
    log.info(f"Loading mods from: {modpack_folder} to {mods_folder}")
    ModManager.load_mods(modpack_folder, mods_folder)

    exe_path = Args.get("exe_path")
    subprocess.Popen(resource_path(exe_path))
    log.info(f"Game launched with executable: {exe_path}")

    delay = 30
    revert_thread = threading.Thread(target=restore, args=(delay,))
    revert_thread.start()

def open_mods_folder(version_var):
    version_var = version_var.get()
    log.info(f"Opening mods folder for version: {version_var}")
    modpack_folder = Args.get("modpacks_path") + "\\" + version_var
    if not os.path.exists(modpack_folder):
        os.makedirs(modpack_folder)
    os.startfile(modpack_folder)
