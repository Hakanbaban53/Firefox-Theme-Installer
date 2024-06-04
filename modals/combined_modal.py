import tkinter as tk
from customtkinter import CTkButton

from json import load

class CombinedModal(tk.Toplevel):
    def __init__(self, parent, modal):
        super().__init__(parent)
        self._configure_window(parent)
        self._load_data()
        self.create_modal(modal)
        self.center_window()

    def _configure_window(self, parent):
        self.transient(parent)
        self.configure(bg="#2B2631")
        self.resizable(False, False)
        self.wait_visibility()
        self.grab_set()
        self.iconbitmap("C:/Users/hakan/Documents/GitHub/RealFire-Installer/assets/icons/firefox.ico")

    def _load_data(self):
        try:
            with open("../RealFire-Installer/data/installer_data.json", "r") as file:
                self.installer_data = load(file)
            self.text_data = self.installer_data.get("common_values", {}).get("modals", {})
        except FileNotFoundError:
            raise FileNotFoundError("The installer data file was not found.")
        

    def create_modal(self, modal):
        modal_mapping = {
            "exit": "exit_modal",
            "attention": "attention_modal",
            "admin_req": "admin_req_modal",
            "check_files_installed": "check_files_installed_modal",
            "check_files_not_installed": "check_files_not_installed_modal",
        }

        modal_key = modal_mapping.get(modal.lower())
        modal_data = self.text_data.get(modal_key)

        # For testing purposes, I will comment out the following lines
        # if modal_key is None:
        #     raise ValueError(f"Unknown modal type: '{modal}'")

        # if modal_data is None:
        #     raise KeyError(f"Modal data not found for key: '{modal_key}'")

        self.title(modal_data["modal_title"])
        self.create_label(modal_data["modal_label"])
        self.create_buttons(modal)

    def create_label(self, text):
        self.message_label = tk.Label(
            self,
            text=text,
            fg="white",
            background="#2B2631",
            font=("Arial", 16),
        )
        self.message_label.pack(padx=10, pady=10)

    def create_buttons(self, modal):
        if modal.lower() == "exit":
            self.create_exit_buttons()
        elif modal.lower() == "attention":
            self.create_attention_exit_button()
        else:
            self.ok_button = self.create_button("Ok", "#10dc60", self.cancel_action)
            self.ok_button.pack(pady=20)

    def create_exit_buttons(self):
        self.ok_button = self.create_button("Yes", "#f04141", self.ok_action)
        self.ok_button.pack(side="left", padx=10, pady=20)

        self.cancel_button = self.create_button("No", "#10dc60", self.cancel_action)
        self.cancel_button.pack(side="right", padx=10, pady=20)

    def create_attention_exit_button(self):
        self.protocol("WM_DELETE_WINDOW", self.ok_action)
        self.ok_button = self.create_button("Ok", "#10dc60", self.ok_action)
        self.ok_button.pack(pady=20)

    def create_button(self, text, fg_color, command):
        return CTkButton(
            self,
            text=text,
            text_color="white",
            command=command,
            bg_color="#2B2631",
            fg_color=fg_color,
            font=("Arial", 18),
        )

    def ok_action(self):
        self.master.quit()
        self.destroy()

    def cancel_action(self):
        self.destroy()

    def center_window(self):
        self.update_idletasks()  # Ensure that window dimensions are updated
        parent_width = self.master.winfo_width()
        parent_height = self.master.winfo_height()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (parent_width - width) // 2
        y = (parent_height - height) // 2
        self.geometry(f"+{self.master.winfo_rootx() + x}+{self.master.winfo_rooty() + y}")
        

