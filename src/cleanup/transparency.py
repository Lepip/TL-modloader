from src.utils.media import load_cropped_background
import tkinter as tk
frames = []

def make_transparent(frame):
    global frames
    transparent_label = tk.Label(frame, borderwidth=0)
    frame.transparent_label = transparent_label
    frames.append(frame)

def update_transparency():

    global frames
    for frame in frames:
        frame.update_idletasks()
        x = frame.winfo_x()
        y = frame.winfo_y()
        width = frame.winfo_width()
        height = frame.winfo_height()
        cropped_image = load_cropped_background("media\\background.jpg", x, y, width, height)
        frame.transparent_label.configure(image=cropped_image)
        frame.transparent_label.image = cropped_image
        frame.transparent_label.place(x=0, y=0, relwidth=1, relheight=1)