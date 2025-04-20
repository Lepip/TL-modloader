import tkinter as tk
from tkinter import Canvas, ttk
from src.cleanup.window_manager import configure_window, configure_settings_window
from src.cleanup.closing import close_window
from src.launch import launch_game, open_mods_folder
from src.versions import populate_versions, select_version, update_version, get_version_number
from src.utils.media import load_background, load_icon
import logging

logging.basicConfig(
    filename='app.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='w'
)
log = logging.getLogger(__name__)

def start_button_process(root, version_var):
    from src.utils.consts import Args
    launch_game(version_var)
    if Args.get("close_on_start", 0):
        close_window(root)

def open_settings(root):
    from src.utils.consts import Args
    settings_window = tk.Toplevel(root)

    ttk.Label(settings_window, text="Close the launcher on start:").grid(row=2, column=0, padx=10, pady=10)
    close_on_start_var = tk.IntVar(master=settings_window, value=Args.get("close_on_start", 0))
    close_on_start_check = ttk.Checkbutton(settings_window, variable=close_on_start_var, command=lambda: Args.set("close_on_start", close_on_start_var.get()))  
    close_on_start_check.grid(row=2, column=1, padx=5, pady=2)

    save_button = ttk.Button(settings_window, text="Save", command=lambda: settings_window.destroy())
    save_button.grid(row=5, column=0)
    configure_settings_window(settings_window, root)

def main():
    log.info(f"Starting!")
    root = tk.Tk()
    configure_window(root)
    root.protocol("WM_DELETE_WINDOW", lambda: close_window(root))
    s = ttk.Style()
    s.configure('Main.TFrame', background='#c9d7f0')
    s.configure('Main.TLabel', foreground='black', background='#c9d7f0')
    blurred_image = load_background("media\\background.jpg")
    background_label = tk.Label(root, image=blurred_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    icon_image = load_icon("icon.ico", (128, 128))
    root.iconphoto(False, icon_image)

    # Create a settings button
    buttons_frame = ttk.Frame(root, style="Main.TFrame")
    buttons_frame.pack(side="top", anchor="nw", padx=10, pady=10)
    settings_icon = load_icon("media\\settings.png", (32, 32))
    settings_button = ttk.Button(buttons_frame, image=settings_icon, command=lambda: open_settings(root), style="Main.TButton")
    settings_button.grid(row=0, column=0, padx=5, pady=5)
    frame = ttk.Frame(root, padding="10", style="Main.TFrame")
    frame.pack(padx=100, pady=(380, 20))

    versions_frame = ttk.Frame(frame, style="Main.TFrame")
    versions_frame.grid(row=0, column=0)
    versions = populate_versions()
    selected_version = select_version(versions)
    version_var = tk.StringVar(value=selected_version)

    version_number = get_version_number(selected_version)
    version_label = ttk.Label(versions_frame, text=f"Version: {version_number}", font=("Helvetica", 12, "bold"), style="Main.TLabel")
    version_label.grid(row=0, column=0, sticky="W")

    version_menu = ttk.Combobox(versions_frame, textvariable=version_var)
    version_menu.bind("<<ComboboxSelected>>", lambda _: (
        version_label.config(text=f"Version: {get_version_number(version_var.get())}"), 
        update_version(version_var)))
    version_menu['values'] = versions
    version_menu.grid(row=1, column=0, padx=(0, 5), pady=(0, 0), sticky="W")

    folder_icon = load_icon("media\\folder-icon.png", (30, 30))
    mod_folder_button = tk.Button(versions_frame, image=folder_icon, command=lambda: open_mods_folder(version_var))
    mod_folder_button.grid(row=0, column=1, padx=5)

    start_frame = ttk.Frame(frame, style="Main.TFrame")
    start_frame.grid(row=1, column=0)
    start_button = tk.Button(start_frame, text="START", font=("Helvetica", 14, "bold"), command=lambda: start_button_process(root, version_var))
    start_button.pack(side=tk.TOP, padx=(0, 0), pady=(30, 10))
    root.mainloop()
    log.info("Launcher window closed.")

if __name__ == "__main__":
    main()