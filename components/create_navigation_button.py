from os import path
from PIL import Image
from customtkinter import CTkButton, CTkImage

from installer_core.data_tools.load_json_data import LoadJsonData

class NavigationButton:
    def __init__(self, base_dir, app_language):
        load_json_data = LoadJsonData()
        NAVIGATION_BUTTON_DATA_PATH = path.join(
            base_dir, "data", "components", "navigation_buttons", "data.json"
        )
        self.navigation_button_data = load_json_data.load_json_data(
            NAVIGATION_BUTTON_DATA_PATH
        )
        self.base_dir = base_dir
        NAVIGATION_BUTTON_TEXT = path.join(
            base_dir, "language", "components", "navigation_buttons", f"{app_language}.json"
        )
        self.navigation_button_text = load_json_data.load_json_data(
            NAVIGATION_BUTTON_TEXT
        )

    def create_navigation_button(
        self,
        parent,
        text,
        image_path,
        command,
        padding_x,
        side,
        img_side="left",
        **kwargs,
    ):
        button_image = CTkImage(light_image=Image.open(image_path), dark_image=Image.open(image_path), size=(20, 20)) if image_path else None

        button = CTkButton(
            parent,
            width=float(self.navigation_button_data["width"]),
            height=float(self.navigation_button_data["height"]),
            corner_radius=float(self.navigation_button_data["corner_radius"]),
            bg_color=self.navigation_button_data["bg_color"],
            fg_color=self.navigation_button_data["fg_color"],
            hover_color=self.navigation_button_data["hover_color"],
            text_color=self.navigation_button_data["text_color"],
            font=(self.navigation_button_data["font_family"], int(self.navigation_button_data["font_size"])),
            image=button_image,
            text=self.navigation_button_text[text] if text in self.navigation_button_text else text,
            compound=img_side,
            command=command,
            **kwargs,
        )
        button.pack(padx=padding_x, pady=10, side=side)
        return button