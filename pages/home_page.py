from json import load
from time import sleep
from tkinter import PhotoImage, Label, TclError
from itertools import cycle
from threading import Thread

from customtkinter import (
    CTkFrame,
    CTkImage,
    CTkLabel,
    CTkButton,
    StringVar,
    CTkCheckBox,
)
from PIL import Image

from modals.check_files_modal import FileInstallerModal
from modals.combined_modal import CombinedModal
from functions.get_os_properties import OSProperties
from functions.detect_files import FileManager


class HomePage(CTkFrame):
    ICON_PATH = "../RealFire-Installer/assets/icons/"
    BACKGROUND_PATH = "../RealFire-Installer/assets/backgrounds/"
    DATA_PATH = "../RealFire-Installer/data/installer_data.json"
    FILES_DATA_PATH = "../RealFire-Installer/data/installer_files_data.json"
    FILES_DATA_URL = "https://raw.githubusercontent.com/Hakanbaban53/RealFire-Installer/main/data/installer_files_data.json"
    ANIMATION_SPEED = 100

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.text_data = self.load_json_data(self.DATA_PATH)
        self.button_data = self.text_data.get("common_values")["navigation_buttons"]
        self.os_values = OSProperties().get_values()

        self.configure_layout()
        self.create_widgets()

        self.attention_icon = PhotoImage(
            file="../RealFire-Installer/assets/icons/attention.png", height=24, width=24
        )
        self.check_icon = PhotoImage(
            file="../RealFire-Installer/assets/icons/check.png", height=20, width=20
        )

    def load_json_data(self, path):
        with open(path, "r") as file:
            return load(file)

    def load_image(self, file_name, size):
        return CTkImage(
            light_image=Image.open(file_name),
            dark_image=Image.open(file_name),
            size=size,
        )

    def configure_layout(self):
        home_page_frame = CTkFrame(
            self,
            fg_color="#2B2631",
        )
        home_page_frame.grid(row=0, column=1, sticky="SW")
        home_page_frame.columnconfigure(0, weight=1)
        self.home_page_frame = home_page_frame

    def create_widgets(self):
        self.create_header()
        self.create_os_info()
        self.create_navigation_buttons()
        self.create_file_detection()
        self.create_recheck_skip_section()

    def create_header(self):
        header_title_bg = self.load_image(
            f"{self.BACKGROUND_PATH}header_title_background.png", (390, 64)
        )
        line_top_img = self.load_image(f"{self.BACKGROUND_PATH}line_top.png", (650, 6))

        header_label = CTkLabel(
            self.home_page_frame,
            text="Welcome to the RealFire Installer",
            image=header_title_bg,
            text_color="White",
            font=("Inter", 22, "bold"),
        )
        header_label.grid(
            row=0, column=0, columnspan=2, padx=203, pady=(75, 0), sticky="NSEW"
        )

        line_top_label = CTkLabel(self.home_page_frame, text="", image=line_top_img)
        line_top_label.grid(
            row=1, column=0, columnspan=2, padx=10, pady=(20, 30), sticky="NSEW"
        )

    def create_os_info(self):
        os_icon_image = self.load_image(
            f"{self.ICON_PATH}{self.os_values['os_name'].lower()}.png", (20, 24)
        )

        os_label = CTkLabel(
            self.home_page_frame,
            text="Detected Operating System: ",
            text_color="White",
            font=("Inter", 20, "bold"),
        )
        os_label.grid(row=2, column=0, padx=(175, 0), sticky="ew")

        os_frame = CTkFrame(self.home_page_frame, corner_radius=12, fg_color="white")
        os_frame.grid(row=2, column=1, padx=(0, 185), sticky="ew")

        os_info_label = CTkLabel(
            os_frame,
            text=f"{self.os_values['os_name']} ",
            text_color=self.os_values["os_color"],
            font=("Arial", 20, "bold"),
            image=os_icon_image,
            compound="right",
        )
        os_info_label.pack(padx=10, pady=10, side="left")

    def create_navigation_buttons(self):
        select_action_img = self.load_image(
            f"{self.BACKGROUND_PATH}header_title_background.png", (270, 36)
        )

        select_action_label = CTkLabel(
            self.home_page_frame,
            text="Please Select the Action",
            image=select_action_img,
            text_color="White",
            font=("Inter", 20, "bold"),
        )
        select_action_label.grid(
            row=3, column=0, columnspan=2, padx=60, pady=(70, 30), sticky="ew"
        )

        navigation_frame = CTkFrame(
            self.home_page_frame,
            width=460,
            height=54,
            corner_radius=12,
            border_width=4,
            fg_color="white",
            border_color="#F89F24",
        )
        navigation_frame.grid(row=4, column=0, columnspan=2, sticky="")

        self.create_navigation_button(
            navigation_frame,
            "Remove",
            self.ICON_PATH + "remove_icon.png",
            lambda: self.controller.show_frame("remove_page"),
            padding_x=(10, 20),
            side="right",
        )
        self.install_button = self.create_navigation_button(
            navigation_frame,
            "Install",
            self.ICON_PATH + "install_icon.png",
            lambda: self.controller.show_frame("install_page"),
            padding_x=(5, 5),
            side="right",
            state="disabled",
        )
        self.create_navigation_button(
            navigation_frame,
            "Exit",
            self.ICON_PATH + "exit_icon.png",
            lambda: CombinedModal(self, "Exit"),
            padding_x=(20, 10),
            side="left",
        )

    def create_navigation_button(
        self,
        parent,
        text,
        image_path,
        command,
        padding_x,
        side,
        img_side="left",
        **kwargs,
    ):
        button_image = self.load_image(image_path, (20, 20))
        button = CTkButton(
            parent,
            width=float(self.button_data["width"]),
            height=float(self.button_data["height"]),
            corner_radius=float(self.button_data["corner_radius"]),
            bg_color=self.button_data["bg_color"],
            fg_color=self.button_data["fg_color"],
            hover_color=self.button_data["hover_color"],
            text_color=self.button_data["text_color"],
            font=(self.button_data["font_family"], int(self.button_data["font_size"])),
            image=button_image,
            text=text,
            compound=img_side,
            command=command,
            **kwargs,
        )
        button.pack(padx=padding_x, pady=10, side=side)
        return button

    def create_file_detection(self):
        self.detect_files_frame = CTkFrame(
            self.home_page_frame, corner_radius=12, fg_color="white"
        )
        self.detect_files_frame.grid(
            row=5, column=0, padx=0, pady=(20, 10), columnspan=2, sticky=""
        )

        self.detect_files_text = Label(
            self.detect_files_frame,
            text="Checking The Files   ",
            fg="#000000",
            bg="#FFFFFF",
            font=("Arial", 16, "bold"),
            compound="right",
        )
        self.detect_files_text.grid(row=0, column=0, padx=10, pady=10, sticky="")

        install_icon = self.load_image(
            self.ICON_PATH + "get_from_internet.png", (24, 24)
        )
        self.install_files_button = CTkButton(
            master=self.detect_files_frame,
            text="Install Missing Files",
            width=float(self.button_data["width"]),
            height=float(self.button_data["height"]),
            corner_radius=float(self.button_data["corner_radius"]),
            bg_color=self.button_data["bg_color"],
            fg_color=self.button_data["fg_color"],
            hover_color=self.button_data["hover_color"],
            text_color=self.button_data["text_color"],
            font=(self.button_data["font_family"], int(self.button_data["font_size"])),
            command=self.install_files,
            image=install_icon,
            state="disabled",
        )

        thread = Thread(target=self.locate_files)
        thread.start()

    def create_recheck_skip_section(self):
        self.recheck_skip_frame = CTkFrame(self.home_page_frame, fg_color="#2B2631")
        self.recheck_skip_frame.grid(
            row=6, column=0, padx=0, pady=0, columnspan=2, sticky=""
        )

        self.check_var = StringVar(value="off")
        self.user_know_what_do = CTkCheckBox(
            self.recheck_skip_frame,
            text="I know what I do",
            text_color="#FFFFFF",
            font=("Arial", 16, "bold"),
            command=self.checkbox_event,
            variable=self.check_var,
            onvalue="on",
            offvalue="off",
        )

        reload_icon = self.load_image(self.ICON_PATH + "reload_icon.png", (20, 20))
        self.recheck_button = CTkButton(
            self.recheck_skip_frame,
            width=40,
            height=40,
            text="",
            fg_color="#FFFFFF",
            command=self.recheck_files,
            image=reload_icon,
        )
        self.recheck_button.grid(
            row=1, column=0, padx=0, pady=0, columnspan=2, sticky=""
        )

    def load_gif(self):
        frames = []
        index = 0
        while True:
            try:
                frame = PhotoImage(
                    file="../RealFire-Installer/assets/icons/block_spin.gif",
                    format=f"gif -index {index}",
                )
                frames.append(frame)
                index += 2
            except TclError:
                break
        return cycle(frames)

    def update_gif(self, frames):
        frame = next(frames)
        self.detect_files_text.config(image=frame)
        self.animation_id = self.after(self.ANIMATION_SPEED, self.update_gif, frames)

    def locate_files(self):
        frames = self.load_gif()
        self.update_gif(frames)
        sleep(1)
        file_check_result = FileManager(self.FILES_DATA_PATH, self.FILES_DATA_URL).check_files_exist()
        self.master.after_cancel(self.animation_id)
        if not file_check_result:
            self.detect_files_text.configure(
                text="All Files Installed  ", fg="#10dc60", image=self.check_icon
            )
            self.install_button.configure(state="normal")
            self.recheck_button.grid(row=6, column=0, padx=0, pady=0, sticky="")
            self.user_know_what_do.grid_remove()
        else:
            self.detect_files_text.configure(
                text="Some Files Are Missing  ", fg="#f04141", image=self.attention_icon
            )
            self.install_files_button.configure(state="normal")
            self.install_files_button.grid(row=1, column=0, padx=10, pady=10, sticky="")
            self.user_know_what_do.grid(row=6, column=0, padx=10, pady=0, sticky="")
            self.recheck_button.grid(row=6, column=1, padx=10, pady=0, sticky="")

    def checkbox_event(self):
        if self.user_know_what_do.get() == "on":
            self.install_button.configure(state="normal")
            self.install_files_button.configure(state="disabled")
            self.detect_files_text.configure(
                text="Skipped by User  ", fg="#f04141", image=self.attention_icon
            )
            self.recheck_button.configure(state="disabled")
        else:
            self.install_button.configure(state="disabled")
            self.install_files_button.configure(state="normal")
            self.detect_files_text.configure(
                text="Some Files Are Missing  ", fg="#f04141", image=self.attention_icon
            )
            self.recheck_button.configure(state="normal")

    def install_files(self):
        modal = FileInstallerModal(self)
        self.wait_window(modal)
        self.recheck_files()

    def recheck_files(self):
        self.detect_files_text.configure(text="Checking The Files  ", fg="#000000")
        self.install_button.configure(state="disabled")
        self.install_files_button.grid_remove()
        self.user_know_what_do.grid_remove()
        thread = Thread(target=self.locate_files)
        thread.start()

    def update_parameters(self, **kwargs):
        # Process and use the parameters as needed
        pass
