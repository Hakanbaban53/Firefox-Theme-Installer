import json
from pathlib import Path
from custom_exit_message import CombinedModal
from status_page import status_page
from home_page import home_page
from remove_page import remove_page
from install_page import install_page
from os_properties import OSProperties
import customtkinter
from PIL import Image


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(
    r"/home/hakan/Documents/GitHub/pythonInstaller/assets/"
)

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class MultiPageApp(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        customtkinter.CTk.__init__(self, *args, **kwargs)

        with open("/home/hakan/Documents/GitHub/pythonInstaller/test/installer_data.json", "r") as file:
            self.text_data = json.load(file)

        self.title(self.text_data["installer_info"]["installer_title"])
        self.geometry("1108x667")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.exit_confirmation)

        self.cont = home_page
        self.os_properties = OSProperties()

        self.container = customtkinter.CTkFrame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

    def create_frame(self, page_class):
        frame = page_class(self.container, self, os_properties=self.os_properties)
        frame.configure(fg_color="#2B2631")

        frame.installer_img = customtkinter.CTkImage(
            light_image=Image.open(relative_to_assets("img/installer_img.png")),
            dark_image=Image.open(relative_to_assets("img/installer_img.png")),
            size=(310, 667),
        )
        frame.installer_img_label = customtkinter.CTkLabel(
            frame,
            text="",
            image=frame.installer_img,
        )
        frame.installer_img_label.place(x=0, y=0)

        version = customtkinter.CTkLabel(
            frame,
            text=self.text_data["installer_info"]["installer_version"],
            text_color="White",
            bg_color="#2B2631",
            font=customtkinter.CTkFont(family="Inter", size=14),
        )
        version.place(x=65.0, y=620.0)

        frame.grid(row=0, column=0, sticky="nsew")
        return frame

    def show_frame(self, page_name, **kwargs):
        page_class = {
            "status_page": status_page,
            "home_page": home_page,
            "remove_page": remove_page,
            "install_page": install_page,
        }.get(page_name)

        if page_class:
            if page_class not in self.frames:
                self.frames[page_class] = self.create_frame(page_class)

            frame = self.frames[page_class]
            frame.update_parameters(**kwargs)
            frame.tkraise()

    def exit_confirmation(self):
        CombinedModal(self, "Exit")


if __name__ == "__main__":
    app = MultiPageApp()
    app.show_frame("home_page")
    app.mainloop()



# import os
# import subprocess
# import sys

# def run_as_admin():
#     # Use pkexec to execute a command with administrative privileges
#     cmd = "pkexec " + " ".join(sys.argv)
#     subprocess.call(cmd, shell=True)

# run_as_admin()
