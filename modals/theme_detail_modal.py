from os import path, makedirs
from pathlib import Path
from time import time
from tkinter import Toplevel, BOTH, END, DISABLED, X, LEFT
from customtkinter import (
    CTkFrame,
    CTkLabel,
    CTkButton,
    CTkTextbox,
    CTkImage,
    CTkScrollableFrame,
)
from PIL import Image
from io import BytesIO
from webbrowser import open as openweb
from threading import Thread
from requests import get, RequestException

from components.set_window_icon import SetWindowIcon
from installer_core.data_tools.load_json_data import LoadJsonData

class ThemeDetailModal(Toplevel):
    def __init__(self, parent, theme, base_dir):
        super().__init__(parent)
        # Load the UI data from the JSON file
        UI_DATA_PATH = path.join(
            base_dir, "data", "modals", "theme_detail_modal_data.json"
        )
        load_json_data = LoadJsonData()
        self.ui_data = load_json_data.load_json_data(UI_DATA_PATH)

        self.base_dir = base_dir

        self.CACHE_PATH = Path(
            path.expanduser(self.ui_data["ThemeDetailModal"]["CACHE_PATH"])
        )
        self.image_cache_dir = path.join(self.CACHE_PATH, "image_cache")

        self.theme = theme

        self.cache_expiration = self.ui_data["ThemeDetailModal"]["cache_expiration"]

        self.title(
            f"{self.ui_data['ThemeDetailModal']['title_prefix']}{self.theme.title}"
        )
        self.configure_modal_window(parent)
        self.create_detail_window(self.theme)

    def configure_modal_window(self, parent):
        """Configures the modal window's basic properties."""
        self.transient(parent)
        self.configure(bg=self.ui_data["ThemeDetailModal"]["background_color"])
        self.resizable(False, False)
        self.geometry(self.ui_data["ThemeDetailModal"]["window_geometry"])
        self.wait_visibility()
        self.grab_set()
        icon_setter = SetWindowIcon(self.base_dir)
        icon_setter.set_window_icon(self)

    def create_detail_window(self, theme):
        """Creates and configures the theme detail window."""
        detail_modal_frame = CTkFrame(
            self, fg_color=self.ui_data["ThemeDetailModal"]["background_color"]
        )
        detail_modal_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        detail_modal_frame.columnconfigure(0, weight=1)

        self.add_text_widget(detail_modal_frame, theme.description)
        self.add_image_widget(detail_modal_frame, theme)
        self.add_tags_widget(detail_modal_frame, theme.tags)
        self.add_buttons(detail_modal_frame, theme)

    def add_text_widget(self, parent, description):
        """Adds a text widget to display the theme's description."""
        text_frame = CTkFrame(parent)
        text_frame.grid(row=0, column=0, sticky="NSEW", pady=(0, 10))

        text_widget = CTkTextbox(
            text_frame,
            font=tuple(self.ui_data["ThemeDetailModal"]["text_frame"]["font"]),
            height=self.ui_data["ThemeDetailModal"]["text_frame"]["height"],
        )
        text_widget.insert(END, description)
        text_widget.configure(
            state=DISABLED,
            bg_color=self.ui_data["ThemeDetailModal"]["text_frame"]["background_color"],
        )
        text_widget.pack(side=LEFT, fill=BOTH, expand=True)

    def add_image_widget(self, parent, theme):
        """Adds a label for image preview and a loading message."""
        image_frame = CTkFrame(parent, fg_color="#F8F8F8")
        image_frame.grid(row=1, column=0, sticky="NSEW", pady=(0, 10))

        image_label = CTkLabel(
            image_frame,
            text=self.ui_data["ThemeDetailModal"]["loading_image_text"],
            width=self.ui_data["ThemeDetailModal"]["image_size"][0],
            height=self.ui_data["ThemeDetailModal"]["image_size"][1],
        )
        image_label.pack()

        Thread(
            target=self.load_image_in_background, args=(theme, image_label), daemon=True
        ).start()

    def load_image_in_background(self, theme, image_label):
        """Handles image loading in a background thread."""
        image_data = self.load_image(theme)

        if image_data:
            self.display_image(image_label, image_data)
        else:
            self.display_image_error(image_label)

    def sanitize_title(self, title):
        # # Replace any problematic characters with underscores or remove them
        return title.replace('/', '_').replace('\\', '_')

    def load_image(self, theme):
        """Loads the image from cache or downloads it."""
        makedirs(self.image_cache_dir, exist_ok=True)  # Ensure cache directory exists
        sanitized_title = self.sanitize_title(theme.title)
        image_cache_path = path.join(self.image_cache_dir, f"{sanitized_title}.webp")
        current_time = time()

        if (
            path.exists(image_cache_path)
            and (current_time - path.getmtime(image_cache_path)) < self.cache_expiration
        ):
            return self.read_image_from_cache(image_cache_path)
        return self.download_and_cache_image(theme.image, image_cache_path)

    def read_image_from_cache(self, cache_path):
        """Reads image data from the cache."""
        try:
            with open(cache_path, "rb") as f:
                return f.read()
        except IOError as e:
            return None

    def download_and_cache_image(self, url, cache_path):
        """Downloads the image and caches it."""
        image_data = self.download_image(url)
        if image_data:
            try:
                with open(cache_path, "wb") as f:
                    f.write(image_data)
            except IOError as e:
                raise e
        return image_data

    def download_image(self, url):
        """Downloads the image from the URL."""
        try:
            response = get(url, timeout=10)  # Add timeout to prevent hanging
            response.raise_for_status()
            return response.content
        except RequestException as e:
            return None

    def display_image(self, image_label, image_data):
        """Displays the image in the UI."""
        try:
            image = CTkImage(
                light_image=Image.open(BytesIO(image_data)),
                dark_image=Image.open(BytesIO(image_data)),
                size=tuple(self.ui_data["ThemeDetailModal"]["image_size"]),
            )
            image_label.configure(text="", image=image)
            image_label.image = image
        except (IOError, Exception) as e:
            self.display_image_error(image_label, error_message=str(e))

    def display_image_error(self, image_label, error_message=None):
        """Displays an error message if image loading fails."""
        error_message = (
            error_message or self.ui_data["ThemeDetailModal"]["failed_image_text"]
        )
        image_label.configure(text=error_message, image=None)

    def add_tags_widget(self, parent, tags):
        """Adds a section to display tags associated with the theme."""
        tags_frame = CTkFrame(
            parent,
            fg_color=self.ui_data["ThemeDetailModal"]["add_tags_widget"][
                "fg_color"
            ],
        )
        tags_frame.grid(row=2, column=0, sticky="NSEW", pady=(0, 10))

        tags_label = CTkLabel(
            tags_frame, text=self.ui_data["ThemeDetailModal"]["add_tags_widget"]["text"]
        )
        tags_label.pack(anchor="w", padx=10)

        tags_container = CTkScrollableFrame(
            tags_frame,
            height=self.ui_data["ThemeDetailModal"]["add_tags_widget"]["height"],
            fg_color=self.ui_data["ThemeDetailModal"]["background_color"],
            orientation=self.ui_data["ThemeDetailModal"]["add_tags_widget"][
                "orientation"
            ],
        )
        tags_container.pack(fill=X, expand=True, padx=4, pady=(0, 4))

        for tag in tags:
            tag_label = CTkLabel(
                tags_container,
                text=f" #{tag} ",
                fg_color=self.ui_data["ThemeDetailModal"]["add_tags_widget"][
                    "fg_color"
                ],
                corner_radius=self.ui_data["ThemeDetailModal"]["add_tags_widget"][
                    "corner_radius"
                ],
            )
            tag_label.pack(side=LEFT, padx=5, pady=5)

    def add_buttons(self, parent, theme):
        """Adds the Open Theme Page and Provide Feedback buttons."""
        buttons_frame = CTkFrame(
            parent, fg_color=self.ui_data["ThemeDetailModal"]["background_color"]
        )
        buttons_frame.grid(row=3, column=0, pady=10)

        link_button = CTkButton(
            buttons_frame,
            text=self.ui_data["ThemeDetailModal"]["open_theme_page_button"]["text"],
            text_color=self.ui_data["ThemeDetailModal"]["open_theme_page_button"]["text_color"],
            fg_color=self.ui_data["ThemeDetailModal"]["open_theme_page_button"][
                "fg_color"
            ],
            hover_color=self.ui_data["ThemeDetailModal"]["open_theme_page_button"][
                "hover_color"
            ],
            font=eval(
                self.ui_data["ThemeDetailModal"]["open_theme_page_button"]["font"]
            ),
            command=lambda: openweb(theme.link),
        )
        link_button.grid(row=0, column=0, padx=10)
