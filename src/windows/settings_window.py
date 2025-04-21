import tkinter as tk
from tkinter import ttk
from src.windows.window_manager import configure_settings_window
from src.utils.consts import Args

def handle_row_click(event, row, settings):
    print(row)

def open_settings(root):
    from src.utils.consts import Args
    settings_window = tk.Toplevel(root)
    configure_settings_window(settings_window, root)

    settings_frame = ttk.Frame(settings_window)
    settings_frame.grid(row=0, column=0, sticky="nsew")

    # Define settings
    settings = [
        {"description": "Close the launcher on start", "type": "checkbutton", "var": "close_on_start"},
        {"description": "Select a version", "type": "combobox", "var": "version", "values": ["1.21.2", "1.22.0", "1.23.1"]}
    ]
    ttk.Separator(settings_frame, orient="vertical").grid(row=0, column=1, rowspan=2*len(settings), sticky="ns", padx=5)
    # Add settings to the frame
    for i, setting in enumerate(settings):
        ttk.Label(settings_frame, text=setting["description"]).grid(row=2*i, column=0, sticky=tk.W, padx=10, pady=5)
        if setting["type"] == "checkbutton":
            var = tk.IntVar(value=Args.get(setting["var"], 0))
            checkbutton = ttk.Checkbutton(settings_frame, variable=var, command=lambda var=var, key=setting["var"]: toggle_check(var, key), takefocus=False)
            checkbutton.grid(row=2*i, column=2, sticky=tk.W, padx=10, pady=5)
        elif setting["type"] == "combobox":
            var = tk.StringVar(value=Args.get(setting["var"], setting["values"][0]))
            combobox = ttk.Combobox(settings_frame, textvariable=var, values=setting["values"])
            combobox.grid(row=2*i, column=2, sticky=tk.W, padx=10, pady=5)
            combobox.bind("<<ComboboxSelected>>", lambda event, var=var, key=setting["var"]: update_combobox(var, key))
        ttk.Separator(settings_frame, orient="horizontal").grid(row=2*i + 1, column=0, columnspan=3, sticky="ew")

    save_button = ttk.Button(settings_frame, text="Save", command=lambda: settings_window.destroy())
    save_button.grid(row=len(settings) + 2, column=0, columnspan=3, pady=10)

    settings_frame.grid_columnconfigure(0, weight=1)
    settings_frame.grid_rowconfigure(len(settings) + 2, weight=1)

    settings_window.grid_columnconfigure(0, weight=1)
    settings_window.grid_rowconfigure(0, weight=1)

def toggle_check(var, key):
    from src.utils.consts import Args
    Args.set(key, var.get())

def update_combobox(var, key):
    from src.utils.consts import Args
    Args.set(key, var.get())