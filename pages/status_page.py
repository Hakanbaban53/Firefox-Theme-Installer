from os import listdir, makedirs, path
from json import dump
from customtkinter import (
    CTkFrame,
    CTkLabel,
    CTkFont,
    CTkTextbox,
    CTkProgressBar,
)
from tkinter import Frame

from components.create_header import CreateHeader
from components.create_navigation_button import NavigationButton
from installer_core.component_tools.thread_managing import ThreadManager
from installer_core.data_tools.get_os_properties import OSProperties
from installer_core.data_tools.image_loader import ImageLoader
from installer_core.data_tools.load_json_data import LoadJsonData
from installer_core.file_utils.file_actions import FileActions
from modals.info_modals import InfoModals

class StatusPage(Frame):
    def __init__(self, parent, controller, base_dir):
        super().__init__(parent)
        # Load the UI data from the JSON file
        UI_DATA_PATH = path.join(base_dir, "data", "pages", "status_page_data.json")
        PATHS = path.join(base_dir, "data", "global", "paths.json")
        ICONS = path.join(base_dir, "data", "global", "icons.json")
        load_json_data = LoadJsonData()
        self.ui_data = load_json_data.load_json_data(UI_DATA_PATH)
        self.paths = load_json_data.load_json_data(PATHS)
        self.icons = load_json_data.load_json_data(ICONS)

        self.thread_manager = ThreadManager()

        self.controller = controller
        self.base_dir = base_dir

        # Set the paths
        self.ASSETS_PATH = path.join(
            base_dir, self.paths["ASSETS_PATH"]
        )

        self.os_properties = OSProperties(base_dir)
        self.os_values = self.os_properties.get_values()

        self.CACHE_PATH = self.os_properties.get_cache_location()

        
        # Get navigation button data
        NAVIGATION_BUTTON_DATA_PATH = path.join(
            base_dir, self.paths["NAVIGATION_BUTTON_DATA_PATH"]
        )
        self.navigation_button_data = load_json_data.load_json_data(
            NAVIGATION_BUTTON_DATA_PATH
        )
        self.button_data = self.navigation_button_data["navigation_buttons"]

        self.header = CreateHeader()
        self.come_from_which_page = None

        self.navigation_button = NavigationButton(self.button_data)
        self.file_actions = FileActions(self.os_values["os_name"])
        self.image_loader = ImageLoader(self.ASSETS_PATH, self.os_values['os_name'])


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
        self.check_icon = self.image_loader.load_check_icon(self.icons)
        self.os_icon_image = self.image_loader.load_os_icon_image()
        self.header_title_bg = self.image_loader.load_header_title_bg(
            self.icons,
        )
        self.line_top_img = self.image_loader.load_line_top_img(self.icons)


    def create_header(self):
        header_data = self.ui_data["header_data"]

        self.header.create_header(
            self.status_page_frame,
            header_title_bg=self.header_title_bg,
            line_top_img=self.line_top_img,
            text=header_data["text"],
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
        self.progress_bar.grid(row=3, column=0, padx=80, pady=10, sticky="NSEW") # This widget centering the frame. :d
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
            path.join(self.ASSETS_PATH, "icons/finish.png"),
            lambda: InfoModals(self, self.base_dir, "Attention"),
            padding_x=(10, 20),
            side="right",
            img_side="right",
        )

        self.back_button = self.navigation_button.create_navigation_button(
            parent,
            "Back",
            path.join(self.ASSETS_PATH, "icons/back.png"),
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
            path.join(self.ASSETS_PATH, "icons/exit.png"),
            lambda: InfoModals(self, self.base_dir, "Exit"),
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

    def update_text(self):
        if self.come_from_which_page == "install":
            self.action_label.configure(
                text="Installed  ",
                image=self.check_icon,
                compound="right",
            )
        elif self.come_from_which_page == "remove":
            self.action_label.configure(
                text="Removed  ",
                image=self.check_icon,
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

        # Decide which function to call based on the page source
        if self.come_from_which_page == "install":
            self.install()
        elif self.come_from_which_page == "remove":
            self.remove()

        self.start_thread(
            target=self.file_actions.execute_operations(self.progress_bar, self.output_entry)
        )

    def start_thread(self, target, *args):
        """Start a new thread for the specified target function with args."""
        self.thread_manager.start_thread(target=target, *args)
        self.check_thread()

    def check_thread(self):
        """Check if the thread is finished and update the UI accordingly."""
        if self.thread_manager.are_threads_alive():
            self.after(100, self.check_thread)
        else:
            # Call a thread-safe method to update the UI
            self.after(0, self.update_text)

    def install(self):
        # Handles the installation process
        self.action_label.configure(text="Installing...")
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

        # # For Testing
        # self.back_button.configure(
        #     command=lambda: self.controller.show_frame(
        #         f"{self.come_from_which_page}_page",
        #         status="normal"
        #     ),
        # )
