import tkinter as tk
from tkinter import ttk
from src.cleanup.window_manager import configure_window
from src.cleanup.closing import close_window
from src.launch import launch_game
from src.versions import populate_versions
import logging

logging.basicConfig(
    filename='app.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='w'
)
log = logging.getLogger(__name__)

def main():
    log.info(f"Starting!")
    root = tk.Tk()
    configure_window(root)
    root.protocol("WM_DELETE_WINDOW", lambda: close_window(root))

    versions = populate_versions()
    version_var = tk.StringVar(value=versions[0] if versions else "")
    version_menu = ttk.Combobox(root, textvariable=version_var)
    version_menu['values'] = versions
    version_menu.pack(pady=10)

    launch_button = tk.Button(root, text="Launch Minecraft", command=lambda: launch_game(root, version_var))
    launch_button.pack(pady=10)

    root.mainloop()
    log.info("Launcher window closed.")

if __name__ == "__main__":
    main()