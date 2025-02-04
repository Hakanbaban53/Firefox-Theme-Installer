from os import path
from customtkinter import CTkImage
from PIL import Image
from tkinter import PhotoImage


class ImageLoader:
    def __init__(self, assets_path):
        self.assets_path = assets_path

    def load_CTK_image(self, icon_name, size):
        """General method to load an image with a specified size."""
        return CTkImage(
            light_image=Image.open(path.join(self.assets_path, icon_name)),
            dark_image=Image.open(path.join(self.assets_path, icon_name)),
            size=size,
        )

    def load_photo_image(self, icon_name, size):
        """General method to load an image."""
        return PhotoImage(file=path.join(self.assets_path, icon_name), height=size[0], width=size[1])
