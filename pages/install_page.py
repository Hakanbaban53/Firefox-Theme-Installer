from json import JSONDecodeError, load
from os import path

import threading
from tkinter import BooleanVar
from customtkinter import (
    CTkFrame,
    CTkImage,
    CTkLabel,
    CTkFont,
    CTkEntry,
    CTkCheckBox,
    StringVar,
    CTkButton,
)
from PIL import Image

from components.create_header import CreateHeader
from components.create_navigation_button import NavigationButton
from functions.get_theme_data import Theme
from functions.preview_theme import PreviewTheme
from modals.info_modals import InfoModals
from functions.get_os_properties import OSProperties
from functions.get_folder_locations import GetFolderLocations
from functions.special_input_functions import SpecialInputFunc
from modals.theme_detail_modal import ThemeDetailModal


class InstallPage(CTkFrame):
    def __init__(self, parent, controller, base_dir):
        super().__init__(parent)
        self.controller = controller
        self.base_dir = base_dir
        self.theme_dir = None
        self.theme_data = None

        self.config_data = self.load_json_data(
            path.join(base_dir, "data", "pages", "install_page_data.json")
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
        self.inputs_data = self.load_json_data(self.INPUTS_DATA_PATH)

        self.button_data = self.navigation_button_data["navigation_buttons"]
        self.input_data = self.inputs_data["inputs"]

        self.header = CreateHeader()
        self.os_values = OSProperties(self.OS_PROPERTIES_PATH).get_values()
        self.input_values = OSProperties(self.OS_PROPERTIES_PATH).get_locations()
        self.navigation_button = NavigationButton(self.button_data)
        self.profile_folder_location = GetFolderLocations(
            self.os_values
        ).get_profile_folder()

        self.chrome_folder = path.join(self.profile_folder_location, "chrome")
        self.theme_data_path = path.join(self.chrome_folder, "selected_theme_data.json")

        self.configure_layout()
        self.create_widgets()

    def load_json_data(self, path):
        with open(path, "r") as file:
            return load(file)

    def configure_layout(self):
        self.fg_color = "#2B2631"
        self.grid(row=0, column=1, sticky="SW")
        self.columnconfigure(0, weight=1)

        self.install_page_frame = CTkFrame(
            self,
            fg_color="#2B2631",
        )
        self.install_page_frame.grid(row=0, column=0, sticky="SW")
        self.install_page_frame.columnconfigure(0, weight=1)

    def create_widgets(self):
        self.create_images()
        self.create_header()
        self.create_installed_themes_frame()
        self.create_inputs()
        self.create_invalid_entry_frame()
        self.create_preview_theme()
        self.create_bottom_widgets()
        self.update_button_and_frame()
        self.checkbox_event()
        self.detect_installed_theme()

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
            size=(390, 64),
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
        self.preview_icon = CTkImage(
            light_image=Image.open(path.join(self.ASSETS_PATH, icons["preview_icon"])),
            dark_image=Image.open(path.join(self.ASSETS_PATH, icons["preview_icon"])),
            size=(24, 24),
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
        self.theme_not_detected_icon = CTkImage(
            light_image=Image.open(
                path.join(self.ASSETS_PATH, icons["theme_not_detected_icon"])
            ),
            dark_image=Image.open(
                path.join(self.ASSETS_PATH, icons["theme_not_detected_icon"])
            ),
            size=(24, 32),
        )

    def create_header(self):
        self.header.create_header(
            self.install_page_frame, self.header_title_bg, self.line_top_img
        )

    def create_installed_themes_frame(self):
        installed_themes_frame = CTkFrame(
            self.install_page_frame,
            width=440,
            height=60,
            corner_radius=12,
            fg_color="white",
        )
        installed_themes_frame.grid(
            row=2, column=0, columnspan=2, padx=40, pady=0, sticky=""
        )

        self.installed_themes_label = CTkLabel(
            installed_themes_frame,
            text="",
            text_color="black",
            font=("Arial", 18, "bold"),
            compound="right",
        )
        self.installed_themes_label.pack(padx=(10, 4), pady=10, side="left")

        self.theme_details_button = CTkButton(
            installed_themes_frame,
            text="Theme Details",
            height=42,
            fg_color="#D9D9D9",
            hover_color="#EEEEEE",
            corner_radius=12,
            text_color="#000000",
            compound="right",
            font=("Arial", 16, "bold"),
            image=self.theme_detected_icon,
            command=lambda: ThemeDetailModal(
                self,
                theme=self.theme_data,
                cache_dir=self.cache_dir,
                base_dir=self.base_dir,
            ),
        )

    def create_inputs(self):
        inputs_frame = CTkFrame(
            self.install_page_frame,
            width=440,
            height=54,
            corner_radius=12,
            fg_color="#2B2631",
        )
        inputs_frame.grid(
            row=3, column=0, columnspan=2, padx=40, pady=(10, 20), sticky="NSEW"
        )

        self.create_input_widgets(inputs_frame)
        self.create_edit_checkbox(inputs_frame)

    def create_input_widgets(self, frame):
        # Profile Name
        self.profile_folder_label = CTkLabel(
            master=frame,
            text_color="white",
            font=CTkFont(family="Inter", size=18, weight="bold"),
            text="Profile Folder",
        )
        self.profile_folder_label.grid(
            row=0, column=0, padx=(10, 4), pady=(14, 2), sticky="w"
        )

        self.profile_folder_entry = CTkEntry(
            master=frame,
            width=int(self.input_data["width"]),
            height=int(self.input_data["height"]),
            fg_color=self.input_data["fg_color"],
            text_color=self.input_data["text_color"],
            corner_radius=int(self.input_data["corner_radius"]),
            border_width=int(self.input_data["border_width"]),
            bg_color=self.input_data["bg_color"],
            border_color=self.input_data["border_color"],
            placeholder_text=self.profile_folder_location,
        )
        self.profile_folder_entry.grid(
            row=1, column=0, padx=(10, 4), pady=10, sticky="ew"
        )

        # Application Folder
        self.application_folder_label = CTkLabel(
            master=frame,
            text_color="white",
            font=CTkFont(family="Inter", size=18, weight="bold"),
            text="Application Folder",
        )
        self.application_folder_label.grid(
            row=0, column=1, padx=(10, 4), pady=(14, 2), sticky="w"
        )

        self.application_folder_entry = CTkEntry(
            master=frame,
            width=int(self.input_data["width"]),
            height=int(self.input_data["height"]),
            fg_color=self.input_data["fg_color"],
            text_color=self.input_data["text_color"],
            corner_radius=int(self.input_data["corner_radius"]),
            border_width=int(self.input_data["border_width"]),
            bg_color=self.input_data["bg_color"],
            border_color=self.input_data["border_color"],
            placeholder_text=self.input_values["application_folder"],
        )
        self.application_folder_entry.grid(
            row=1, column=1, padx=(10, 4), pady=10, sticky="ew"
        )

        self.key_bind(self.profile_folder_entry)
        self.key_bind(self.application_folder_entry)

        self.CSL = BooleanVar(value=False)
        CSL_checkbox = CTkCheckBox(
            master=frame,
            text="Enable Custom Script Loader",
            command=self.checkbox_event,
            fg_color="#F08D27",
            hover_color="#F08D27",
            bg_color="#2B2631",
            text_color="white",
            variable=self.CSL,
            onvalue=True,
            offvalue=False,
        )
        CSL_checkbox.grid(row=2, column=0, padx=(10, 4), pady=10, sticky="ew")

        self.telemetry = BooleanVar(value=False)
        telemetry_checkbox = CTkCheckBox(
            master=frame,
            text="Disable Firefox Telemetry",
            command=self.checkbox_event,
            fg_color="#F08D27",
            hover_color="#F08D27",
            bg_color="#2B2631",
            text_color="white",
            variable=self.telemetry,
            onvalue=True,
            offvalue=False,
        )
        telemetry_checkbox.grid(row=2, column=1, padx=(10, 4), pady=10, sticky="ew")

    def create_edit_checkbox(self, frame):
        self.check_var = StringVar(value="off")
        edit_checkbox = CTkCheckBox(
            master=frame,
            text="Edit Inputs",
            command=self.checkbox_event,
            fg_color="#F08D27",
            hover_color="#F08D27",
            bg_color="#2B2631",
            text_color="white",
            variable=self.check_var,
            onvalue="on",
            offvalue="off",
        )
        edit_checkbox.grid(row=3, column=1, padx=(10, 4), pady=10, sticky="ew")

    def create_invalid_entry_frame(self):
        self.invalid_entry_frame = CTkFrame(
            self.install_page_frame,
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

    def create_preview_theme(self):
        preview_frame = CTkFrame(
            self.install_page_frame,
            width=440,
            height=60,
            corner_radius=12,
            fg_color="white",
        )
        preview_frame.grid(
            row=5, column=0, columnspan=2, padx=40, pady=(20, 30), sticky=""
        )

        preview_label = CTkLabel(
            preview_frame,
            text="Preview Theme in Firefox",
            text_color="black",
            font=("Arial", 18, "bold"),
        )
        preview_label.pack(padx=(10, 4), pady=10, side="left")

        self.navigation_button.create_navigation_button(
            preview_frame,
            text="Preview Theme",
            image_path=path.join(self.ASSETS_PATH, "icons/preview_icon.png"),
            side="right",
            padding_x=10,
            command=self.start_theme_preview_thread,  # Updated to use threading
        )

    def start_theme_preview_thread(self):
        # Start the preview in a new thread
        preview_thread = threading.Thread(target=self.preview_theme)
        preview_thread.start()

    def preview_theme(self):
        profile_folder = SpecialInputFunc().get_variables(self.profile_folder_entry)
        application_folder = SpecialInputFunc().get_variables(
            self.application_folder_entry
        )

        self.preview = PreviewTheme(
            self.base_dir,
            self.theme_dir,
            "/tmp/theme_preview",
            self.os_values["os_name"],
            self.CSL.get(),
            profile_folder,
            application_folder,
        )
        self.preview.run_firefox()

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
            path.join(self.ASSETS_PATH, "icons/install_icon.png"),
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
        if SpecialInputFunc().update_invalid_entries_display():
            self.install_button.configure(state="normal")
            self.invalid_entry_frame.grid_remove()
        else:
            self.install_button.configure(state="disabled")
            self.invalid_entries_text.configure(
                text=f"  {len(SpecialInputFunc().return_invalid_entries())} entries is invalid"
            )
            self.invalid_entry_frame.grid()

    def get_variables_combobox(self, combobox_widget):
        selected_value = combobox_widget.get()
        return selected_value if selected_value else "Blue"

    def checkbox_event(self):
        if self.check_var.get() == "on":
            self.application_folder_entry.configure(state="normal")
            self.profile_folder_entry.configure(state="normal")
        else:
            self.application_folder_entry.configure(state="disabled")
            self.profile_folder_entry.configure(state="disabled")

    def detect_installed_theme(self):
        # Start the detection in a separate thread
        thread = threading.Thread(target=self._detect_installed_theme)
        thread.start()
        thread.join()  # Wait for the thread to finish
        result = self._detect_installed_theme()  # Get the result

        # Update the label based on the result
        self.update_ui(result)

    def _detect_installed_theme(self):
        # Check if the chrome folder exists
        if path.exists(self.chrome_folder):
            # Check for the theme data file
            if path.isfile(self.theme_data_path):
                try:
                    with open(self.theme_data_path, "r") as file:
                        data = load(file)
                        # Assuming 'title' is a key in the JSON file
                        self.theme_data = Theme(**data)
                        if self.theme_data.title:
                            return self.theme_data.title
                        else:
                            return False
                except (JSONDecodeError, IOError) as e:
                    print(f"Error reading theme data file: {e}")
                    return False
            else:
                # Check if userChrome.css exists
                user_chrome_css_path = path.join(self.chrome_folder, "userChrome.css")
                if path.isfile(user_chrome_css_path):
                    return True
                else:
                    return False
        else:
            return False

    def update_ui(self, result):
        # Use the Tkinter `after` method to safely update the UI from the main thread
        def update_label():
            if result is True:
                self.installed_themes_label.configure(text="Unknow Theme Installed ")
            elif result is False:
                self.installed_themes_label.configure(text="No Theme Installed ")
            else:
                self.installed_themes_label.configure(
                    text=f"Theme Installed: {result} "
                )
                self.theme_details_button.pack(padx=10, pady=10, side="right")

        # Call the update function after a delay to ensure it's on the main thread
        self.installed_themes_label.after(0, update_label)

    def update_parameters(self, **kwargs):
        self.theme_dir = kwargs.get("theme_dir")
        self.selected_theme_data = kwargs.get("selected_theme_data")
