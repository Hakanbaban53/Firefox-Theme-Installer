from os import path
from tkinter import Frame
from customtkinter import (
    CTkFrame,
    CTkLabel,
)

from components.create_detect_installed_theme import DetectInstalledTheme
from components.create_header import CreateHeader
from components.create_inputs_and_checkboxes import InputsAndCheckboxes
from components.create_navigation_button import NavigationButton
from installer_core.component_tools.special_input_functions import SpecialInputFunc
from installer_core.data_tools.get_os_properties import OSProperties
from installer_core.data_tools.image_loader import ImageLoader
from installer_core.data_tools.load_json_data import LoadJsonData
from installer_core.data_tools.get_folder_locations import GetFolderLocations
from modals.info_modals import InfoModals


class RemovePage(Frame):
    def __init__(self, parent, controller, base_dir, app_language):
        super().__init__(parent)
        # Load the UI data from the JSON file
        UI_DATA_PATH = path.join(
            base_dir, "language", "pages", "remove_page", f"{app_language}.json"
        )
        PATHS = path.join(base_dir, "data", "local", "global", "paths.json")
        ICONS = path.join(base_dir, "data", "local", "global", "icons.json")
        load_json_data = LoadJsonData()
        self.ui_data = load_json_data.load_json_data(UI_DATA_PATH)
        self.paths = load_json_data.load_json_data(PATHS)
        self.icons = load_json_data.load_json_data(ICONS)

        self.app_language = app_language
        self.controller = controller
        self.base_dir = base_dir

        # Set the paths
        self.ASSETS_PATH = path.join(base_dir, self.paths["ASSETS_PATH"])

        self.os_properties = OSProperties(base_dir)
        self.input_values = self.os_properties.get_locations()
        self.os_values = self.os_properties.get_values()

        self.header = CreateHeader()

        self.navigation_button = NavigationButton(
            base_dir=base_dir, app_language=app_language
        )

        self.profile_folder_location = GetFolderLocations(
            self.os_values
        ).get_profile_folder()

        self.chrome_folder = path.join(self.profile_folder_location, "chrome")

        # Initialize ImageLoader with the asset path and OS name
        self.image_loader = ImageLoader(self.ASSETS_PATH, self.os_values["os_name"])

        self.configure_layout()
        self.create_widgets()

    def configure_layout(self):
        self.remove_page_frame = CTkFrame(
            self,
            fg_color="#2B2631",
        )
        self.remove_page_frame.grid(row=0, column=1, sticky="SW")
        self.remove_page_frame.columnconfigure(0, weight=1)

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

        self.header_title_bg = self.image_loader.load_header_title_bg(
            self.icons, size=(320, 80)  # Different size specified here
        )

        self.line_top_img = self.image_loader.load_line_top_img(self.icons)
        self.os_icon_image = self.image_loader.load_os_icon_image()
        self.theme_detected_icon = self.image_loader.load_theme_detected_icon(
            self.icons
        )

    def create_header(self):
        self.header.create_header(
            self.remove_page_frame,
            header_title_bg=self.header_title_bg,
            line_top_img=self.line_top_img,
            text=self.ui_data["header_label"],
        )

    def create_inputs_and_checkboxes(self):
        self.inputs_and_checkboxes = InputsAndCheckboxes(
            base_dir=self.base_dir,
            app_language=self.app_language,
            frame=self.remove_page_frame,
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

        self.key_bind(self.application_folder_entry)  # Bind keys to the entry
        self.key_bind(self.profile_folder_entry)

    def create_invalid_entry_frame(self):
        self.invalid_entry_frame = CTkFrame(
            self.remove_page_frame,
            width=440,
            height=54,
            corner_radius=12,
            bg_color="#2B2631",
            fg_color="white",
        )
        self.invalid_entry_frame.grid(
            row=5, column=0, columnspan=2, padx=(10, 4), pady=10
        )

        self.invalid_entries_text = CTkLabel(
            self.invalid_entry_frame,
            text="",
            text_color="#f04141",
            font=("Arial", 16, "bold"),
            image=self.attention_icon,
            compound="left",
        )
        self.invalid_entries_text.pack(padx=10, pady=10)

    def create_preview_and_check_installed_theme(self):
        preview_and_check_installed_theme_frame = CTkFrame(
            self.remove_page_frame,
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

        self.detect_installed_theme_component.detect_installed_theme()

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
        self.remove_button = self.navigation_button.create_navigation_button(
            parent,
            "remove_button",
            path.join(self.ASSETS_PATH, "remove.png"),
            lambda: self.controller.show_frame(
                "status_page",
                come_from_which_page="remove",
                profile_folder=SpecialInputFunc().get_variables(
                    self.profile_folder_entry
                ),
                application_folder=SpecialInputFunc().get_variables(
                    self.application_folder_entry
                ),
                base_dir=self.base_dir,
            ),
            padding_x=(10, 20),
            side="right",
            img_side="right",
        )

        self.back_button = self.navigation_button.create_navigation_button(
            parent,
            "back_button",
            path.join(self.ASSETS_PATH, "back.png"),
            padding_x=(5, 5),
            side="right",
            command=lambda: self.controller.show_frame("home_page"),
        )
        self.navigation_button.create_navigation_button(
            parent,
            "exit_button",
            path.join(self.ASSETS_PATH, "exit.png"),
            lambda: InfoModals(
                self, self.base_dir, "Exit", app_language=self.app_language
            ),
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

    def key_bind(self, entry_widget):
        entry_widget.bind(
            "<KeyRelease>",
            lambda event: self.on_key_release(entry_widget),
        )
        entry_widget.bind(
            "<FocusOut>",
            lambda event: self.on_key_release(entry_widget),
        )

    def on_key_release(self, entry_widget):
        SpecialInputFunc().validate_file_location(entry_widget)
        self.update_button_and_frame()

    def update_button_and_frame(self):
        update_button_and_frame_data = self.ui_data["update_button_and_frame"]
        if SpecialInputFunc().update_invalid_entries_display():
            self.remove_button.configure(state="normal")
            self.invalid_entry_frame.lower()
        else:
            self.remove_button.configure(state="disabled")
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
        pass
