import json
import tkinter as tk
import customtkinter


class CombinedModal(tk.Toplevel):
    def __init__(self, parent, modal):
        super().__init__(parent)
        self.configure(bg="#2B2631")
        self.resizable(False, False)
        self.wait_visibility()
        self.grab_set()

        with open("/home/hakan/Documents/GitHub/pythonInstaller/test/installer_data.json", "r") as file:
            self.text_data = json.load(file)

        self.button_font = customtkinter.CTkFont(family="Arial", size=18)

        modal_mapping = {
            "exit": "exit_modal",
            "attention": "attention_modal"
        }

        modal_key = modal_mapping.get(modal.lower())
        if modal_key is None:
            raise ValueError(f"Unknown modal type: {modal}")

        modal_data = self.text_data.get(modal_key)
        if modal_data is None:
            raise KeyError(f"Modal data not found for key: {modal_key}")

        self.title(modal_data["modal_title"])
        self.message_label = customtkinter.CTkLabel(
            self, text=modal_data["modal_label"], font=customtkinter.CTkFont(family="Arial", size=16)
        )
        self.message_label.pack(padx=10, pady=10)

        if modal.lower() == "exit":
            self.create_exit_modal()
        elif modal.lower() == "attention":
            self.create_attention_modal()

    def create_exit_modal(self):
        self.ok_button = customtkinter.CTkButton(
            self,
            text="Yes",
            text_color="white",
            command=self.ok_action,
            bg_color="#2B2631",
            fg_color="#f04141",
            font=self.button_font
        )
        self.ok_button.pack(side="left", padx=10, pady=20)

        self.cancel_button = customtkinter.CTkButton(
            self,
            text="No",
            text_color="white",
            command=self.cancel_action,
            bg_color="#2B2631",
            fg_color="#10dc60",
            font=self.button_font
        )
        self.cancel_button.pack(side="right", padx=10, pady=20)

    def create_attention_modal(self):
        self.protocol("WM_DELETE_WINDOW", self.ok_action)
        self.ok_button = customtkinter.CTkButton(
            self,
            text="Ok",
            text_color="white",
            command=self.ok_action,
            bg_color="#2B2631",
            fg_color="#10dc60",
            font=self.button_font
        )
        self.ok_button.pack(pady=20)

    def ok_action(self):
        self.master.quit()
        self.destroy()

    def cancel_action(self):
        self.destroy()
