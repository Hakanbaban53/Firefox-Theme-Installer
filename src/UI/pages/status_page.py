from os import listdir, makedirs, path
from json import dump
from customtkinter import (
    CTkFrame,
    CTkLabel,
    CTkTextbox,
    CTkProgressBar,
)
from tkinter import Frame

from UI.components.create_header import CreateHeader
from UI.components.create_navigation_button import NavigationButton
from core.component_tools.thread_manager import ThreadManager
from core.data_tools.get_os_properties import OSProperties
from core.data_tools.image_loader import ImageLoader
from core.data_tools.load_json_data import LoadJsonData
from core.file_utils.file_actions import FileActions
from UI.modals.info_modals import InfoModals
from data.static.global_data import (
    APP_LANGUAGE,
    ASSETS_PATH,
    BACK_ICON,
    BASE_DIR,
    CHECK_ICON,
    EXIT_ICON,
    FINISH_ICON,
    HEADER_TITLE_BACKGROUND,
    LINE_TOP,
)


class StatusPage(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        # Load the UI data from the JSON file
        self.controller = controller
        UI_DATA_PATH = path.join(
            BASE_DIR, "data", "language", "pages", "status_page", f"{APP_LANGUAGE}.json"
        )
        load_json_data = LoadJsonData()
        self.ui_data = load_json_data.load_json_data(UI_DATA_PATH)

        self.thread_manager = ThreadManager()

        self.os_properties = OSProperties()
        self.os_values = self.os_properties.get_values()

        self.CACHE_PATH = self.os_properties.get_cache_location()

        self.navigation_button = NavigationButton()

        self.come_from_which_page = None

        self.file_actions = FileActions(self.os_values["os_name"])

        self.configure_layout()
        self.create_widgets()

    def configure_layout(self):
        self.status_page_frame = CTkFrame(
            self,
            fg_color="#2B2631",
        )
        self.status_page_frame.grid(row=0, column=1, sticky="SW")
        self.status_page_frame.columnconfigure(0, weight=1)

    def create_widgets(self):
        self.create_images()
        self.create_header()
        self.create_action_status()
        self.create_progress_bar()
        self.create_output_entry()
        self.create_bottom_widgets()

    def create_images(self):
        image_loader = ImageLoader(ASSETS_PATH)

        self.check_icon = image_loader.load_CTK_image(CHECK_ICON, (24, 24))
        self.os_icon_image = image_loader.load_CTK_image(
            f"{self.os_values["os_name"].lower()}.png", (20, 24)
        )
        self.header_title_bg = image_loader.load_CTK_image(
            HEADER_TITLE_BACKGROUND, size=(390, 64)  # Specific size for HomePage
        )
        self.line_top_img = image_loader.load_CTK_image(LINE_TOP, (650, 6))

    def create_header(self):
        header = CreateHeader()

        self.header_label, self.line_top_label = header.create_header(
            self.status_page_frame,
            header_title_bg=self.header_title_bg,
            line_top_img=self.line_top_img,
            text=self.ui_data["header_label"],
        )

    def create_action_status(self):
        self.action_label = CTkLabel(
            self.status_page_frame,
            fg_color="#2B2631",
            text_color="#FFFFFF",
            text="",
            image=None,
            compound="right",
            font=("Arial", 18, "bold"),
        )
        self.action_label.grid(row=2, column=0, padx=60, pady=(14, 2), sticky="NSEW")

    def create_progress_bar(self):
        self.progress_bar = CTkProgressBar(
            self.status_page_frame,
            width=650,
            orientation="horizontal",
            height=24,
            fg_color="#666666",
            progress_color="#9747FF",
        )
        self.progress_bar.grid(
            row=3, column=0, padx=80, pady=10, sticky="NSEW"
        )  # This widget centering the frame. :d
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
        self.finish_button = self.navigation_button.create_navigation_button(
            parent,
            "finish_button",
            path.join(ASSETS_PATH, FINISH_ICON),
            lambda: InfoModals(self, "Attention"),
            padding_x=(10, 20),
            side="right",
            img_side="right",
        )

        self.back_button = self.navigation_button.create_navigation_button(
            parent,
            "back_button",
            path.join(ASSETS_PATH, BACK_ICON),
            padding_x=(5, 5),
            side="right",
            command=lambda: self.controller.show_frame(
                f"{self.come_from_which_page}_page"
            ),
            state="Normal",
        )
        self.exit_button = self.navigation_button.create_navigation_button(
            parent,
            "exit_button",
            path.join(ASSETS_PATH, EXIT_ICON),
            lambda: InfoModals(self, "Exit"),
            padding_x=(20, 10),
            side="left",
        )

    def create_os_info(self, parent):
        os_frame = CTkFrame(parent, corner_radius=12, fg_color="white")
        os_frame.grid(row=0, column=0, padx=20, sticky="W")

        os_label = CTkLabel(
            os_frame,
            text=f"{self.os_values['os_name']} ",
            text_color=self.os_values["os_color"],
            font=("Arial", 20, "bold"),
            image=self.os_icon_image,
            compound="right",
        )
        os_label.pack(padx=10, pady=10, side="right")

    def update_text_2(self):
        update_text = self.ui_data["update_text"]
        if self.come_from_which_page == "install":
            self.action_label.configure(
                text=f"{update_text["install"]}  ",
                image=self.check_icon,
                compound="right",
            )
        elif self.come_from_which_page == "remove":
            self.action_label.configure(
                text=f"{update_text["remove"]}  ",
                image=self.check_icon,
                compound="right",
            )

    def update_parameters(self, **kwargs):
        self.come_from_which_page = kwargs.get("come_from_which_page")
        self.profile_folder = kwargs.get("profile_folder")
        self.application_folder = kwargs.get("application_folder")
        self.theme_dir = kwargs.get("theme_dir")
        self.custom_script_loader = kwargs.get("custom_script_loader")
        self.selected_theme_data = kwargs.get("selected_theme_data")
        self.chrome_folder = path.join(self.profile_folder, "chrome")

        # Decide which function to call based on the page source
        if self.come_from_which_page == "install":
            self.install()
        elif self.come_from_which_page == "remove":
            self.remove()

        self.thread_manager.start_thread(
            self.file_actions.execute_operations,
            self.progress_bar,
            self.output_entry,
            on_finish=self.update_text_2,
        )

    def install(self):
        # Handles the installation process
        install = self.ui_data["install"]
        self.action_label.configure(text=f"{install}  ")
        user_js_src = path.join(self.CACHE_PATH, "fx-autoconfig", "user.js")

        if path.exists(user_js_src):
            self.file_actions.copy_file(user_js_src, self.profile_folder)

        if self.custom_script_loader:
            self.file_actions.copy_file(
                path.join(self.CACHE_PATH, "fx-autoconfig", "config.js"),
                self.application_folder,
            )
            self.file_actions.copy_file(
                path.join(self.CACHE_PATH, "fx-autoconfig", "mozilla.cfg"),
                self.application_folder,
            )
            self.file_actions.copy_file(
                path.join(self.CACHE_PATH, "fx-autoconfig", "config-prefs.js"),
                path.join(self.application_folder, "defaults", "pref"),
            )
            self.file_actions.copy_file(
                path.join(self.CACHE_PATH, "fx-autoconfig", "local-settings.js"),
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
        with open(theme_data_path, "w") as json_file:
            dump(self.selected_theme_data, json_file, indent=4)

    def remove(self):
        remove = self.ui_data["remove"]
        # Handles the removal process
        self.action_label.configure(text=f"{remove}  ")

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
