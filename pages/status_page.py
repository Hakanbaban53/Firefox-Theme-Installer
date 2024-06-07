from json import load
from threading import Thread
from customtkinter import (
    CTkFrame,
    CTkImage,
    CTkLabel,
    CTkFont,
    CTkProgressBar,
    CTkTextbox,
    CTkButton,
)
from PIL import Image
from modals.combined_modal import CombinedModal
from functions.get_os_properties import OSProperties
from functions.install_files import FileActions

class StatusPage(CTkFrame):
    ICON_PATH = "../RealFire-Installer/assets/icons/"
    BACKGROUND_PATH = "../RealFire-Installer/assets/backgrounds/"
    DATA_PATH = "../RealFire-Installer/data/installer_data.json"

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.file_actions = FileActions()
        self.os_values = OSProperties().get_values()

        self.come_from_which_page = None
        self.load_text_data()
        self.button_data = self.text_data.get("common_values")["navigation_buttons"]

        self.configure_layout()
        self.create_widgets()

    def load_text_data(self):
        with open(self.DATA_PATH, "r", encoding="utf-8") as file:
            self.text_data = load(file)

    def load_image(self, file_name, size):
        return CTkImage(
            light_image=Image.open(file_name),
            dark_image=Image.open(file_name),
            size=size,
        )

    def configure_layout(self):
        self.fg_color = "#2B2631"
        self.grid(row=0, column=1, sticky="SW")
        self.columnconfigure(0, weight=1)

    def create_widgets(self):
        self.create_status_page_frame()
        self.create_header()
        self.create_action_status()
        self.create_progress_bar()
        self.create_output_entry()
        self.create_bottom_widgets()

    def create_status_page_frame(self):
        self.status_page_frame = CTkFrame(
            self,
            fg_color="#2B2631",
        )
        self.status_page_frame.grid(row=0, column=0, sticky="SW")
        self.status_page_frame.columnconfigure(0, weight=1)

    def create_header(self):
        header_title_bg = self.load_image(
            f"{self.BACKGROUND_PATH}header_title_background.png", (250, 64)
        )
        line_top_img = self.load_image(f"{self.BACKGROUND_PATH}line_top.png", (650, 6))

        header_label = CTkLabel(
            self.status_page_frame,
            text="Status",
            image=header_title_bg,
            text_color="White",
            font=CTkFont(family="Inter", size=24, weight="bold"),
        )
        header_label.grid(
            row=0, column=0, columnspan=2, padx=273, pady=(75, 0), sticky="NSEW"
        )

        line_top_label = CTkLabel(self.status_page_frame, text="", image=line_top_img)
        line_top_label.grid(
            row=1, column=0, columnspan=2, padx=10, pady=(20, 30), sticky="NSEW"
        )

    def create_action_status(self):
        self.action_label = CTkLabel(
            self.status_page_frame,
            fg_color="#2B2631",
            text_color="#FFFFFF",
            text="",
            image=None,
            compound="right",
            font=CTkFont(family="Inter", size=18, weight="bold"),
        )
        self.action_label.grid(row=2, column=0, padx=60, pady=10, sticky="W")

    def create_progress_bar(self):
        self.progress_bar = CTkProgressBar(
            self.status_page_frame,
            orientation="horizontal",
            height=24,
            fg_color="#666666",
            progress_color="#9747FF",
        )
        self.progress_bar.grid(row=3, column=0, padx=50, pady=10, sticky="NSEW")
        self.progress_bar.set(0)

    def create_output_entry(self):
        self.output_entry = CTkTextbox(
            self.status_page_frame,
            height=190,
            fg_color="white",
            text_color="black",
            corner_radius=12,
        )
        self.output_entry.grid(row=4, column=0, padx=60, pady=20, sticky="NSEW")

    def create_bottom_widgets(self):
        bottom_frame = CTkFrame(self, fg_color="#2B2631")
        bottom_frame.place(x=200.0, y=600.0)

        navigation_frame = CTkFrame(
            bottom_frame,
            width=440,
            height=54,
            corner_radius=12,
            border_width=4,
            fg_color="white",
            border_color="#F89F24",
        )
        navigation_frame.grid(row=0, column=1, sticky="E")

        self.create_navigation_buttons(navigation_frame)
        self.create_os_info(bottom_frame)

    def create_navigation_buttons(self, parent):

        self.create_navigation_button(
            parent,
            "Finish",
            self.ICON_PATH + "finish_icon.png",
            lambda: CombinedModal(self, "Attention"),
            padding_x=(10, 20),
            side="right",
            img_side="right",
        )

        self.back_button = self.create_navigation_button(
            parent,
            "Back",
            self.ICON_PATH + "back_icon.png",
            padding_x=(5, 5),
            side="right",
            command=lambda: self.controller.show_frame(
                f"{self.come_from_which_page}_page"
            ),
            state="disabled",
        )
        self.create_navigation_button(
            parent,
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

    def create_os_info(self, parent):
        os_icon_image = self.load_image(
            f"{self.ICON_PATH}{self.os_values['os_name'].lower()}.png", (20, 24)
        )

        os_frame = CTkFrame(parent, corner_radius=12, fg_color="white")
        os_frame.grid(row=0, column=0, padx=20, sticky="W")

        os_label = CTkLabel(
            os_frame,
            text=f"{self.os_values['os_name']} ",
            text_color=self.os_values["os_color"],
            font=("Arial", 20, "bold"),
            image=os_icon_image,
            compound="right",
        )
        os_label.pack(padx=10, pady=10, side="right")

    def update_text(self):
        if self.come_from_which_page == "install":
            self.action_label.configure(
                text="Installed  ",
                image=self.load_image(f"{self.ICON_PATH}check.png", (20, 20)),
                compound="right",
            )
        elif self.come_from_which_page == "remove":
            self.action_label.configure(
                text="Removed  ",
                image=self.load_image(f"{self.ICON_PATH}check.png", (20, 20)),
                compound="right",
            )

    def update_parameters(self, **kwargs):
        self.come_from_which_page = kwargs.get("come_from_which_page")
        self.profile_folder = kwargs.get("profile_folder")
        self.application_folder = kwargs.get("application_folder")
        self.new_tab_wallpaper = kwargs.get("new_tab_wallpaper")
        self.accent_color = kwargs.get("accent_color")

        if self.come_from_which_page == "install":
            self.action_label.configure(text="Installing...")
            self.file_actions.move_file(
                "../RealFire-Installer/fx-autoconfig/config.js", self.application_folder
            )
            self.file_actions.move_file(
                "../RealFire-Installer/fx-autoconfig/mozilla.cfg",
                self.application_folder,
            )
            self.file_actions.move_file(
                "../RealFire-Installer/fx-autoconfig/config-prefs.js",
                f"{self.application_folder}/defaults/pref/",
            )
            self.file_actions.move_file(
                "../RealFire-Installer/fx-autoconfig/local-settings.js",
                f"{self.application_folder}/defaults/pref/",
            )
            self.file_actions.move_folder(
                "../RealFire-Installer/chrome", self.profile_folder
            )
            self.file_actions.move_file(
                "../RealFire-Installer/fx-autoconfig/user.js", self.profile_folder
            )
        elif self.come_from_which_page == "remove":
            self.action_label.configure(text="Removing...")
            self.file_actions.remove_file(f"{self.application_folder}/config.js")
            self.file_actions.remove_file(f"{self.application_folder}/mozilla.cfg")
            self.file_actions.remove_file(
                f"{self.application_folder}/defaults/pref/config-prefs.js"
            )
            self.file_actions.remove_file(
                f"{self.application_folder}/defaults/pref/local-settings.js"
            )
            self.file_actions.remove_file(f"{self.profile_folder}/user.js")
            self.file_actions.remove_folder(f"{self.profile_folder}/chrome")

        operation_thread = Thread(
            target=self.file_actions.execute_operations,
            args=(self.progress_bar, self.output_entry),
        )
        operation_thread.start()

        self.after(500, self.update_text)

        # For Testing
        # self.back_button.configure(
        #     command=lambda: self.controller.show_frame(
        #         f"{self.come_from_which_page}_page"
        #     ),
        # )
