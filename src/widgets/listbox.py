import tkinter as tk
from tkinter import ttk

class CustomListbox(tk.Frame):
    def __init__(self, parent, text_rows, on_click):
        super().__init__(parent)
        self.text_rows = text_rows
        self.on_click = on_click

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.canvas = tk.Canvas(self)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', self.on_canvas_configure)

        self.list_frame = tk.Frame(self.canvas, borderwidth=0, highlightthickness=0)
        self.list_window = self.canvas.create_window((0, 0), window=self.list_frame, anchor="nw", width=380)

        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)
        self.list_frame.bind("<MouseWheel>", self.on_mouse_wheel)

        self.create_widgets()

    def on_canvas_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_mouse_wheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def create_widgets(self):
        for i, text in enumerate(self.text_rows):
            row_frame = tk.Frame(self.list_frame, borderwidth=0, highlightthickness=0)
            row_frame.pack(fill="x", pady=5, padx=0)

            label = tk.Label(row_frame, text=text)
            label.pack(side="left")

            button = tk.Button(row_frame, text="B", command=lambda i=i, text=text: self.on_click(i, text))
            button.pack(side="right")
            button2 = tk.Button(row_frame, text="B2", command=lambda i=i, text=text: self.on_click(i, text + "2"))
            button2.pack(side="right")
            separator = ttk.Separator(self.list_frame, orient="horizontal")
            separator.pack(fill="x", padx=0)

    def update_list(self, new_text_rows):
        self.text_rows = new_text_rows
        for widget in self.list_frame.winfo_children():
            widget.destroy()
        self.create_widgets()