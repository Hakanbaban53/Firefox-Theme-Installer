from os import path
from pathlib import Path
from tkinter import BooleanVar
from customtkinter import (
    CTkFrame,
    CTkLabel,
    CTkEntry,
    CTkCheckBox,
    CTkButton,
)

from components.create_header import CreateHeader
from components.create_navigation_button import NavigationButton
from components.create_detect_installed_theme import DetectInstalledTheme
from installer_core.component_tools.preview_theme import PreviewTheme
from installer_core.component_tools.special_input_functions import SpecialInputFunc
from installer_core.component_tools.thread_managing import ThreadManager
from installer_core.data_tools.get_os_properties import OSProperties
from installer_core.data_tools.image_loader import ImageLoader
from installer_core.data_tools.load_json_data import LoadJsonData
from installer_core.file_utils.get_folder_locations import GetFolderLocations
from modals.info_modals import InfoModals

class InstallPage(CTkFrame):
    def __init__(self, parent, controller, base_dir):
        super().__init__(parent)
        # Load the UI data from the JSON file
        UI_DATA_PATH = path.join(base_dir, "data", "pages", "install_page_data.json")
        load_json_data = LoadJsonData()
        self.ui_data = load_json_data.load_json_data(UI_DATA_PATH)

        self.controller = controller
        self.base_dir = base_dir
        self.theme_dir = None
        self.theme_data = None

        # Set the paths
        self.ASSETS_PATH = path.join(
            base_dir, self.ui_data["data_paths"]["ASSETS_PATH"]
        )
        self.OS_PROPERTIES_PATH = path.join(
            base_dir, self.ui_data["data_paths"]["OS_PROPERTIES_PATH"]
        )
        self.CACHE_PATH = Path(
            path.expanduser(self.ui_data["data_paths"]["CACHE_PATH"])
        )

        # Get navigation button data
        NAVIGATION_BUTTON_DATA_PATH = path.join(
            base_dir, self.ui_data["data_paths"]["NAVIGATION_BUTTON_DATA_PATH"]
        )
        self.navigation_button_data = load_json_data.load_json_data(
            NAVIGATION_BUTTON_DATA_PATH
        )
        self.button_data = self.navigation_button_data["navigation_buttons"]

        # Get inputs data
        INPUTS_DATA_PATH = path.join(
            base_dir, self.ui_data["data_paths"]["INPUTS_DATA_PATH"]
        )
        self.inputs_data = load_json_data.load_json_data(INPUTS_DATA_PATH)

        self.header = CreateHeader()
        self.os_values = OSProperties(self.OS_PROPERTIES_PATH).get_values()
        self.input_values = OSProperties(self.OS_PROPERTIES_PATH).get_locations()
        self.navigation_button = NavigationButton(self.button_data)
        self.profile_folder_location = GetFolderLocations(
            self.os_values
        ).get_profile_folder()
        self.thread_manager = ThreadManager()


        self.chrome_folder = path.join(self.profile_folder_location, "chrome")

        # Initialize ImageLoader with the asset path and OS name
        self.image_loader = ImageLoader(self.ASSETS_PATH, self.os_values['os_name'])

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
        icons = self.ui_data["icons"]
        self.attention_icon = self.image_loader.load_attention_icon(icons)
        self.header_title_bg = self.image_loader.load_header_title_bg(icons)
        self.line_top_img = self.image_loader.load_line_top_img(icons)
        self.os_icon_image = self.image_loader.load_os_icon_image()
        self.preview_icon = self.image_loader.load_preview_icon(icons)
        self.theme_detected_icon = self.image_loader.load_theme_detected_icon(icons)


    def create_header(self):
        header_data = self.ui_data["header_data"]

        self.header.create_header(
            self.install_page_frame,
            header_title_bg=self.header_title_bg,
            line_top_img=self.line_top_img,
            text=header_data["text"],
        )

    def create_inputs_and_checkboxes(self):
        inputs_data = self.inputs_data["create_inputs_and_checkboxes"]

        inputs_checkboxes_frame = CTkFrame(
            self.install_page_frame,
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

        self.CSL = BooleanVar(value=False)
        CSL_checkbox = CTkCheckBox(
            master=frame,
            text=inputs_data["CSL_checkbox"]["text"],
            fg_color=inputs_data["CSL_checkbox"]["fg_color"],
            hover_color=inputs_data["CSL_checkbox"]["hover_color"],
            text_color=inputs_data["CSL_checkbox"]["text_color"],
            bg_color=inputs_data["CSL_checkbox"]["bg_color"],
            font=eval(inputs_data["CSL_checkbox"]["font"]),
            border_color=inputs_data["CSL_checkbox"]["border_color"],
            command=self.checkbox_event,
            variable=self.CSL,
            onvalue=True,
            offvalue=False,
        )
        CSL_checkbox.grid(
            row=inputs_data["CSL_checkbox"]["grid_data"]["row"],
            column=inputs_data["CSL_checkbox"]["grid_data"]["column"],
            padx=inputs_data["CSL_checkbox"]["grid_data"]["padx"],
            pady=inputs_data["CSL_checkbox"]["grid_data"]["pady"],
            sticky=inputs_data["CSL_checkbox"]["grid_data"]["sticky"],
        )
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
            base_dir=self.base_dir
        )
        self.detect_installed_theme_component.create_installed_themes(preview_and_check_installed_theme_frame)

        self.create_preview_theme(preview_and_check_installed_theme_frame)

        self.detect_installed_theme_component.detect_installed_theme()


    def create_preview_theme(self, preview_and_check_installed_theme_frame):
        preview_theme_data = self.ui_data["create_preview_theme"]
        preview_frame = CTkFrame(
            preview_and_check_installed_theme_frame,
            width=preview_theme_data["preview_frame"]["width"],
            height=preview_theme_data["preview_frame"]["height"],
            corner_radius=preview_theme_data["preview_frame"][
                "corner_radius"
            ],
            fg_color=preview_theme_data["preview_frame"]["fg_color"],
        )
        preview_frame.grid(
            row=preview_theme_data["preview_frame"]["grid_data"]["row"],
            column=preview_theme_data["preview_frame"]["grid_data"][
                "column"
            ],
            padx=preview_theme_data["preview_frame"]["grid_data"]["padx"],
            pady=preview_theme_data["preview_frame"]["grid_data"]["pady"],
            sticky=preview_theme_data["preview_frame"]["grid_data"][
                "sticky"
            ],
        )

        preview_label = CTkLabel(
            preview_frame,
            text=preview_theme_data["preview_label"]["text"],
            text_color=preview_theme_data["preview_label"]["text_color"],
            font=eval(preview_theme_data["preview_label"]["font"]),
        )
        preview_label.pack(
            padx=preview_theme_data["preview_label"]["pack_data"]["padx"],
            pady=preview_theme_data["preview_label"]["pack_data"]["pady"],
            side=preview_theme_data["preview_label"]["pack_data"]["side"],

        )

        preview_button =CTkButton(
            preview_frame,
            text=preview_theme_data["preview_button"]["text"],
            height=preview_theme_data["preview_button"]["height"],
            fg_color=preview_theme_data["preview_button"]["fg_color"],
            hover_color=preview_theme_data["preview_button"]["hover_color"],
            corner_radius=preview_theme_data["preview_button"]["corner_radius"],
            font=eval(preview_theme_data["preview_button"]["font"]),
            text_color=preview_theme_data["preview_button"]["text_color"],
            image=self.preview_icon,
            command=self.start_theme_preview_thread,
        )
        preview_button.pack(
            padx=preview_theme_data["preview_button"]["pack_data"]["padx"],
            pady=preview_theme_data["preview_button"]["pack_data"]["pady"],
        )
    
    def create_invalid_entry_frame(self):
        invalid_entry_frame_data = self.ui_data["create_invalid_entry_frame"]
        self.invalid_entry_frame = CTkFrame(
            self.install_page_frame,
            width=invalid_entry_frame_data["invalid_entry_frame"]["width"],
            height=invalid_entry_frame_data["invalid_entry_frame"]["height"],
            corner_radius=invalid_entry_frame_data["invalid_entry_frame"][
                "corner_radius"
            ],
            fg_color=invalid_entry_frame_data["invalid_entry_frame"]["fg_color"],
        )
        self.invalid_entry_frame.grid(
            row=invalid_entry_frame_data["invalid_entry_frame"]["grid_data"]["row"],
            column=invalid_entry_frame_data["invalid_entry_frame"]["grid_data"][
                "column"
            ],
            padx=invalid_entry_frame_data["invalid_entry_frame"]["grid_data"]["padx"],
            pady=invalid_entry_frame_data["invalid_entry_frame"]["grid_data"]["pady"],
        )

        self.invalid_entries_text = CTkLabel(
            self.invalid_entry_frame,
            text=invalid_entry_frame_data["invalid_entries_text"]["text"],
            text_color=invalid_entry_frame_data["invalid_entries_text"]["text_color"],
            font=eval(invalid_entry_frame_data["invalid_entries_text"]["font"]),
            compound=invalid_entry_frame_data["invalid_entries_text"]["compound"],
            image=self.attention_icon,
        )
        self.invalid_entries_text.pack(
            padx=invalid_entry_frame_data["invalid_entries_text"]["pack_data"]["padx"],
            pady=invalid_entry_frame_data["invalid_entries_text"]["pack_data"]["pady"],

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
            "Install",
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
                temp_dir="/tmp/theme_preview",
                custom_script_loader=self.CSL.get(),
                selected_theme_data=self.selected_theme_data,
            ),
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
            command=lambda: self.controller.show_frame("home_page"),
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

    def start_theme_preview_thread(self):
        # Start the preview in a new thread
        self.thread_manager.start_thread(target=self.preview_theme)

    def preview_theme(self):
        profile_folder = SpecialInputFunc().get_variables(self.profile_folder_entry)
        application_folder = SpecialInputFunc().get_variables(
            self.application_folder_entry
        )

        self.preview = PreviewTheme(
            self.CACHE_PATH,
            self.theme_dir,
            "/tmp/theme_preview",
            self.os_values["os_name"],
            self.CSL.get(),
            profile_folder,
            application_folder,
        )
        self.preview.run_firefox()

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
            self.invalid_entry_frame.grid_remove()
        else:
            self.install_button.configure(state="disabled")
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
        self.theme_dir = kwargs.get("theme_dir")
        self.selected_theme_data = kwargs.get("selected_theme_data")
