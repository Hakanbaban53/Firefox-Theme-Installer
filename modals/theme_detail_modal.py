import os
import time
import json
import tkinter as tk
from tkinter import messagebox, simpledialog
from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkTextbox, CTkImage, CTkScrollableFrame
from PIL import Image
from io import BytesIO
import webbrowser
import threading
import requests


class ThemeDetailModal(tk.Toplevel):
    def __init__(self, parent, theme, cache_dir, base_dir):
        super().__init__(parent)
        self.base_dir = base_dir
        self.cache_dir = cache_dir
        self.theme = theme
        print(f"Opening theme detail for: {theme}")

        self.data = self.load_ui_data()  # Load UI data from JSON
        self.cache_expiration = self.data["ThemeDetailModal"]["cache_expiration"]

        self.title(f"{self.data['ThemeDetailModal']['title_prefix']}{self.theme.title}")
        self.configure_modal_window(parent)
        self.create_detail_window(self.theme)
    
    def load_ui_data(self):
        """Load UI configuration data from JSON file."""
        ui_data_path = os.path.join(self.base_dir, "data", "modals","theme_detail_modal_data.json")  # Path to JSON file
        try:
            with open(ui_data_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError("The UI configuration file was not found.")
        except json.JSONDecodeError:
            raise ValueError("Error parsing the UI configuration JSON file.")
        except Exception as e:
            raise Exception(f"An error occurred while loading the UI data file: {e}")

    def configure_modal_window(self, parent):
        """Configures the modal window's basic properties."""
        self.transient(parent)
        self.configure(bg=self.data["ThemeDetailModal"]["background_color"])
        self.resizable(False, False)
        self.geometry(self.data["ThemeDetailModal"]["window_geometry"])
        self.wait_visibility()
        self.grab_set()

    def create_detail_window(self, theme):
        """Creates and configures the theme detail window."""
        detail_modal_frame = CTkScrollableFrame(self, fg_color=self.data["ThemeDetailModal"]["background_color"])
        detail_modal_frame.pack(fill=tk.BOTH, expand=True)
        detail_modal_frame.columnconfigure(0, weight=1)
        
        self.add_text_widget(detail_modal_frame, theme.description)
        self.add_image_widget(detail_modal_frame, theme)
        self.add_buttons(detail_modal_frame, theme)

    def add_text_widget(self, parent, description):
        """Adds a text widget to display the theme's description."""
        text_frame = CTkFrame(parent)
        text_frame.grid(row=0, column=0, sticky="NSEW")

        text_widget = CTkTextbox(
            text_frame,
            font=tuple(self.data["ThemeDetailModal"]["text_frame"]["font"]),
            wrap=getattr(tk, self.data["ThemeDetailModal"]["text_frame"]["wrap"])
        )
        text_widget.insert(tk.END, description)
        text_widget.configure(state=tk.DISABLED)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def add_image_widget(self, parent, theme):
        """Adds a label for image preview and a loading message."""
        image_frame = CTkFrame(parent)
        image_frame.grid(row=1, column=0, sticky="NSEW")

        loading_label = CTkLabel(image_frame, text=self.data["ThemeDetailModal"]["loading_image_text"])
        loading_label.pack()

        image_label = CTkLabel(image_frame, text="")
        image_label.pack()

        threading.Thread(target=self.load_image_in_background, args=(theme, image_label, loading_label), daemon=True).start()

    def load_image_in_background(self, theme, image_label, loading_label):
        """Handles image loading in a background thread."""
        image_data = self.load_image(theme)

        if image_data:
            self.display_image(image_label, loading_label, image_data)
        else:
            self.display_image_error(loading_label)

    def load_image(self, theme):
        """Loads the image from cache or downloads it."""
        os.makedirs(self.cache_dir, exist_ok=True)  # Ensure cache directory exists
        image_cache_path = os.path.join(self.cache_dir, f"{theme.title}.webp")
        current_time = time.time()

        if os.path.exists(image_cache_path) and (current_time - os.path.getmtime(image_cache_path)) < self.cache_expiration:
            return self.read_image_from_cache(image_cache_path)
        return self.download_and_cache_image(theme.image, image_cache_path)

    def read_image_from_cache(self, cache_path):
        """Reads image data from the cache."""
        try:
            with open(cache_path, "rb") as f:
                return f.read()
        except IOError as e:
            print(f"Error reading image from cache: {e}")
            return None

    def download_and_cache_image(self, url, cache_path):
        """Downloads the image and caches it."""
        image_data = self.download_image(url)
        if image_data:
            try:
                with open(cache_path, "wb") as f:
                    f.write(image_data)
            except IOError as e:
                print(f"Error caching image: {e}")
        return image_data

    def download_image(self, url):
        """Downloads the image from the URL."""
        try:
            response = requests.get(url, timeout=10)  # Add timeout to prevent hanging
            response.raise_for_status()
            return response.content
        except requests.RequestException as e:
            print(f"Error downloading image: {e}")
            return None

    def display_image(self, image_label, loading_label, image_data):
        """Displays the image in the UI."""
        try:
            image = CTkImage(
            light_image=Image.open(BytesIO(image_data)),
            dark_image=Image.open(BytesIO(image_data)),
            size=tuple(self.data["ThemeDetailModal"]["image_size"]),
            )
            image_label.configure(image=image)
            image_label.image = image
            loading_label.pack_forget()
        except (IOError, Exception) as e:
            self.display_image_error(loading_label, error_message=str(e))

    def display_image_error(self, loading_label, error_message=None):
        """Displays an error message if image loading fails."""
        error_message = error_message or self.data["ThemeDetailModal"]["failed_image_text"]
        error_label = CTkLabel(loading_label.master, text=error_message)
        error_label.pack(pady=10)
        loading_label.pack_forget()

    def add_buttons(self, parent, theme):
        """Adds the Open Theme Page and Provide Feedback buttons."""
        buttons_frame = CTkFrame(parent, fg_color=self.data["ThemeDetailModal"]["background_color"])
        buttons_frame.grid(row=2, column=0, pady=10)

        link_button = CTkButton(
            buttons_frame,
            text=self.data["ThemeDetailModal"]["buttons"]["open_theme_page"],
            command=lambda: webbrowser.open(theme.link)
        )
        link_button.grid(row=0, column=0, padx=10)

        feedback_button = CTkButton(
            buttons_frame,
            text=self.data["ThemeDetailModal"]["buttons"]["provide_feedback"],
            command=self.open_feedback_form
        )
        feedback_button.grid(row=0, column=1, padx=10)

    def open_feedback_form(self):
        """Opens a dialog to collect user feedback."""
        feedback = simpledialog.askstring(
            self.data["ThemeDetailModal"]["buttons"]["feedback_prompt"],
            self.data["ThemeDetailModal"]["buttons"]["feedback_prompt"]
        )
        if feedback:
            messagebox.showinfo(
                self.data["ThemeDetailModal"]["buttons"]["feedback_received_title"],
                self.data["ThemeDetailModal"]["buttons"]["feedback_received"]
            )
