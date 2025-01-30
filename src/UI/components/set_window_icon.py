from os import name, path
from PIL import Image, ImageTk

class SetWindowIcon:
    def __init__(self, base_dir):
        self.base_dir = base_dir

    def set_window_icon(self, window):
        """Set the window icon based on the operating system."""
        icon_path = path.join(self.base_dir, "assets", "firefox.ico")
        try:
            if name == "nt":
                window.iconbitmap(icon_path)
            else:
                icon = Image.open(icon_path)
                window.iconphoto(True, ImageTk.PhotoImage(icon))
        except Exception as e:
            print(f"Error setting window icon: {e}")
