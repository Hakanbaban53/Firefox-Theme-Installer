import tkinter as tk
import customtkinter


class CombinedModal(tk.Toplevel):
    def __init__(self, parent, title, message, ok_text="Yes", cancel_text="No"):
        super().__init__(parent)
        self.title(title)
        self.geometry("250x100")
        self.configure(bg="#2B2631")
        self.resizable(False, False)

        # Wait for the dialog to be fully visible before grabbing focus
        self.wait_visibility()
        self.grab_set()

        self.button_font = customtkinter.CTkFont(family="Arial", size=18)

        self.message_label = customtkinter.CTkLabel(
            self, text=message, font=customtkinter.CTkFont(family="Arial", size=16)
        )
        self.message_label.pack(pady=5)

        if ok_text and cancel_text == "No":
            self.ok_button = customtkinter.CTkButton(
                self,
                text=ok_text,
                text_color="white",
                command=self.ok_action,
                bg_color="#2B2631",
                fg_color="#f04141",
                font=self.button_font
            )
            self.ok_button.pack(side="left", padx=10)

            self.cancel_button = customtkinter.CTkButton(
                self,
                text=cancel_text,
                text_color="white",
                command=self.cancel_action,
                bg_color="#2B2631",
                fg_color="#10dc60",
                font=self.button_font
            )
            self.cancel_button.pack(side="right", padx=10)
        else:
            self.protocol("WM_DELETE_WINDOW", self.ok_action)
            self.ok_button = customtkinter.CTkButton(
                self,
                text=ok_text,
                text_color="white",
                command=self.ok_action,
                bg_color="#2B2631",
                fg_color="#10dc60",
                font=self.button_font
            )
            self.ok_button.pack(pady=10)

    def ok_action(self):
        self.master.quit()  # Destroy the parent window
        self.destroy()  # Destroy the dialog first

    def cancel_action(self):
        self.destroy()  # Destroy the dialog

