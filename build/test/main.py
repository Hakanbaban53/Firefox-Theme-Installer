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
    r"/home/hakan/Documents/GitHub/pythonInstaller/build/assets"
)

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class MultiPageApp(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        customtkinter.CTk.__init__(self, *args, **kwargs)

        self.title("RealFire Installer")
        self.geometry("1108x667")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.exit_confirmation)
        


        # Instantiate the OSProperties class
        self.os_properties = OSProperties()

        # Detect the operating system
        self.os_properties.get_os()

        # Container to hold all the pages
        container = customtkinter.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (home_page, install_page, remove_page, status_page):
            frame = F(container, self, os_properties=self.os_properties)

            frame.configure(fg_color="#2B2631")
            frame.installer_img = customtkinter.CTkImage(
                light_image=Image.open(
                    "/home/hakan/Documents/GitHub/pythonInstaller/build/assets/img/installer_img.png"
                ),
                dark_image=Image.open(
                    "/home/hakan/Documents/GitHub/pythonInstaller/build/assets/img/installer_img.png"
                ),
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
                text=" RealFire Version: Beta β 0.1 ",
                text_color="White",
                bg_color="#2B2631",
                font=customtkinter.CTkFont(family="Inter", size=14),
            )
            version.place(x=65.0, y=620.0)
            # Add the version label to each frame


            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("home_page")

    def show_frame(self, cont, **kwargs):
        frame = self.frames[cont]
        frame.update_parameters(**kwargs)
        frame.tkraise()

    def exit_confirmation(self):
        CombinedModal(self, "Exit Confirmation", "Are you sure you want to exit?")


if __name__ == "__main__":
    app = MultiPageApp()
    app.mainloop()


# import os
# import subprocess
# import sys

# def run_as_admin():
#     # Use pkexec to execute a command with administrative privileges
#     cmd = "pkexec " + " ".join(sys.argv)
#     subprocess.call(cmd, shell=True)

# run_as_admin()
