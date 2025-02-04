from os import name, path
from PIL import Image, ImageTk

from data.static.global_data import BASE_DIR

class SetWindowIcon:
    def __init__(self):
        pass
    def set_window_icon(self, window):
        """Set the window icon based on the operating system."""
        icon_path = path.join(BASE_DIR, "assets", "firefox.ico")
        try:
            if name == "nt":
                window.iconbitmap(icon_path)
            else:
                icon = Image.open(icon_path)
                window.iconphoto(True, ImageTk.PhotoImage(icon))
        except Exception as e:
            print(f"Error setting window icon: {e}")
