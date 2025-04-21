import tkinter as tk
from tkinter import ttk
from src.windows.settings_window import open_settings
from src.windows.window_manager import configure_window
from src.cleanup.closing import close_window
from src.launch import launch_game, open_mods_folder
from src.versions import populate_versions, select_version, update_version, get_version_number
from src.utils.media import load_icon
import logging
from src.cleanup.transparency import make_transparent, update_transparency
from src.widgets.listbox import CustomListbox
from src.utils.modloader import ModManager
from src.utils import TkVariables

log = logging.getLogger(__name__)

def start_button_process(root, version_var, mod_list):
    from src.utils.consts import Args
    launch_game(version_var, mod_list)
    if Args.get("close_on_start", 0):
        close_window(root)

def configure_styles():
    s = ttk.Style()
    s.configure('Main.TFrame', background='#c9d7f0')
    s.configure('Main.TLabel', foreground='black', background='#c9d7f0')

def left_frame(root):
    left_frame = ttk.Frame(root, style="Main.TFrame")
    left_frame.grid(row=0, column=0, sticky="nsew", rowspan=2, padx=10, pady=10)
    make_transparent(left_frame)
    buttons_frame = ttk.Frame(left_frame, style="Main.TFrame")
    buttons_frame.grid(row=0, column=0, sticky="nsew")
    make_transparent(buttons_frame)
    settings_icon = load_icon("media\\settings.png", (32, 32))
    settings_button = ttk.Button(buttons_frame, image=settings_icon, command=lambda: open_settings(root), style="Main.TButton", takefocus=False)
    settings_button.pack(fill='x', padx=5, pady=5)
    #button2 = tk.Button(buttons_frame, text="Button 2")
    #button2.pack(fill='x', padx=5, pady=5)

    #button3 = tk.Button(buttons_frame, text="Button 3")
    #button3.pack(fill='x', padx=5, pady=5)

def center_bottom_frame(root):
    center_bottom_frame = ttk.Frame(root, style="Main.TFrame")
    center_bottom_frame.grid(row=1, column=0, sticky="nsew")
    make_transparent(center_bottom_frame)

    menu_frame = ttk.Frame(center_bottom_frame, style="Main.TFrame")
    menu_frame.place(relx=0.5, rely=0.5, anchor="center", width=280, height=200)

    menu_frame.grid_columnconfigure(0, weight=1)
    menu_frame.grid_rowconfigure(0, weight=1)
    menu_frame.grid_rowconfigure(1, weight=1)

    versions_frame = ttk.Frame(menu_frame, style="Main.TFrame")
    versions_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    versions_frame.grid_columnconfigure(0, weight=2)
    versions_frame.grid_columnconfigure(1, weight=1)
    versions_frame.grid_rowconfigure(0, weight=1)
    versions_frame.grid_rowconfigure(1, weight=1)

    versions = populate_versions()
    selected_version = select_version(versions)
    version_var = tk.StringVar(value=selected_version)
    TkVariables.version_var = version_var
    

    version_number = get_version_number(selected_version)
    version_label = ttk.Label(versions_frame, text=f"Version: {version_number}", font=("Helvetica", 11, "bold"), style="Main.TLabel")
    version_label.grid(row=0, column=0, sticky="nsew")

    version_menu = ttk.Combobox(versions_frame, textvariable=version_var)
    version_menu.bind("<<ComboboxSelected>>", lambda _: (
        version_label.config(text=f"Version: {get_version_number(version_var.get())}"),
        update_mods_list(version_var.get()),
        update_version(version_var.get())))
    version_menu['values'] = versions
    version_menu.grid(row=1, column=0, sticky="nsew")

    folder_icon = load_icon("media\\folder-icon.png", (30, 30))
    mod_folder_button = tk.Button(versions_frame, image=folder_icon, command=lambda: open_mods_folder(version_var))
    mod_folder_button.grid(row=0, column=1, rowspan=2, padx=10, pady=10)

    start_frame = ttk.Frame(menu_frame, style="Main.TFrame")
    start_frame.grid(row=1, column=0, sticky="nsew")

    start_button = tk.Button(start_frame, text="START", font=("Helvetica", 14, "bold"), command=lambda: start_button_process(root, version_var, TkVariables.mods_listbox.get_selected_items()), takefocus=False)
    start_button.pack(side=tk.TOP, padx=(0, 0), pady=(30, 10))

def update_mods_list(version):
    mods_list = ModManager.list_mods(version)
    TkVariables.mods_listbox.update_list(mods_list)

def right_frame(root):
    right_frame = ttk.Frame(root, style="Main.TFrame")
    right_frame.grid(row=0, column=1, sticky="nsew", rowspan=2, padx=10, pady=10)
    make_transparent(right_frame)

    mod_list_frame = ttk.Frame(right_frame, style="Main.TFrame")
    mod_list_frame.place(relx=0.5, rely=0.5, anchor="center")
    mods_label = ttk.Label(mod_list_frame, text="Mods", font=("Helvetica", 14, "bold"), style="Main.TLabel")
    mods_label.pack(pady=(10, 0))
    mods_list = ModManager.list_mods(TkVariables.version_var.get())
    mods_listbox = CustomListbox(mod_list_frame, mods_list)
    mods_listbox.pack(fill="both", padx=10, pady=10)
    TkVariables.mods_listbox = mods_listbox

def configure_main_scene(root):
    configure_window(root)
    root.protocol("WM_DELETE_WINDOW", lambda: close_window(root))
    configure_styles()

    icon_image = load_icon("icon.ico", (128, 128))
    root.iconphoto(False, icon_image)

    root.grid_columnconfigure(0, weight=2)
    root.grid_columnconfigure(1, weight=3)
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)

    left_frame(root)
    center_bottom_frame(root)
    right_frame(root)
    
    update_transparency()