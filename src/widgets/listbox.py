import tkinter as tk
from tkinter import ttk
from src.utils.media import load_icon

class CustomListbox(tk.Frame):
    def __init__(self, parent, text_rows):
        super().__init__(parent)
        self.text_rows = text_rows

        self.checked_icon = load_icon("media\\checkamark.png", (20, 20))
        self.unchecked_icon = load_icon("media\\no.png", (20, 20))

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
        
        self._widgets = self.create_widgets()
        self.update_scrollbar()
        self.update_idletasks()

    def on_canvas_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.update_scrollbar()

    def on_mouse_wheel(self, event):
        if self.scrollbar.grid_info():
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def update_scrollbar(self):
        content_height = self.list_frame.winfo_reqheight()
        canvas_height = self.canvas.winfo_height()
        if content_height <= canvas_height:
            self.scrollbar.grid_remove()
        else:
            self.scrollbar.grid()

    def on_click(self, index, text):
        if self._widgets[index][1].checked:
            self._widgets[index][1].config(image=self.unchecked_icon)
        else:
            self._widgets[index][1].config(image=self.checked_icon)
        self._widgets[index][1].checked = not self._widgets[index][1].checked

    def create_widgets(self):
        widgets = []
        for i, text in enumerate(self.text_rows):
            row_frame = tk.Frame(self.list_frame, borderwidth=0, highlightthickness=0)
            row_frame.pack(fill="x", pady=5, padx=0)
            label = tk.Label(row_frame, text=text)
            label.pack(side="left")

            button = tk.Button(row_frame, image=self.checked_icon, command=lambda i=i, text=text: self.on_click(i, text))
            button.pack(side="right")
            button.checked = True
            separator = ttk.Separator(self.list_frame, orient="horizontal")
            separator.pack(fill="x", padx=0)
            widgets.append((label, button))
        return widgets

    def update_list(self, new_text_rows):
        self.text_rows = new_text_rows
        for widget in self.list_frame.winfo_children():
            widget.destroy()
        self._widgets = self.create_widgets()
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.update_scrollbar()

    def get_selected_items(self):
        selected = []
        for i, (label, button) in enumerate(self._widgets):
            if button.checked:
                selected.append(label.cget('text'))
        return selected