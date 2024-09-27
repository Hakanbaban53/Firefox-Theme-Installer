from itertools import cycle
from os import path
from tkinter import BooleanVar, PhotoImage, Label, TclError, Frame
from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkCheckBox

from components.create_header import CreateHeader
from components.create_navigation_button import NavigationButton
from installer_core.component_tools.thread_manager import ThreadManager
from installer_core.data_tools.get_os_properties import OSProperties
from installer_core.data_tools.image_loader import ImageLoader
from installer_core.data_tools.load_json_data import LoadJsonData
from installer_core.file_utils.detect_and_download_files import FileManager
from installer_core.file_utils.get_the_theme_files import ThemeDownloader
from modals.check_files_modal import FileInstallerModal
from modals.info_modals import InfoModals
from modals.theme_modal import ThemeModal

class HomePage(Frame):
    def __init__(self, parent, controller, base_dir, app_language):
        super().__init__(parent)
        # Load the UI data from the JSON file based on the selected language
        UI_DATA_PATH = path.join(base_dir, "language", "pages", "home_page", f"{app_language}.json")
        PATHS = path.join(base_dir, "data", "global", "paths.json")
        ICONS = path.join(base_dir, "data", "global", "icons.json")
        load_json_data = LoadJsonData()
        self.ui_data = load_json_data.load_json_data(UI_DATA_PATH)
        self.paths = load_json_data.load_json_data(PATHS)
        self.icons = load_json_data.load_json_data(ICONS)

        self.app_language = app_language
        self.controller = controller
        self.base_dir = base_dir

        # Set the animation speed
        self.ANIMATION_SPEED = 100

        # Set the paths
        self.ASSETS_PATH = path.join(
            base_dir, self.paths["ASSETS_PATH"]
        )
        
        self.os_properties = OSProperties(base_dir)
        self.os_values = self.os_properties.get_values()
        self.CACHE_PATH = self.os_properties.get_cache_location()
        self.CUSTOM_SCRIPT_LOADER_PATH = path.join(
            self.CACHE_PATH, self.paths["CUSTOM_SCRIPT_LOADER_PATH"]
        )
        self.THEME_PATH = path.join(
            self.CACHE_PATH, self.paths["THEME_PATH"]
        )

        self.thread_manager = ThreadManager()

        self.navigation_button = NavigationButton(base_dir=base_dir, app_language=app_language)
        self.header = CreateHeader()

        # Initialize ImageLoader with the asset path and OS name
        self.image_loader = ImageLoader(self.ASSETS_PATH, self.os_values['os_name'])

        # Initialize variables
        self.data_json_path = None
        self.modal_theme = None
        self.theme_data = None

        # Configure layout and create widgets
        self.configure_layout()
        self.create_widgets()

    def configure_layout(self):
        self.home_page_frame = CTkFrame(self, fg_color="#2B2631")
        self.home_page_frame.grid(row=0, column=1, sticky="SW")
        self.home_page_frame.columnconfigure(0, weight=1)

    def create_widgets(self):
        self.create_images()
        self.create_header()
        self.create_os_info()
        self.theme_select()
        self.create_navigation_buttons()
        self.create_file_detection()
        self.create_recheck_skip_section()

    def create_images(self):
        # Load icons and images using the ImageLoader
        
        self.attention_icon = self.image_loader.load_attention_icon(self.icons)
        self.check_icon = self.image_loader.load_check_icon(self.icons)
        self.install_files_icon = self.image_loader.load_install_files_icon(self.icons)
        self.theme_not_selected_icon = self.image_loader.load_theme_not_selected_icon(self.icons)
        self.theme_selected_icon = self.image_loader.load_theme_selected_icon(self.icons)
        self.header_title_bg = self.image_loader.load_header_title_bg(
            self.icons, size=(390, 64)  # Specific size for HomePage
        )
        self.line_top_img = self.image_loader.load_line_top_img(self.icons)
        self.os_icon_image = self.image_loader.load_os_icon_image()
        self.select_action_img = self.image_loader.load_select_action_img(self.icons)
        self.reload_icon = self.image_loader.load_reload_icon(self.icons)
        
    def create_header(self):
        self.header.create_header(
            self.home_page_frame, header_title_bg=self.header_title_bg, line_top_img=self.line_top_img, text=self.ui_data["header_label"]
        )

    def create_os_info(self):
        os_info = self.ui_data["create_os_info"]

        os_label = CTkLabel(
            self.home_page_frame,
            text=os_info["os_label"],
            text_color="#FFFFFF",
            font=("Arial", 20, "bold"),  # Convert the string to a tuple
        )
        os_label.grid(
            row=2,
            column=0,
            padx=(175,0),
            pady=20,
            sticky="ew",
        )
        os_frame = CTkFrame(
            self.home_page_frame,
            fg_color="#FFFFFF",
            corner_radius=12,
            border_width=0,
        )
        os_frame.grid(
            row=2,
            column=1,
            padx=(0,185),
            pady=0,
            sticky="ew",
        )

        os_info_label = CTkLabel(
            os_frame,
            text=f"{self.os_values['os_name']} ",
            text_color=self.os_values["os_color"],
            font=("Arial", 18),
            image=self.os_icon_image,
            compound="right",
        )
        os_info_label.pack(
            padx=10,
            pady=10,
            side="left",
        )

    def theme_select(self):
        theme_select = self.ui_data["theme_select"]

        theme_frame = CTkFrame(
            self.home_page_frame,
            fg_color="#FFFFFF",
            corner_radius=12,
            border_color="#771D76",
            border_width=4,
        )
        theme_frame.grid(
            row=3,
            column=0,
            columnspan=2,
            padx=0,
            pady=(10,35),
            sticky="",
        )

        self.theme_label = CTkLabel(
            theme_frame,
            text=theme_select["theme_label"],
            font=("Arial", 18),
            text_color="#000000"
        )
        self.theme_label.pack(
            padx=10,
            pady=10,
            side="left",
        )

        theme_select_button = self.navigation_button.create_navigation_button(
            theme_frame,
            theme_select["theme_select_button"],
            None,
            self.select_theme,
            padding_x=(10, 10),
            side="right",
        )
        theme_select_button.pack(
            padx=10,
            pady=10,
            side="right",
        )

    def create_navigation_buttons(self):

        navigation_buttons = self.ui_data["create_navigation_buttons"]

        select_action_label = CTkLabel(
            self.home_page_frame,
            text=navigation_buttons["select_action_label"],
            image=self.select_action_img,
            text_color="#FFFFFF",
            font=("Arial", 20),
        )
        select_action_label.grid(
            row=4,
            column=0,
            columnspan=2,
            padx=60,
            pady=(0,15),
            sticky="ew",
        )
        navigation_frame = CTkFrame(
            self.home_page_frame,
            fg_color="#FFFFFF",
            corner_radius=10,
            border_color="#F89F24",
            border_width=4,
            width=440,
            height=54,
        )
        navigation_frame.grid(
            row=5,
            column=0,
            columnspan=2,
            padx=10,
            pady=(0,15),
            sticky="",
        )

        self.navigation_button.create_navigation_button(
            navigation_frame,
            "remove_button",
            path.join(self.ASSETS_PATH, "icons/remove.png"),
            lambda: self.controller.show_frame("remove_page"),
            padding_x=(10, 20),
            side="right",
        )
        self.install_button = self.navigation_button.create_navigation_button(
            navigation_frame,
            "install_button",
            path.join(self.ASSETS_PATH, "icons/install.png"),
            lambda: self.controller.show_frame(
                "install_page",
                theme_dir=(
                    self.theme_data.get("path")
                    if self.theme_data.get("type") == "userChrome.css"
                    else path.join(self.theme_data.get("path"), "chrome")
                ),
                selected_theme_data = self.modal_theme.theme_selected.to_dict() # We sent the selected theme data a dictionary format.
            ),
            padding_x=(5, 5),
            side="right",
            state="disabled",
        )
        self.navigation_button.create_navigation_button(
            navigation_frame,
            "exit_button",
            path.join(self.ASSETS_PATH, "icons/exit.png"),
            lambda: InfoModals(self, self.base_dir, "Exit", app_language=self.app_language),
            padding_x=(20, 10),
            side="left",
        )

    def create_file_detection(self):

        file_detection = self.ui_data["create_file_detection"]

        self.detect_files_frame = CTkFrame(
            self.home_page_frame,
            fg_color="#FFFFFF",
            corner_radius=12,
            border_width=0,
        )
        self.detect_files_frame.grid(
            row=6,
            column=0,
            columnspan=2,
            padx=0,
            pady=0,
            sticky="",
        )
        self.detect_files_text = Label(
            self.detect_files_frame,
            text=f"{file_detection["detect_files_text"]} ",
            font=("Arial", 18),
            fg="#000000",
            bg="#FFFFFF",
            compound="right",
            image=self.theme_not_selected_icon,
        )
        self.detect_files_text.grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
            sticky="",
        )
        self.install_files_button = CTkButton(
            master=self.detect_files_frame,
            text=file_detection["install_files_button"],
            width=120,
            height=40,
            corner_radius=12,
            fg_color="#E0E0E0",
            hover_color="#D0D0D0",
            text_color="#000000",
            font=("Arial", 18, "bold")
        )

    def create_recheck_skip_section(self):
        create_section = self.ui_data["create_recheck_skip_section"]

        self.recheck_skip_frame = CTkFrame(
            self.home_page_frame,
            fg_color="#2B2631",
        )
        self.recheck_skip_frame.grid(
            row=7,
            column=0,
            columnspan=2,
            padx=0,
            pady=0,
            sticky="",
        )

        self.check_var = BooleanVar(value=False)
        self.clean_install = CTkCheckBox(
            self.recheck_skip_frame,
            text=create_section["clean_install_checkbox"],
            text_color="#FFFFFF",
            onvalue=True,
            offvalue=False,
            variable=self.check_var,
            font=("Arial", 16, "bold"),
        )
        self.clean_install.grid(
            row=7,
            column=0,
            padx=10,
            pady=10,
            sticky="", 
        )
        self.clean_install.lower()

        self.recheck_button = CTkButton(
            self.recheck_skip_frame,
            width=40,
            height=40,
            text="",
            fg_color="#FFFFFF",
            image=self.reload_icon,
        )

    def start_loading_animation(self):
        """Start the loading GIF animation."""
        self.frames = self.load_gif()
        self.update_gif(self.frames)

    def stop_loading_animation(self):
        """Stop the loading GIF animation."""
        if hasattr(self, "animation_id"):
            self.after_cancel(self.animation_id)
            self.detect_files_text.config(image="")

    def load_gif(self):
        """Load frames from the GIF file."""
        frames = []
        index = 0
        while True:
            try:
                frame = PhotoImage(
                    file=path.join(self.ASSETS_PATH, self.icons["block_spin_gif"]),
                    format=f"gif -index {index}",
                )
                frames.append(frame)
                index += 2
            except TclError:
                break
        return cycle(frames)

    def update_gif(self, frames):
        """Update the GIF animation frame by frame."""
        frame = next(frames)
        self.detect_files_text.config(image=frame)
        self.animation_id = self.after(self.ANIMATION_SPEED, self.update_gif, frames)

    # Theme selection and processing
    def select_theme(self):
        """Open the theme selection modal and configure UI elements based on selection."""
        self.modal_theme = ThemeModal(self, self.base_dir, self.CACHE_PATH, app_language=self.app_language)
        self.wait_window(self.modal_theme)
        self.recheck_button.lower()

        if getattr(self.modal_theme, "theme_selected", False):
            self.update_ui_for_selected_theme()
        else:
            self.clear_selection()

    def clear_selection(self):
        clear_selection = self.ui_data["clear_selection"]
        self.modal_theme = None
        self.theme_label.configure(text=clear_selection["theme_label"])
        self.detect_files_text.config(
            text=f"{clear_selection["detect_files_text"]} ",
            fg="#000000",
            image=self.theme_not_selected_icon,
        )
        self.install_button.configure(state="disabled")
        self.install_files_button.grid_remove()


    def update_ui_for_selected_theme(self):
        """Update UI when a theme is selected."""
        updated_ui_data = self.ui_data["update_ui_for_selected_theme"]

        self.install_button.configure(state="disabled")
        
        self.detect_files_text.config(
        image=self.theme_selected_icon,
        text=f"{updated_ui_data["detect_files_text"]} ",
        fg="#000000",
        )

        self.theme_label.configure(
            text=f"{updated_ui_data["theme_label"]} {self.modal_theme.theme_selected.title}"
        )
        self.install_files_button.configure(
            command=self.get_theme,
            text=updated_ui_data["install_files_button"],
            text_color="#000000",
            image=None,
            state="normal", 
        )
        self.clean_install.lift()
        self.install_files_button.grid(pady=10)

    def run_theme_process(self):
        """Run the theme processing logic."""
        self.theme_data = ThemeDownloader(
            self.modal_theme.theme_selected,
            self.THEME_PATH,
            self.check_var.get(),
            self.base_dir,
        ).process_theme()
        if isinstance(self.theme_data, dict):
            theme_type = self.theme_data.get("type")
            self.handle_theme_type(theme_type)
        else:
            self.no_theme_data_found()

    def handle_theme_type(self, theme_type):
        """Handle different types of themes based on the theme data."""
        if theme_type == "data":
            self.handle_data_json_theme()
        elif theme_type == "userChrome.css":
            self.handle_userChrome_theme()
        else:
            self.no_theme_data_found()

    def handle_data_json_theme(self):
        """Handle themes that have their own data JSON file."""
        handle_data_json_theme = self.ui_data["handle_data_json_theme"]
        self.detect_files_text.config(
            text=handle_data_json_theme["detect_files_text"],
            fg="#00FF00",
        )
        self.data_json_path = path.join(self.theme_data.get("path"), "data", "installer_files_data.json")
        self.thread_manager.start_thread(target=self.fetch_files)
        self.clean_install.lower()

    def handle_userChrome_theme(self):
        """Handle themes that include a userChrome.css file."""
        handle_userChrome_theme = self.ui_data["handle_userChrome_theme"]
        self.detect_files_text.config(
            text=handle_userChrome_theme["detect_files_text"],
            fg="#00FF00",
        )
        self.install_button.configure(
            state="Normal"
        )
        self.recheck_button.configure(
            state="normal",
            command=self.get_theme)
        self.install_files_button.configure(
            image=self.check_icon,
            text=handle_userChrome_theme["install_files_button"],
            text_color="#000000",
            state="disabled",
            fg_color="#D9D9D9",
            width=150,
        )       
        self.check_var = BooleanVar(value=False)
        self.recheck_button.grid(
            row=1,
            column=0,
            padx=10,
            pady=10,
            sticky="",
        )
        self.clean_install.lower()

    def no_theme_data_found(self):
        """Handle cases where no valid theme data is found."""
        no_theme_data_found = self.ui_data["no_theme_data_found"]
        self.detect_files_text.config(
            text=no_theme_data_found["detect_files_text"],
            fg= "#FF0000",
        )
        self.install_files_button.configure(
            image=self.check_icon,
            text=no_theme_data_found["install_files_button"],
            text_color="#000000",
            state="disabled",
            fg_color="#D9D9D9",
            width=150,
        )  
        self.install_button.configure(
            state="disabled"
        )

    # File handling and animations
    def locate_files(self):
        """Check if all necessary theme files are present."""
        file_check_result = FileManager(self.data_json_path).check_files_exist(
            root=self.theme_data.get("path")
        )
        if file_check_result:
            self.handle_missing_files()
        else:
            self.handle_all_files_installed()

    def handle_all_files_installed(self):
        """Update UI when all theme files are installed."""
        handle_all_files_installed = self.ui_data["handle_all_files_installed"]
        self.install_files_button.configure(
            width=200,
            text=handle_all_files_installed["install_files_button"],
            text_color="#10dc60",
            state="disabled",
            image=self.check_icon,
        )
        self.install_button.configure(state="normal")
        self.recheck_button.grid(
            row=7,
            column=1,
            padx=10,
            pady=10,
            sticky="",
        )
        self.clean_install.lower()

    def handle_missing_files(self):
        """Update UI when some theme files are missing."""
        handle_missing_files = self.ui_data["handle_missing_files"]
        self.install_files_button.configure(
            text=handle_missing_files["install_files_button"],
            text_color="#f04141",
            state="normal",
            width=200,
            image=self.attention_icon, command=self.install_files
        )
        self.install_files_button.grid(
            row=2,
            column=0,
            padx=10,
            pady=10,
            sticky="",
        )
        self.recheck_button.grid(
            row=7,
            column=1,
            padx=10,
            pady=10,
            sticky="",
        )

    def install_files(self):
        """Open modal to install missing files and recheck afterward."""
        modal = FileInstallerModal(self, self.base_dir, self.data_json_path, self.theme_data.get("path"), app_language=self.app_language)
        self.wait_window(modal)
        self.recheck_files()

    def refetch_files(self):
        """Refetch necessary files and update UI."""
        refetch_files = self.ui_data["refetch_files"]
        self.install_files_button.configure(
            text=refetch_files["install_files_button"],
            text_color="#000000",
            state="disabled",
        )
        self.install_button.configure(state="disabled")
        self.clean_install.lower()
        self.thread_manager.start_thread(self.fetch_files)

    # Thread and file fetching management
    def get_theme(self):
        """Handle the theme installation process."""
        get_theme = self.ui_data["get_theme"]
        self.start_loading_animation()
        self.get_neccessary_files()
        self.install_files_button.configure(
            text=get_theme["install_files_button"],
            text_color="#000000",
            state="disabled",
        )
        self.detect_files_text.config(
            text=f"{get_theme["detect_files_text"]} ", fg="#000000"
        )
        self.thread_manager.start_thread(target=self.run_theme_process, on_finish=self.stop_loading_animation)

    def get_neccessary_files(self):
        """Fetch and check necessary files for the theme."""
        get_neccessary_files = self.ui_data["get_neccessary_files"]
        self.detect_files_text.config(
            text=f"{get_neccessary_files["detect_files_text"]} ",
            fg="#000000",
        )
        file_manager = FileManager(json_file_path=self.CUSTOM_SCRIPT_LOADER_PATH, json_file_url=self.paths["CUSTOM_SCRIPT_LOADER_URL"])
        if file_manager.json_data:
            missing_files = file_manager.check_files_exist()
            if missing_files:
                self.thread_manager.start_thread(file_manager.download_missing_files, missing_files, self.CACHE_PATH)


    def fetch_files(self):
        """Fetch files based on data JSON path."""
        self.start_loading_animation()
        file_manager = FileManager(self.data_json_path)
        self.recheck_button.configure(
            state="normal",
            command=self.refetch_files)
        self.recheck_button.grid(
            row=7,
            column=1,
            padx=10,
            pady=10,
            sticky="",
        )

        if file_manager.json_data:
            self.thread_manager.start_thread(self.locate_files, on_finish=self.stop_loading_animation)
        else:
            self.handle_fetch_files_failure()

    def recheck_files(self):
        """Recheck file status and update UI."""
        recheck_files = self.ui_data["recheck_files"]
        self.start_loading_animation()
        self.install_files_button.configure(
            text=recheck_files["install_files_button"],
            text_color="#000000",
            state="disabled",
        )
        self.install_button.configure(state="disabled")
        self.clean_install.lower()
        self.thread_manager.start_thread(self.locate_files, on_finish=self.stop_loading_animation)

    def handle_fetch_files_failure(self):
        """Handle the failure to fetch files."""
        handle_fetch_files_failure = self.ui_data["handle_fetch_files_failure"]
        self.install_files_button.configure(
            image=self.attention_icon,
            text=handle_fetch_files_failure["install_files_button"],
            text_color="#f04141",
            state="disabled",
        )
        self.clean_install.grid(
            row=7,
            column=0,
            padx=10,
            pady=10,
            sticky="",
        )

    def update_parameters(self, **kwargs):
        # Process and use the parameters as needed
        pass
