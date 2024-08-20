import os
import time
import tkinter as tk
from tkinter import messagebox, simpledialog
from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkTextbox, CTkImage, CTkScrollableFrame
from PIL import Image
from io import BytesIO
import webbrowser
import threading
import requests


class ThemeDetailModal(tk.Toplevel):
    def __init__(self, parent, theme, cache_dir):
        super().__init__(parent)
        self.cache_dir = cache_dir
        self.theme = theme
        print(f"Opening theme detail for: {theme}")

        self.cache_expiration = 86400  # Cache expiration in seconds (1 day)
        self.title(f"Theme Details: {self.theme.title}")

        self.configure_modal_window(parent)
        self.create_detail_window(self.theme)
    
    def configure_modal_window(self, parent):
        """Configures the modal window's basic properties."""
        self.transient(parent)
        self.configure(bg="#2B2631")
        self.resizable(False, False)
        self.geometry("700x700")
        self.wait_visibility()
        self.grab_set()

    def create_detail_window(self, theme):
        """Creates and configures the theme detail window."""
        detail_modal_frame = CTkScrollableFrame(self, fg_color="#2B2631")
        detail_modal_frame.pack(fill=tk.BOTH, expand=True)
        detail_modal_frame.columnconfigure(0, weight=1)
        
        self.add_text_widget(detail_modal_frame, theme.description)
        self.add_image_widget(detail_modal_frame, theme)
        self.add_buttons(detail_modal_frame, theme)

    def add_text_widget(self, parent, description):
        """Adds a text widget to display the theme's description."""
        text_frame = CTkFrame(parent)
        text_frame.grid(row=0, column=0, sticky="NSEW")

        text_widget = CTkTextbox(text_frame, font=("Arial", 16), wrap=tk.WORD)
        text_widget.insert(tk.END, description)
        text_widget.configure(state=tk.DISABLED)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def add_image_widget(self, parent, theme):
        """Adds a label for image preview and a loading message."""
        image_frame = CTkFrame(parent)
        image_frame.grid(row=1, column=0, sticky="NSEW")

        loading_label = CTkLabel(image_frame, text="Loading image...")
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
                size=(650, 500),
            )
            image_label.configure(image=image)
            image_label.image = image
            loading_label.pack_forget()
        except (IOError, Exception) as e:
            self.display_image_error(loading_label, error_message=str(e))

    def display_image_error(self, loading_label, error_message="Failed to load image."):
        """Displays an error message if image loading fails."""
        error_label = CTkLabel(loading_label.master, text=error_message)
        error_label.pack(pady=10)
        loading_label.pack_forget()

    def add_buttons(self, parent, theme):
        """Adds the Open Theme Page and Provide Feedback buttons."""
        buttons_frame = CTkFrame(parent, fg_color="#2B2631")
        buttons_frame.grid(row=2, column=0, pady=10)

        link_button = CTkButton(buttons_frame, text="Open Theme Page", command=lambda: webbrowser.open(theme.link))
        link_button.grid(row=0, column=0, padx=10)

        feedback_button = CTkButton(buttons_frame, text="Provide Feedback", command=self.open_feedback_form)
        feedback_button.grid(row=0, column=1, padx=10)

    def open_feedback_form(self):
        """Opens a dialog to collect user feedback."""
        feedback = simpledialog.askstring("Feedback", "Please provide your feedback or report an issue:")
        if feedback:
            messagebox.showinfo("Feedback Received", "Thank you for your feedback!")
