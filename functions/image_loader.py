from os import path
from customtkinter import CTkImage
from PIL import Image
from tkinter import PhotoImage

class ImageLoader:
    def __init__(self, assets_path, os_name):
        self.assets_path = assets_path
        self.os_name = os_name.lower()

    def load_image(self, icon_name, size):
        """General method to load an image with a specified size."""
        return CTkImage(
            light_image=Image.open(path.join(self.assets_path, icon_name)),
            dark_image=Image.open(path.join(self.assets_path, icon_name)),
            size=size,
        )

    def load_attention_icon(self, icons):
        """Load the attention icon."""
        return self.load_image(icons["attention_icon"], (24, 24))

    def load_check_icon(self, icons):
        """Load the check icon."""
        return self.load_image(icons["check_icon"], (24, 24))

    def load_install_files_icon(self, icons):
        """Load the install files icon."""
        return self.load_image(icons["install_files_icon"], (24, 24))

    def load_header_title_bg(self, icons, size=(390, 64)):
        """Load the header title background image with customizable size."""
        return self.load_image(icons["header_title_bg"], size)

    def load_line_top_img(self, icons):
        """Load the line top image."""
        return self.load_image(icons["line_top_img"], (650, 6))
    
    def load_preview_icon(self, icons):
        """Load the preview icon."""
        return self.load_image(icons["preview_icon"], (24, 24))

    def load_os_icon_image(self):
        """Load the OS-specific icon image."""
        return self.load_image(f"icons/{self.os_name}.png", (20, 24))

    def load_select_action_img(self, icons):
        """Load the select action image."""
        return self.load_image(icons["header_title_bg"], (270, 36))

    def load_reload_icon(self, icons):
        """Load the reload icon."""
        return self.load_image(icons["reload_icon"], (24, 24))

    def load_theme_not_selected_icon(self, icons):
        """Load theme not selected icon using PhotoImage."""
        return PhotoImage(
            file=path.join(self.assets_path, icons["theme_not_selected_icon"]),
            height=32,
            width=24,
        )

    def load_theme_selected_icon(self, icons):
        """Load theme selected icon using PhotoImage."""
        return PhotoImage(
            file=path.join(self.assets_path, icons["theme_selected_icon"]),
            height=32,
            width=24,
        )
    
    def load_theme_detected_icon(self, icons):
        """Load the theme detected icon."""
        return self.load_image(icons["theme_detected_icon"], (24, 32))
        # Same icon load_theme_selected_icon but I want to CTKImage instead of PhotoImage.
