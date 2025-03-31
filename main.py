import tkinter as tk
from tkinter import Canvas, ttk
from src.cleanup.window_manager import configure_window
from src.cleanup.closing import close_window
from src.launch import launch_game, open_mods_folder
from src.versions import populate_versions, select_version, update_version
from src.utils.media import load_background, load_icon
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
    s = ttk.Style()
    s.configure('Main.TFrame', background='#c9d7f0')

    blurred_image = load_background("media\\background.jpg")
    background_label = tk.Label(root, image=blurred_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    frame = ttk.Frame(root, padding="10", style="Main.TFrame")
    frame.pack(padx=100, pady=(380, 20))

    versions_frame = ttk.Frame(frame, style="Main.TFrame")
    versions_frame.grid(row=0, column=0)
    versions = populate_versions()
    selected_version = select_version(versions)
    version_var = tk.StringVar(value=selected_version)

    version_menu = ttk.Combobox(versions_frame, textvariable=version_var)

    version_menu.bind("<<ComboboxSelected>>", lambda _: update_version(version_var))
    version_menu['values'] = versions
    version_menu.grid(row=0, column=0, padx=(5, 5), pady=(15, 0))

    folder_icon = load_icon("media\\folder-icon.png", (30, 30))
    mod_folder_button = tk.Button(versions_frame, image=folder_icon, command=lambda: open_mods_folder(version_var))
    mod_folder_button.grid(row=0, column=1, padx=5)

    start_frame = ttk.Frame(frame, style="Main.TFrame")
    start_frame.grid(row=1, column=0)
    start_button = tk.Button(start_frame, text="START", font=("Helvetica", 14, "bold"), command=lambda: launch_game(root, version_var))
    start_button.pack(side=tk.TOP, padx=(0, 0), pady=(30, 10))
    root.mainloop()
    log.info("Launcher window closed.")

if __name__ == "__main__":
    main()