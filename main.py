import tkinter as tk
from src.windows.main_window import configure_main_scene
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
    configure_main_scene(root)
    root.mainloop()
    log.info("Launcher window closed.")

if __name__ == "__main__":
    main()