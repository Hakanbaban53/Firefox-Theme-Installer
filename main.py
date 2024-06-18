import os
import ctypes
from json import load
from sys import exit
import sys
from tkinter import Tk
from customtkinter import CTk, CTkImage, CTkLabel, CTkFont, CTkFrame, CTkButton
from PIL import Image
from modals.combined_modal import CombinedModal
from pages.home_page import HomePage
from pages.install_page import InstallPage
from pages.remove_page import RemovePage
from pages.status_page import StatusPage


class MultiPageApp(CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Determine base directory using _MEIPASS or current script directory
        self.base_dir = getattr(
            sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__))
        )  # Also I send the other pages and functions this path.

        if not self.is_admin():
            self.show_admin_error()
            exit()

        installer_data_path = os.path.join(self.base_dir, "data", "installer_data.json")
        with open(installer_data_path, "r", encoding="utf-8") as file:
            self.text_data = load(file)

        self.title(self.text_data["common_values"]["installer_info"]["installer_title"])
        self.geometry("1115x666")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.exit_confirmation)

        if os.name == "nt":
            icon_path = os.path.join(self.base_dir, "assets", "icons", "firefox.ico")
            self.iconbitmap(icon_path)

        self.center_window()

        self.installer_img = CTkImage(
            light_image=Image.open(
                os.path.join(
                    self.base_dir, "assets", "backgrounds", "installer_img.png"
                )
            ),
            dark_image=Image.open(
                os.path.join(
                    self.base_dir, "assets", "backgrounds", "installer_img.png"
                )
            ),
            size=(315, 666),
        )

        self.installer_img_label = CTkLabel(
            self,
            text=self.text_data["common_values"]["installer_info"]["installer_version"],
            text_color="white",
            image=self.installer_img,
            font=CTkFont(family="Inter", size=14),
        )
        self.installer_img_label.place(x=0, y=0)  # Place image label at (0, 0)

        self.container = CTkFrame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.frames = {}

    def create_frame(self, page_class):
        frame = page_class(self.container, self, self.base_dir)

        frame.configure(
            fg_color="#2B2631",
            corner_radius=0,
        )

        frame.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        return frame

    def slide_to_frame(self, current_frame, next_frame, x, speed=35, direction=None):
        if direction is None:
            current_index = list(self.frames.values()).index(current_frame)
            next_index = list(self.frames.values()).index(next_frame)
            direction = "left" if current_index > next_index else "right"

        if direction == "right":
            next_x = self.winfo_width() - x
            current_x = -x + 315
        else:
            next_x = x - self.winfo_width() + 625
            current_x = x + 2 * 315

        next_frame.place(x=next_x, y=0, relwidth=1, relheight=1)
        current_frame.place(x=current_x, y=0, relwidth=1, relheight=1)

        next_frame.lift()
        self.update()

        if direction == "left" and x <= self.winfo_width() - 315:
            self.after(
                1,
                self.slide_to_frame,
                current_frame,
                next_frame,
                x + speed,
                speed,
                direction,
            )
        elif direction == "right" and x <= self.winfo_width() - 315:
            self.after(
                1,
                self.slide_to_frame,
                current_frame,
                next_frame,
                x + speed,
                speed,
                direction,
            )
        else:
            current_frame.place_forget()

    def show_frame(self, page_name, **kwargs):
        self.installer_img_label.lift()

        page_class = {
            "home_page": HomePage,
            "install_page": InstallPage,
            "remove_page": RemovePage,
            "status_page": StatusPage,
        }.get(page_name)

        if page_class:
            if page_class not in self.frames:
                self.frames[page_class] = self.create_frame(page_class)

            current_frame = None
            for frame in self.frames.values():
                if frame.winfo_ismapped():
                    current_frame = frame
                    break

            next_frame = self.frames[page_class]
            if current_frame is not None:
                self.slide_to_frame(current_frame, next_frame, 0)
            else:
                next_frame.place(x=315, y=0, relwidth=1, relheight=1)

            next_frame.update_parameters(**kwargs)
            next_frame.tkraise()

    def is_admin(self):
        try:
            if os.name == "nt":  # Windows
                try:
                    is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
                except AttributeError:
                    is_admin = False
                return is_admin
            else:  # Unix-like systems
                return os.getuid() == 0
        except Exception as e:
            print(f"Error checking admin rights: {e}")
            return False

    def exit_confirmation(self):
        CombinedModal(self, self.base_dir, "Exit")

    def center_window(self):
        self.update_idletasks()

        window_width = self.winfo_width()
        window_height = self.winfo_height()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.geometry("+{}+{}".format(x, y))

    def show_admin_error(self):
        modal = Tk()
        modal.title("Admin Error")
        modal.geometry("300x150")
        modal.configure(bg="#2B2631")
        modal.resizable(False, False)

        if os.name == "nt":
            icon_path = os.path.join(self.base_dir, "assets", "icons", "firefox.ico")
            modal.iconbitmap(icon_path)

        label = CTkLabel(
            modal,
            text="Administrative privileges are required.",
            text_color="white",
            font=CTkFont(family="Segoe UI", size=15),
        )
        label.pack(padx=20, pady=20)

        ok_button = CTkButton(
            modal,
            text="OK",
            text_color="white",
            command=exit,
            bg_color="#2B2631",
            fg_color="#f04141",
            font=("Arial", 14),
        )
        ok_button.pack(pady=10)

        # Bind the close event to the exit function
        modal.protocol("WM_DELETE_WINDOW", exit)

        # Center the modal window
        modal.update_idletasks()
        width = modal.winfo_width()
        height = modal.winfo_height()
        x = (modal.winfo_screenwidth() // 2) - (width // 2)
        y = (modal.winfo_screenheight() // 2) - (height // 2)
        modal.geometry(f"{width}x{height}+{x}+{y}")

        modal.grab_set()
        modal.mainloop()


if __name__ == "__main__":
    app = MultiPageApp()
    app.show_frame("home_page")
    app.mainloop()
