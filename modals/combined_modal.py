import os
import tkinter as tk
from customtkinter import CTkButton
from json import load
from os import path

class CombinedModal(tk.Toplevel):
    def __init__(self, parent, base_dir, modal):
        super().__init__(parent)
        
        self.base_dir = base_dir

        self._configure_window(parent)
        self._load_data()
        self.create_modal(modal)
        self.center_window()

    def _configure_window(self, parent):
        """Configure the modal window properties."""
        self.transient(parent)
        self.configure(bg="#2B2631")
        self.resizable(False, False)
        self.wait_visibility()
        self.grab_set()

        if os.name == "nt":
            icon_path = os.path.join(self.base_dir, "assets", "icons", "firefox.ico")
            self.iconbitmap(icon_path)

    def _load_data(self):
        """Load data from JSON file."""
        try:
            data_file_path = path.join(
                self.base_dir, "data", "installer_data.json"
            )
            with open(data_file_path, "r", encoding="utf-8") as file:
                self.installer_data = load(file)
            self.text_data = self.installer_data.get("common_values", {}).get(
                "modals", {}
            )
        except FileNotFoundError:
            raise FileNotFoundError("The installer data file was not found.")
        except Exception as e:
            raise Exception(f"An error occurred while loading the data file: {e}")

    def create_modal(self, modal):
        """Create the modal based on the type specified."""
        modal_mapping = {
            "exit": "exit_modal",
            "attention": "attention_modal",
            "check_files_installed": "check_files_installed_modal",
            "check_files_not_installed": "check_files_not_installed_modal",
        }

        modal_key = modal_mapping.get(modal.lower())
        if modal_key:
            modal_data = self.text_data.get(modal_key)
            if modal_data:
                self.title(modal_data["modal_title"])
                self.create_label(modal_data["modal_label"])
                self.create_buttons(modal)
            else:
                raise ValueError(f"No data found for the modal type: {modal}")
        else:
            raise ValueError(f"Invalid modal type: {modal}")

    def create_label(self, text):
        """Create a label for the modal."""
        self.message_label = tk.Label(
            self,
            text=text,
            fg="white",
            background="#2B2631",
            font=("Segoe UI", 15),
        )
        self.message_label.pack(padx=10, pady=10)

    def create_buttons(self, modal):
        """Create buttons based on the modal type."""
        if modal.lower() == "exit":
            self.create_exit_buttons()
        elif modal.lower() == "attention":
            self.create_attention_exit_button()
        else:
            self.create_button("Ok", "#10dc60", self.cancel_action).pack(pady=20)

    def create_exit_buttons(self):
        """Create Yes and No buttons for exit modal."""
        self.create_button("Yes", "#f04141", self.ok_action).pack(
            side="left", padx=10, pady=20
        )
        self.create_button("No", "#10dc60", self.cancel_action).pack(
            side="right", padx=10, pady=20
        )

    def create_attention_exit_button(self):
        """Create Ok button for attention modal."""
        self.protocol("WM_DELETE_WINDOW", self.ok_action)
        self.create_button("Ok", "#10dc60", self.ok_action).pack(pady=20)

    def create_button(self, text, fg_color, command):
        """Create a CTkButton with specified text, color, and command."""
        return CTkButton(
            self,
            text=text,
            text_color="white",
            command=command,
            bg_color="#2B2631",
            fg_color=fg_color,
            font=("Segoe UI", 15),
        )

    def ok_action(self):
        """Action to be taken when Ok button is pressed."""
        self.master.quit()
        self.destroy()

    def cancel_action(self):
        """Action to be taken when Cancel button is pressed."""
        self.destroy()

    def center_window(self):
        """Center the modal window on the parent window."""
        self.update_idletasks()  # Ensure that window dimensions are updated
        parent_width = self.master.winfo_width()
        parent_height = self.master.winfo_height()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (parent_width - width) // 2
        y = (parent_height - height) // 2
        self.geometry(
            f"+{self.master.winfo_rootx() + x}+{self.master.winfo_rooty() + y}"
        )
