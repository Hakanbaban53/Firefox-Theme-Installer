from json import load
from os import path
from tkinter import BooleanVar
from customtkinter import (
    CTkFrame,
    CTkImage,
    CTkLabel,
    CTkEntry,
    CTkCheckBox,
)
from PIL import Image

from components.create_detect_installed_theme import DetectInstalledTheme
from components.create_header import CreateHeader
from components.create_navigation_button import NavigationButton
from modals.info_modals import InfoModals
from functions.get_os_properties import OSProperties
from functions.get_folder_locations import GetFolderLocations
from functions.special_input_functions import SpecialInputFunc


class RemovePage(CTkFrame):
    def __init__(self, parent, controller, base_dir):
        super().__init__(parent)
        self.controller = controller
        self.base_dir = base_dir
        
        self.config_data = self.load_json_data(
            path.join(base_dir, "data", "pages", "remove_page_data.json")
        )

        # Set the paths
        self.ASSETS_PATH = path.join(
            base_dir, self.config_data["data_paths"]["ASSETS_PATH"]
        )
        self.NAVIGATION_BUTTON_DATA_PATH = path.join(
            base_dir, self.config_data["data_paths"]["NAVIGATION_BUTTON_DATA_PATH"]
        )
        self.OS_PROPERTIES_PATH = path.join(
            base_dir, self.config_data["data_paths"]["OS_PROPERTIES_PATH"]
        )
        self.INPUTS_DATA_PATH = path.join(
            base_dir, self.config_data["data_paths"]["INPUTS_DATA_PATH"]
        )
        self.cache_dir = path.join(self.base_dir, "image_cache")

        self.navigation_button_data = self.load_json_data(
            self.NAVIGATION_BUTTON_DATA_PATH
        )
        self.button_data = self.navigation_button_data["navigation_buttons"]

        self.header = CreateHeader()
        self.os_values = OSProperties(self.OS_PROPERTIES_PATH).get_values()
        self.input_values = OSProperties(self.OS_PROPERTIES_PATH).get_locations()
        self.navigation_button = NavigationButton(self.button_data)
        self.profile_folder_location = GetFolderLocations(
            self.os_values
        ).get_profile_folder()


        self.chrome_folder = path.join(self.profile_folder_location, "chrome")

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
        # Load icons and images based on JSON paths
        icons = self.config_data["icons"]
        self.attention_icon = CTkImage(
            light_image=Image.open(
                path.join(self.ASSETS_PATH, icons["attention_icon"])
            ),
            dark_image=Image.open(path.join(self.ASSETS_PATH, icons["attention_icon"])),
            size=(24, 24),
        )
        self.header_title_bg = CTkImage(
            light_image=Image.open(
                path.join(self.ASSETS_PATH, icons["header_title_bg"])
            ),
            dark_image=Image.open(
                path.join(self.ASSETS_PATH, icons["header_title_bg"])
            ),
            size=(300, 64),
        )
        self.line_top_img = CTkImage(
            light_image=Image.open(path.join(self.ASSETS_PATH, icons["line_top_img"])),
            dark_image=Image.open(path.join(self.ASSETS_PATH, icons["line_top_img"])),
            size=(650, 6),
        )
        self.os_icon_image = CTkImage(
            light_image=Image.open(
                path.join(
                    self.ASSETS_PATH, f"icons/{self.os_values['os_name'].lower()}.png"
                )
            ),
            dark_image=Image.open(
                path.join(
                    self.ASSETS_PATH, f"icons/{self.os_values['os_name'].lower()}.png"
                )
            ),
            size=(20, 24),
        )

        self.theme_detected_icon = CTkImage(
            light_image=Image.open(
                path.join(self.ASSETS_PATH, icons["theme_detected_icon"])
            ),
            dark_image=Image.open(
                path.join(self.ASSETS_PATH, icons["theme_detected_icon"])
            ),
            size=(24, 32),
        )

    def create_header(self):
        header_data = self.config_data["header_data"]

        self.header.create_header(
            self.remove_page_frame,
            header_title_bg=self.header_title_bg,
            line_top_img=self.line_top_img,
            text=header_data["text"],
        )

    def create_inputs_and_checkboxes(self):
        inputs_data = self.load_json_data(self.INPUTS_DATA_PATH)
        inputs_data = inputs_data["create_inputs_and_checkboxes"]

        inputs_checkboxes_frame = CTkFrame(
            self.remove_page_frame,
            width=inputs_data["inputs_checkboxes_frame"]["width"],
            height=inputs_data["inputs_checkboxes_frame"]["height"],
            corner_radius=inputs_data["inputs_checkboxes_frame"]["corner_radius"],
            fg_color=inputs_data["inputs_checkboxes_frame"]["fg_color"],
        )
        inputs_checkboxes_frame.grid(
            row=inputs_data["inputs_checkboxes_frame"]["grid_data"]["row"],
            column=inputs_data["inputs_checkboxes_frame"]["grid_data"]["column"],
            columnspan=inputs_data["inputs_checkboxes_frame"]["grid_data"][
                "columnspan"
            ],
            padx=inputs_data["inputs_checkboxes_frame"]["grid_data"]["padx"],
            pady=inputs_data["inputs_checkboxes_frame"]["grid_data"]["pady"],
            sticky=inputs_data["inputs_checkboxes_frame"]["grid_data"]["sticky"],
        )

        self.create_input_and_checkbox_widgets(
            inputs_checkboxes_frame, inputs_data["create_input_and_checkbox_widgets"]
        )

    def create_input_and_checkbox_widgets(self, frame, inputs_data):
        # Profile Name
        self.profile_folder_label = CTkLabel(
            master=frame,
            text=inputs_data["profile_folder_label"]["text"],
            text_color=inputs_data["profile_folder_label"]["text_color"],
            font=eval(inputs_data["profile_folder_label"]["font"]),
        )
        self.profile_folder_label.grid(
            row=inputs_data["profile_folder_label"]["grid_data"]["row"],
            column=inputs_data["profile_folder_label"]["grid_data"]["column"],
            padx=inputs_data["profile_folder_label"]["grid_data"]["padx"],
            pady=inputs_data["profile_folder_label"]["grid_data"]["pady"],
            sticky=inputs_data["profile_folder_label"]["grid_data"]["sticky"],
        )

        self.profile_folder_entry = CTkEntry(
            master=frame,
            width=inputs_data["profile_folder_entry"]["width"],
            height=inputs_data["profile_folder_entry"]["height"],
            fg_color=inputs_data["profile_folder_entry"]["fg_color"],
            text_color=inputs_data["profile_folder_entry"]["text_color"],
            corner_radius=inputs_data["profile_folder_entry"]["corner_radius"],
            border_width=inputs_data["profile_folder_entry"]["border_width"],
            bg_color=inputs_data["profile_folder_entry"]["bg_color"],
            border_color=inputs_data["profile_folder_entry"]["border_color"],
            placeholder_text=self.profile_folder_location,
        )
        self.profile_folder_entry.grid(
            row=inputs_data["profile_folder_entry"]["grid_data"]["row"],
            column=inputs_data["profile_folder_entry"]["grid_data"]["column"],
            padx=inputs_data["profile_folder_entry"]["grid_data"]["padx"],
            pady=inputs_data["profile_folder_entry"]["grid_data"]["pady"],
            sticky=inputs_data["profile_folder_entry"]["grid_data"]["sticky"],

        )

        # Application Folder
        self.application_folder_label = CTkLabel(
            master=frame,
            text=inputs_data["application_folder_label"]["text"],
            text_color=inputs_data["application_folder_label"]["text_color"],
            font=eval(inputs_data["application_folder_label"]["font"]),
        )
        self.application_folder_label.grid(
            row=inputs_data["application_folder_label"]["grid_data"]["row"],
            column=inputs_data["application_folder_label"]["grid_data"]["column"],
            padx=inputs_data["application_folder_label"]["grid_data"]["padx"],
            pady=inputs_data["application_folder_label"]["grid_data"]["pady"],
            sticky=inputs_data["application_folder_label"]["grid_data"]["sticky"],
        )

        self.application_folder_entry = CTkEntry(
            master=frame,
            width=inputs_data["application_folder_entry"]["width"],
            height=inputs_data["application_folder_entry"]["height"],
            fg_color=inputs_data["application_folder_entry"]["fg_color"],
            text_color=inputs_data["application_folder_entry"]["text_color"],
            corner_radius=inputs_data["application_folder_entry"]["corner_radius"],
            border_width=inputs_data["application_folder_entry"]["border_width"],
            bg_color=inputs_data["application_folder_entry"]["bg_color"],
            border_color=inputs_data["application_folder_entry"]["border_color"],
            placeholder_text=self.input_values["application_folder"],
        )
        self.application_folder_entry.grid(
            row=inputs_data["application_folder_entry"]["grid_data"]["row"],
            column=inputs_data["application_folder_entry"]["grid_data"]["column"],
            padx=inputs_data["application_folder_entry"]["grid_data"]["padx"],
            pady=inputs_data["application_folder_entry"]["grid_data"]["pady"],
            sticky=inputs_data["application_folder_entry"]["grid_data"]["sticky"],
        )

        self.key_bind(self.profile_folder_entry)
        self.key_bind(self.application_folder_entry)

        self.check_var = BooleanVar(value=False)
        edit_checkbox = CTkCheckBox(
            master=frame,
            text=inputs_data["edit_checkbox"]["text"],
            fg_color=inputs_data["edit_checkbox"]["fg_color"],
            hover_color=inputs_data["edit_checkbox"]["hover_color"],
            text_color=inputs_data["edit_checkbox"]["text_color"],
            bg_color=inputs_data["edit_checkbox"]["bg_color"],
            font=eval(inputs_data["edit_checkbox"]["font"]),
            border_color=inputs_data["edit_checkbox"]["border_color"],
            command=self.checkbox_event,
            variable=self.check_var,
            onvalue=True,
            offvalue=False,
        )
        edit_checkbox.grid(
            row=inputs_data["edit_checkbox"]["grid_data"]["row"],
            column=inputs_data["edit_checkbox"]["grid_data"]["column"],
            padx=inputs_data["edit_checkbox"]["grid_data"]["padx"],
            pady=inputs_data["edit_checkbox"]["grid_data"]["pady"],
            sticky=inputs_data["edit_checkbox"]["grid_data"]["sticky"],
        )
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
            row=4, column=0, columnspan=2, padx=(10, 4), pady=10
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
            cache_dir=self.cache_dir,
            base_dir=self.base_dir
        )
        self.detect_installed_theme_component.create_installed_themes(preview_and_check_installed_theme_frame)
        
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
            "Remove",
            path.join(self.ASSETS_PATH, "icons/remove_icon.png"),
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
            "Back",
            path.join(self.ASSETS_PATH, "icons/back_icon.png"),
            padding_x=(5, 5),
            side="right",
            command=lambda: self.controller.show_frame("home_page"),
        )
        self.navigation_button.create_navigation_button(
            parent,
            "Exit",
            path.join(self.ASSETS_PATH, "icons/exit_icon.png"),
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
        update_button_and_frame_data = self.config_data["update_button_and_frame"]
        if SpecialInputFunc().update_invalid_entries_display():
            self.remove_button.configure(state="normal")
            self.invalid_entry_frame.grid_remove()
        else:
            self.remove_button.configure(state="disabled")
            self.invalid_entries_text.configure(
                text=f"  {len(SpecialInputFunc().return_invalid_entries())}" + update_button_and_frame_data["invalid_entries_text"]["text"]
            )
            self.invalid_entry_frame.grid()

    def checkbox_event(self):
        if self.check_var.get():
            self.application_folder_entry.configure(state="normal")
            self.profile_folder_entry.configure(state="normal")
        else:
            self.application_folder_entry.configure(state="disabled")
            self.profile_folder_entry.configure(state="disabled")

    def update_parameters(self, **kwargs):
        pass
