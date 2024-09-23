from os import path
from tkinter import Frame
from customtkinter import (
    CTkFrame,
    CTkLabel,
    CTkButton,
)

from components.create_header import CreateHeader
from components.create_inputs_and_checkboxes import InputsAndCheckboxes
from components.create_navigation_button import NavigationButton
from components.create_detect_installed_theme import DetectInstalledTheme
from installer_core.component_tools.preview_theme import PreviewTheme
from installer_core.component_tools.special_input_functions import SpecialInputFunc
from installer_core.component_tools.thread_manager import ThreadManager
from installer_core.data_tools.get_os_properties import OSProperties
from installer_core.data_tools.image_loader import ImageLoader
from installer_core.data_tools.load_json_data import LoadJsonData
from installer_core.file_utils.get_folder_locations import GetFolderLocations
from modals.info_modals import InfoModals


class InstallPage(Frame):
    def __init__(self, parent, controller, base_dir, app_language):
        super().__init__(parent)
        UI_DATA_PATH = path.join(
            base_dir,
            "data",
            "pages",
            "install_page",
            "language",
            f"{app_language}.json",
        )
        PATHS = path.join(base_dir, "data", "global", "paths.json")
        ICONS = path.join(base_dir, "data", "global", "icons.json")
        load_json_data = LoadJsonData()
        self.ui_data = load_json_data.load_json_data(UI_DATA_PATH)
        self.paths = load_json_data.load_json_data(PATHS)
        self.icons = load_json_data.load_json_data(ICONS)

        self.app_language = app_language
        self.controller = controller
        self.base_dir = base_dir
        self.theme_dir = None
        self.theme_data = None

        # Set the paths
        self.ASSETS_PATH = path.join(base_dir, self.paths["ASSETS_PATH"])

        self.os_properties = OSProperties(base_dir)
        self.input_values = self.os_properties.get_locations()
        self.os_values = self.os_properties.get_values()

        self.header = CreateHeader()

        self.navigation_button = NavigationButton(
            base_dir=base_dir,
            app_language=app_language,
        )
        self.profile_folder_location = GetFolderLocations(
            self.os_values
        ).get_profile_folder()
        self.thread_manager = ThreadManager()

        self.chrome_folder = path.join(self.profile_folder_location, "chrome")

        # Initialize ImageLoader with the asset path and OS name
        self.image_loader = ImageLoader(self.ASSETS_PATH, self.os_values["os_name"])

        self.configure_layout()
        self.create_widgets()

    def configure_layout(self):
        self.install_page_frame = CTkFrame(
            self,
            fg_color="#2B2631",
        )
        self.install_page_frame.grid(row=0, column=1, sticky="SW")
        self.install_page_frame.columnconfigure(0, weight=1)

    def create_widgets(self):
        self.create_images()
        self.create_header()
        self.create_inputs_and_checkboxes()
        self.create_invalid_entry_frame()
        self.create_preview_and_check_installed_theme()
        self.create_bottom_widgets()
        self.update_button_and_frame()
        self.checkbox_event()


    def create_images(self):
        # Load icons and images using the ImageLoader
        self.attention_icon = self.image_loader.load_attention_icon(self.icons)
        self.header_title_bg = self.image_loader.load_header_title_bg(self.icons)
        self.line_top_img = self.image_loader.load_line_top_img(self.icons)
        self.os_icon_image = self.image_loader.load_os_icon_image()
        self.preview_icon = self.image_loader.load_preview_icon(self.icons)
        self.theme_detected_icon = self.image_loader.load_theme_detected_icon(
            self.icons
        )

    def create_header(self):
        self.header.create_header(
            self.install_page_frame,
            header_title_bg=self.header_title_bg,
            line_top_img=self.line_top_img,
            text=self.ui_data["header_label"],
        )

    def create_inputs_and_checkboxes(self):
        self.inputs_and_checkboxes = InputsAndCheckboxes(
            base_dir=self.base_dir,
            app_language=self.app_language,
            frame=self.install_page_frame,
        )

        self.profile_folder_entry = (
            self.inputs_and_checkboxes.create_profile_folder_widget(
                self.profile_folder_location
            )
        )
        self.application_folder_entry = (
            self.inputs_and_checkboxes.create_application_folder_widget(
                self.input_values["application_folder"]
            )
        )

        self.check_var = self.inputs_and_checkboxes.create_edit_checkbox(
            self.checkbox_event


        )
        self.CSL = self.inputs_and_checkboxes.create_CSL_checkbox()

        self.key_bind(self.application_folder_entry)  # Bind keys to the entry
        self.key_bind(self.profile_folder_entry)

    def create_preview_and_check_installed_theme(self):
        preview_and_check_installed_theme_frame = CTkFrame(
            self.install_page_frame,
            fg_color="#2B2631",
        )
        preview_and_check_installed_theme_frame.grid(
            row=4, column=0, padx=(10, 4), pady=10
        )

        self.detect_installed_theme_component = DetectInstalledTheme(
            self,
            chrome_folder=self.chrome_folder,
            theme_detected_icon=self.theme_detected_icon,
            base_dir=self.base_dir,
            app_language=self.app_language,
        )
        self.detect_installed_theme_component.create_installed_themes(
            preview_and_check_installed_theme_frame
        )

        self.create_preview_theme(preview_and_check_installed_theme_frame)

        self.detect_installed_theme_component.detect_installed_theme()

    def create_preview_theme(self, preview_and_check_installed_theme_frame):
        preview_theme_data = self.ui_data["create_preview_theme"]
        preview_frame = CTkFrame(
            preview_and_check_installed_theme_frame,
            width=440,
            height=60,
            corner_radius=12,
            fg_color="#FFFFFF",
        )
        preview_frame.grid(
            row=0,
            column=1,
            padx=40,
            pady=(20, 30),
            sticky="",
        )

        preview_label = CTkLabel(
            preview_frame,
            text=preview_theme_data["preview_label"],
            text_color="#000000",
            font=("Inter", 18, "bold"),
        )
        preview_label.pack(
            padx=10,
            pady=10,
            side="top",
        )

        self.preview_button = CTkButton(
            preview_frame,
            text=preview_theme_data["preview_button"],
            height=42,
            fg_color="#D9D9D9",
            hover_color="#EEEEEE",
            corner_radius=12,
            font=("Inter", 16, "bold"),
            text_color="#000000",
            image=self.preview_icon,
            command=self.start_theme_preview_thread,
        )
        self.preview_button.pack(
            padx=10,
            pady=10,
        )

    def create_invalid_entry_frame(self):
        invalid_entry_frame_data = self.ui_data["create_invalid_entry_frame"]
        self.invalid_entry_frame = CTkFrame(
            self.install_page_frame,
            width=440,
            height=54,
            corner_radius=12,
            fg_color="white",
        )
        self.invalid_entry_frame.grid(
            row=5,
            column=0,
            padx=(10, 4),
            pady=10,
        )

        self.invalid_entries_text = CTkLabel(
            self.invalid_entry_frame,
            text=invalid_entry_frame_data["invalid_entries_text"],
            text_color="#F04141",
            font=("Inter", 16, "bold"),
            compound="left",
            image=self.attention_icon,
        )
        self.invalid_entries_text.pack(
            padx=10,
            pady=10,
        )

    def create_bottom_widgets(self):
        bottom_frame = CTkFrame(self, fg_color="#2B2631")
        bottom_frame.place(x=190.0, y=600.0)

        navigation_frame = CTkFrame(
            bottom_frame,
            width=440,
            height=54,
            corner_radius=12,
            border_width=4,
            bg_color="#2B2631",
            fg_color="white",
            border_color="#F89F24",
        )
        navigation_frame.grid(row=0, column=1, sticky="E")

        self.create_navigation_buttons(navigation_frame)
        self.create_os_info(bottom_frame)

    def create_navigation_buttons(self, parent):
        self.install_button = self.navigation_button.create_navigation_button(
            parent,
            "install_button",
            path.join(self.ASSETS_PATH, "icons/install.png"),
            command=lambda: self.controller.show_frame(
                "status_page",
                come_from_which_page="install",
                profile_folder=SpecialInputFunc().get_variables(
                    self.profile_folder_entry
                ),
                application_folder=SpecialInputFunc().get_variables(
                    self.application_folder_entry
                ),
                base_dir=self.base_dir,
                theme_dir=self.theme_dir,
                custom_script_loader=self.CSL.get(),
                selected_theme_data=self.selected_theme_data,
            ),
            padding_x=(10, 20),
            side="right",
            img_side="right",
        )

        self.back_button = self.navigation_button.create_navigation_button(
            parent,
            "back_button",
            path.join(self.ASSETS_PATH, "icons/back.png"),
            padding_x=(5, 5),
            side="right",
            command=lambda: self.controller.show_frame("home_page"),
        )
        self.navigation_button.create_navigation_button(
            parent,
            "exit_button",
            path.join(self.ASSETS_PATH, "icons/exit.png"),
            lambda: InfoModals(self, self.base_dir, "Exit", self.app_language),
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

    def start_theme_preview_thread(self):
        # Disable the install and preview buttons
        start_theme_preview_thread_data = self.ui_data["start_theme_preview_thread"]
        self.install_button.configure(state="disabled")
        self.preview_button.configure(
            state="disabled",
            text=start_theme_preview_thread_data["preview_button"],
            width=150,
        )

        # Start the preview in a new thread and re-enable buttons when done
        self.thread_manager.start_thread(
            target=self.preview_theme, on_finish=self.on_preview_complete
        )

    def preview_theme(self):
        profile_folder = SpecialInputFunc().get_variables(self.profile_folder_entry)
        application_folder = SpecialInputFunc().get_variables(
            self.application_folder_entry
        )

        self.preview = PreviewTheme(
            self.base_dir,
            self.theme_dir,
            self.CSL.get(),
            profile_folder,
            application_folder,
        )
        self.preview.run_firefox()

    def on_preview_complete(self):
        # Re-enable the install and preview buttons when Firefox is closed
        on_preview_complete_data = self.ui_data["on_preview_complete"]
        self.install_button.configure(state="normal")
        self.preview_button.configure(
            text=on_preview_complete_data["preview_button"],
            state="normal",
            width=150,
        )

    def key_bind(self, entry_widget, file_extension=None):
        entry_widget.bind(
            "<KeyRelease>",
            lambda event: self.on_key_release(entry_widget, file_extension),
        )
        entry_widget.bind(
            "<FocusOut>",
            lambda event: self.on_key_release(entry_widget, file_extension),
        )

    def on_key_release(self, entry_widget, file_extension):
        SpecialInputFunc().validate_file_location(entry_widget, file_extension)
        self.update_button_and_frame()

    def update_button_and_frame(self):
        update_button_and_frame_data = self.ui_data["update_button_and_frame"]
        if SpecialInputFunc().update_invalid_entries_display():
            self.install_button.configure(state="normal")
            self.invalid_entry_frame.lower()
        else:
            self.install_button.configure(state="disabled")
            self.invalid_entries_text.configure(
                text=f"  {len(SpecialInputFunc().return_invalid_entries())}"
                + update_button_and_frame_data["invalid_entries_text"]
            )
            self.invalid_entry_frame.lift()

    def checkbox_event(self):
        if self.check_var.get():
            self.application_folder_entry.configure(state="normal")
            self.profile_folder_entry.configure(state="normal")
        else:
            self.application_folder_entry.configure(state="disabled")
            self.profile_folder_entry.configure(state="disabled")

    def update_parameters(self, **kwargs):
        self.theme_dir = kwargs.get("theme_dir")
        self.selected_theme_data = kwargs.get("selected_theme_data")
