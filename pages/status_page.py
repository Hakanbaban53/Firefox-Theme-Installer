from os import listdir, makedirs, path
from json import load, dump
from threading import Thread
from customtkinter import (
    CTkFrame,
    CTkImage,
    CTkLabel,
    CTkFont,
    CTkTextbox,
    CTkProgressBar,
)
from PIL import Image
from components.create_navigation_button import NavigationButton
from modals.info_modals import InfoModals
from functions.edit_file_variables import VariableUpdater
from functions.get_os_properties import OSProperties
from functions.install_files import FileActions


class StatusPage(CTkFrame):
    def __init__(self, parent, controller, base_dir):
        super().__init__(parent)
        self.controller = controller
        self.base_dir = base_dir

        self.ICON_PATH = path.join(base_dir, "assets", "icons")
        self.BACKGROUND_PATH = path.join(base_dir, "assets", "backgrounds")
        self.DATA_PATH = path.join(base_dir, "data", "installer_data.json")
        self.navigation_button_data_path = path.join(self.base_dir,"data", "components", "navigation_button_data.json")
        self.OS_PROPERTIES_PATH = path.join(
            base_dir, "data/OS data/os_properties.json"
        )

        self.text_data = self.load_json_data(self.DATA_PATH)
        self.navigation_button_data=self.load_json_data(self.navigation_button_data_path)
        self.button_data = self.navigation_button_data["navigation_buttons"]
        self.come_from_which_page = None

        self.os_values = OSProperties(self.OS_PROPERTIES_PATH).get_values()
        self.navigation_button = NavigationButton(self.button_data)
        self.file_actions = FileActions(self.os_values["os_name"])

        self.configure_layout()
        self.create_widgets()

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
        self.status_page_frame = CTkFrame(
            self,
            fg_color="#2B2631",
        )
        self.status_page_frame.grid(row=0, column=1, sticky="SW")
        self.status_page_frame.columnconfigure(0, weight=1)

    def create_widgets(self):
        self.create_header()
        self.create_action_status()
        self.create_progress_bar()
        self.create_output_entry()
        self.create_bottom_widgets()

    def create_header(self):
        header_title_bg = self.load_image(
            path.join(self.BACKGROUND_PATH, "header_title_background.png"), (250, 64)
        )
        line_top_img = self.load_image(path.join(self.BACKGROUND_PATH, "line_top.png"), (650, 6))

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
        self.action_label.grid(row=2, column=0, padx=60, pady=(14, 2), sticky="W")

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
            state="disabled",
        )
        self.output_entry.grid(row=4, column=0, padx=60, pady=20, sticky="NSEW")

    def create_bottom_widgets(self):
        bottom_frame = CTkFrame(self, fg_color="#2B2631")
        bottom_frame.place(x=190.0, y=600.0)

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
        self.navigation_button.create_navigation_button(
            parent,
            "Finish",
            path.join(self.ICON_PATH, "finish_icon.png"),
            lambda: InfoModals(self, self.base_dir, "Attention"),
            padding_x=(10, 20),
            side="right",
            img_side="right",
        )

        self.back_button = self.navigation_button.create_navigation_button(
            parent,
            "Back",
            path.join(self.ICON_PATH, "back_icon.png"),
            padding_x=(5, 5),
            side="right",
            command=lambda: self.controller.show_frame(
                f"{self.come_from_which_page}_page"
            ),
            state="disabled",
        )
        self.navigation_button.create_navigation_button(
            parent,
            "Exit",
            path.join(self.ICON_PATH, "exit_icon.png"),
            lambda: InfoModals(self, self.base_dir, "Exit"),
            padding_x=(20, 10),
            side="left",
        )

    def create_os_info(self, parent):
        os_icon_image = self.load_image(
            path.join(self.ICON_PATH, f"{self.os_values['os_name'].lower()}.png"), (20, 24)
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
                image=self.load_image(path.join(self.ICON_PATH, "check.png"), (20, 20)),
                compound="right",
            )
        elif self.come_from_which_page == "remove":
            self.action_label.configure(
                text="Removed  ",
                image=self.load_image(path.join(self.ICON_PATH, "check.png"), (20, 20)),
                compound="right",
            )        

    def update_parameters(self, **kwargs):
        self.come_from_which_page = kwargs.get("come_from_which_page")
        self.profile_folder = kwargs.get("profile_folder")
        self.application_folder = kwargs.get("application_folder")
        self.base_dir = kwargs.get("base_dir")
        self.theme_dir = kwargs.get("theme_dir")
        self.custom_script_loader = kwargs.get("custom_script_loader")
        self.selected_theme_data = kwargs.get("selected_theme_data")
        self.chrome_folder = path.join(self.profile_folder, "chrome")
        print(self.selected_theme_data)

        # Decide which function to call based on the page source
        if self.come_from_which_page == "install":
            self.install()
        elif self.come_from_which_page == "remove":
            self.remove()

        operation_thread = Thread(
            target=self.file_actions.execute_operations,
            args=(self.progress_bar, self.output_entry),
        )
        operation_thread.start()

        self.after(500, self.update_text)

    def install(self):
        # Handles the installation process
        user_js_src = path.join(self.base_dir, "fx-autoconfig", "user.js")
        if path.exists(user_js_src):
            self.file_actions.copy_file(user_js_src, self.profile_folder)

        if self.custom_script_loader:
            self.file_actions.copy_file(
                path.join(self.base_dir, "fx-autoconfig", "config.js"),
                self.application_folder,
            )
            self.file_actions.copy_file(
                path.join(self.base_dir, "fx-autoconfig", "mozilla.cfg"),
                self.application_folder,
            )
            self.file_actions.copy_file(
                path.join(self.base_dir, "fx-autoconfig", "config-prefs.js"),
                path.join(self.application_folder, "defaults", "pref"),
            )
            self.file_actions.copy_file(
                path.join(self.base_dir, "fx-autoconfig", "local-settings.js"),
                path.join(self.application_folder, "defaults", "pref"),
            )

        # Copy all other files and folders into the chrome folder (excluding user.js)
        for item in listdir(self.theme_dir):
            src_path = path.join(self.theme_dir, item)
            dest_path = path.join(self.chrome_folder, item)  # Copy into chrome folder
            if path.isdir(src_path):
                self.file_actions.copy_folder(src_path, dest_path)
            elif path.isfile(src_path) and item != "user.js":
                makedirs(path.dirname(dest_path), exist_ok=True)
                self.file_actions.copy_file(src_path, dest_path)

        theme_data_path = path.join(self.chrome_folder, "selected_theme_data.json")
        with open(theme_data_path, 'w') as json_file:
            dump(self.selected_theme_data, json_file, indent=4)

    def remove(self):
        # Handles the removal process
        self.action_label.configure(text="Removing...")

        self.file_actions.remove_file(path.join(self.application_folder, "config.js"))
        self.file_actions.remove_file(path.join(self.application_folder, "mozilla.cfg"))
        self.file_actions.remove_file(
            path.join(self.application_folder, "defaults", "pref", "config-prefs.js")
        )
        self.file_actions.remove_file(
            path.join(self.application_folder, "defaults", "pref", "local-settings.js")
        )
        self.file_actions.remove_file(path.join(self.profile_folder, "user.js"))
        self.file_actions.remove_folder(path.join(self.profile_folder, "chrome"))

        theme_data_path = path.join(self.chrome_folder, "selected_theme_data.json")
        if path.exists(theme_data_path):
            self.file_actions.remove_file(theme_data_path)


