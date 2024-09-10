from itertools import cycle
from os import path
from pathlib import Path
from tkinter import BooleanVar, PhotoImage, Label, TclError
from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkCheckBox

from components.create_header import CreateHeader
from components.create_navigation_button import NavigationButton
from installer_core.component_tools.thread_managing import ThreadManager
from installer_core.data_tools.get_os_properties import OSProperties
from installer_core.data_tools.image_loader import ImageLoader
from installer_core.data_tools.load_json_data import LoadJsonData
from installer_core.file_utils.detect_and_download_files import FileManager
from installer_core.file_utils.get_the_theme_files import ThemeDownloader
from modals.check_files_modal import FileInstallerModal
from modals.info_modals import InfoModals
from modals.theme_modal import ThemeModal

class HomePage(CTkFrame):

    def __init__(self, parent, controller, base_dir):
        super().__init__(parent)
        # Load the UI data from the JSON file
        UI_DATA_PATH = path.join(base_dir, "data", "pages", "home_page_data.json")
        load_json_data = LoadJsonData()
        self.ui_data = load_json_data.load_json_data(UI_DATA_PATH)

        self.controller = controller
        self.base_dir = base_dir

        # Set the animation speed
        self.ANIMATION_SPEED = self.ui_data["additional_settings"]["animation_speed"]

        # Set the paths
        self.ASSETS_PATH = path.join(
            base_dir, self.ui_data["data_paths"]["ASSETS_PATH"]
        )
        self.NAVIGATION_BUTTON_DATA_PATH = path.join(
            base_dir, self.ui_data["data_paths"]["NAVIGATION_BUTTON_DATA_PATH"]
        )
        self.OS_PROPERTIES_PATH = path.join(
            base_dir, self.ui_data["data_paths"]["OS_PROPERTIES_PATH"]
        )
        
        self.os_values = OSProperties(self.OS_PROPERTIES_PATH).get_values()

        if self.os_values['os_name'].lower()=="windows":
            self.CACHE_PATH = Path(
                path.expandvars(self.ui_data["data_paths"]["CACHE_PATH_win"])
            )
        else:
            self.CACHE_PATH = Path(
                path.expanduser(self.ui_data["data_paths"]["CACHE_PATH_unix"])
            )
        self.THEME_PATH = path.join(
            self.CACHE_PATH, self.ui_data["data_paths"]["THEME_PATH"]
        )
        self.CUSTOM_SCRIPT_LOADER_PATH = path.join(
            self.CACHE_PATH, self.ui_data["data_paths"]["CUSTOM_SCRIPT_LOADER_PATH"]
        )

        # Load additional data
        self.navigation_button_data = load_json_data.load_json_data(
            self.NAVIGATION_BUTTON_DATA_PATH
        )
        self.button_data = self.navigation_button_data["navigation_buttons"]

        self.thread_manager = ThreadManager()


        self.navigation_button = NavigationButton(self.button_data)
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
        icons = self.ui_data["icons"]
        self.attention_icon = self.image_loader.load_attention_icon(icons)
        self.check_icon = self.image_loader.load_check_icon(icons)
        self.install_files_icon = self.image_loader.load_install_files_icon(icons)
        self.theme_not_selected_icon = self.image_loader.load_theme_not_selected_icon(icons)
        self.theme_selected_icon = self.image_loader.load_theme_selected_icon(icons)
        self.header_title_bg = self.image_loader.load_header_title_bg(
            icons, size=(390, 64)  # Specific size for HomePage
        )
        self.line_top_img = self.image_loader.load_line_top_img(icons)
        self.os_icon_image = self.image_loader.load_os_icon_image()
        self.select_action_img = self.image_loader.load_select_action_img(icons)
        self.reload_icon = self.image_loader.load_reload_icon(icons)
        
    def create_header(self):
        header_data = self.ui_data["header_data"]
        self.header.create_header(
            self.home_page_frame, header_title_bg=self.header_title_bg, line_top_img=self.line_top_img, text=header_data["text"]
        )

    def create_os_info(self):
        os_info = self.ui_data["create_os_info"]

        os_label = CTkLabel(
            self.home_page_frame,
            text=os_info["os_label"]["text"],
            text_color=os_info["os_label"]["text_color"],
            font=eval(os_info["os_label"]["font"]),  # Convert the string to a tuple
        )
        os_label.grid(
            row=os_info["os_label"]["grid_data"]["row"],
            column=os_info["os_label"]["grid_data"]["column"],
            padx=os_info["os_label"]["grid_data"]["padx"],
            pady=os_info["os_label"]["grid_data"]["pady"],
            sticky=os_info["os_label"]["grid_data"]["sticky"],
        )
        os_frame = CTkFrame(
            self.home_page_frame,
            fg_color=os_info["os_frame"]["fg_color"],
            corner_radius=int(os_info["os_frame"]["corner_radius"]),
            border_color=os_info["os_frame"]["border_color"],
            border_width=int(os_info["os_frame"]["border_width"]),
        )
        os_frame.grid(
            row=os_info["os_frame"]["grid_data"]["row"],
            column=os_info["os_frame"]["grid_data"]["column"],
            padx=os_info["os_frame"]["grid_data"]["padx"],
            pady=os_info["os_frame"]["grid_data"]["pady"],
            sticky=os_info["os_frame"]["grid_data"]["sticky"],
        )

        os_info_label = CTkLabel(
            os_frame,
            text=f"{self.os_values['os_name']} ",
            text_color=self.os_values["os_color"],
            font=eval(os_info["os_info_label"]["font"]),
            image=self.os_icon_image,
            compound=os_info["os_info_label"]["compound"],
        )
        os_info_label.pack(
            padx=os_info["os_info_label"]["pack_data"]["padx"],
            pady=os_info["os_info_label"]["pack_data"]["pady"],
            side=os_info["os_info_label"]["pack_data"]["side"],
        )

    def theme_select(self):
        theme_select = self.ui_data["theme_select"]

        theme_frame = CTkFrame(
            self.home_page_frame,
            fg_color=theme_select["theme_frame"]["fg_color"],
            corner_radius=int(theme_select["theme_frame"]["corner_radius"]),
            border_color=theme_select["theme_frame"]["border_color"],
            border_width=int(theme_select["theme_frame"]["border_width"]),
        )
        theme_frame.grid(
            row=theme_select["theme_frame"]["grid_data"]["row"],
            column=theme_select["theme_frame"]["grid_data"]["column"],
            columnspan=theme_select["theme_frame"]["grid_data"]["columnspan"],
            padx=theme_select["theme_frame"]["grid_data"]["padx"],
            pady=theme_select["theme_frame"]["grid_data"]["pady"],
            sticky=theme_select["theme_frame"]["grid_data"]["sticky"],
        )

        self.theme_label = CTkLabel(
            theme_frame,
            text=theme_select["theme_label"]["text"],
            font=eval(theme_select["theme_label"]["font"]),
            text_color=theme_select["theme_label"]["fg_color"],
        )
        self.theme_label.pack(
            padx=theme_select["theme_label"]["pack_data"]["padx"],
            pady=theme_select["theme_label"]["pack_data"]["pady"],
            side=theme_select["theme_label"]["pack_data"]["side"],
        )

        theme_select_button = CTkButton(
            theme_frame,
            text=theme_select["theme_select_button"]["text"],
            width=float(self.button_data["width"]),
            height=float(self.button_data["height"]),
            corner_radius=float(self.button_data["corner_radius"]),
            bg_color=self.button_data["bg_color"],
            fg_color=self.button_data["fg_color"],
            hover_color=self.button_data["hover_color"],
            text_color=self.button_data["text_color"],
            command=self.select_theme,
            font=(self.button_data["font_family"], int(self.button_data["font_size"])),
        )
        theme_select_button.pack(
            padx=theme_select["theme_select_button"]["pack_data"]["padx"],
            pady=theme_select["theme_select_button"]["pack_data"]["pady"],
            side=theme_select["theme_select_button"]["pack_data"]["side"],
        )

    def create_navigation_buttons(self):

        navigation_buttons = self.ui_data["create_navigation_buttons"]

        select_action_label = CTkLabel(
            self.home_page_frame,
            text=navigation_buttons["select_action_label"]["text"],
            image=self.select_action_img,
            text_color=navigation_buttons["select_action_label"]["text_color"],
            font=eval(navigation_buttons["select_action_label"]["font"]),
        )
        select_action_label.grid(
            row=navigation_buttons["select_action_label"]["grid_data"]["row"],
            column=navigation_buttons["select_action_label"]["grid_data"]["column"],
            columnspan=navigation_buttons["select_action_label"]["grid_data"][
                "columnspan"
            ],
            padx=navigation_buttons["select_action_label"]["grid_data"]["padx"],
            pady=navigation_buttons["select_action_label"]["grid_data"]["pady"],
            sticky=navigation_buttons["select_action_label"]["grid_data"]["sticky"],
        )
        navigation_frame = CTkFrame(
            self.home_page_frame,
            fg_color=navigation_buttons["navigation_frame"]["fg_color"],
            corner_radius=int(navigation_buttons["navigation_frame"]["corner_radius"]),
            border_color=navigation_buttons["navigation_frame"]["border_color"],
            border_width=int(navigation_buttons["navigation_frame"]["border_width"]),
            width=navigation_buttons["navigation_frame"]["width"],
            height=navigation_buttons["navigation_frame"]["height"],
        )
        navigation_frame.grid(
            row=navigation_buttons["navigation_frame"]["grid_data"]["row"],
            column=navigation_buttons["navigation_frame"]["grid_data"]["column"],
            columnspan=navigation_buttons["navigation_frame"]["grid_data"][
                "columnspan"
            ],
            padx=navigation_buttons["navigation_frame"]["grid_data"]["padx"],
            pady=navigation_buttons["navigation_frame"]["grid_data"]["pady"],
            sticky=navigation_buttons["navigation_frame"]["grid_data"]["sticky"],
        )

        self.navigation_button.create_navigation_button(
            navigation_frame,
            "Remove",
            path.join(self.ASSETS_PATH, "icons/remove.png"),
            lambda: self.controller.show_frame("remove_page"),
            padding_x=(10, 20),
            side="right",
        )
        self.install_button = self.navigation_button.create_navigation_button(
            navigation_frame,
            "Install",
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
            "Exit",
            path.join(self.ASSETS_PATH, "icons/exit.png"),
            lambda: InfoModals(self, self.base_dir, "Exit"),
            padding_x=(20, 10),
            side="left",
        )

    def create_file_detection(self):

        file_detection = self.ui_data["create_file_detection"]

        self.detect_files_frame = CTkFrame(
            self.home_page_frame,
            fg_color=file_detection["detect_files_frame"]["fg_color"],
            corner_radius=int(file_detection["detect_files_frame"]["corner_radius"]),
            border_color=file_detection["detect_files_frame"]["border_color"],
            border_width=int(file_detection["detect_files_frame"]["border_width"]),
        )
        self.detect_files_frame.grid(
            row=file_detection["detect_files_frame"]["grid_data"]["row"],
            column=file_detection["detect_files_frame"]["grid_data"]["column"],
            columnspan=file_detection["detect_files_frame"]["grid_data"]["columnspan"],
            padx=file_detection["detect_files_frame"]["grid_data"]["padx"],
            pady=file_detection["detect_files_frame"]["grid_data"]["pady"],
            sticky=file_detection["detect_files_frame"]["grid_data"]["sticky"],
        )
        self.detect_files_text = Label(
            self.detect_files_frame,
            text=file_detection["detect_files_text"]["text"],
            font=eval(file_detection["detect_files_text"]["font"]),
            fg=file_detection["detect_files_text"]["fg"],
            bg=file_detection["detect_files_text"]["bg"],
            compound=file_detection["detect_files_text"]["compound"],
            image=self.theme_not_selected_icon,
        )
        self.detect_files_text.grid(
            row=file_detection["detect_files_text"]["grid_data"]["row"],
            column=file_detection["detect_files_text"]["grid_data"]["column"],
            padx=file_detection["detect_files_text"]["grid_data"]["padx"],
            pady=file_detection["detect_files_text"]["grid_data"]["pady"],
            sticky=file_detection["detect_files_text"]["grid_data"]["sticky"],
        )
        self.install_files_button = CTkButton(
            master=self.detect_files_frame,
            text=file_detection["install_files_button"]["text"],
            width=float(file_detection["install_files_button"]["width"]),
            height=float(file_detection["install_files_button"]["height"]),
            corner_radius=float(
                file_detection["install_files_button"]["corner_radius"]
            ),
            fg_color=file_detection["install_files_button"]["fg_color"],
            hover_color=file_detection["install_files_button"]["hover_color"],
            text_color=file_detection["install_files_button"]["text_color"],
            font=eval(file_detection["install_files_button"]["font"]),
        )

    def create_recheck_skip_section(self):
        create_section = self.ui_data["create_recheck_skip_section"]

        self.recheck_skip_frame = CTkFrame(
            self.home_page_frame,
            fg_color=create_section["recheck_skip_frame"]["fg_color"],
        )
        self.recheck_skip_frame.grid(
            row=create_section["recheck_skip_frame"]["grid_data"]["row"],
            column=create_section["recheck_skip_frame"]["grid_data"]["column"],
            columnspan=create_section["recheck_skip_frame"]["grid_data"]["columnspan"],
            padx=create_section["recheck_skip_frame"]["grid_data"]["padx"],
            pady=create_section["recheck_skip_frame"]["grid_data"]["pady"],
            sticky=create_section["recheck_skip_frame"]["grid_data"]["sticky"],
        )

        self.check_var = BooleanVar(value=False)
        self.clean_install = CTkCheckBox(
            self.recheck_skip_frame,
            text=create_section["clean_install_checkbox"]["text"],
            text_color=create_section["clean_install_checkbox"]["text_color"],
            onvalue=bool(create_section["clean_install_checkbox"]["onvalue"]),
            offvalue=bool(create_section["clean_install_checkbox"]["offvalue"]),
            variable=self.check_var,
            font=eval(create_section["clean_install_checkbox"]["font"]),
        )

        self.recheck_button = CTkButton(
            self.recheck_skip_frame,
            width=float(create_section["recheck_button"]["width"]),
            height=float(create_section["recheck_button"]["height"]),
            text=create_section["recheck_button"]["text"],
            fg_color=create_section["recheck_button"]["fg_color"],
            image=self.reload_icon,
        )

    def start_loading_animation(self):
        """Start the loading GIF animation."""
        self.frames = self.load_gif()
        self.update_gif(self.frames)

    def stop_loading_animation(self):
        """Stop loading animation, ensuring it's done after threads finish."""
        if self.thread_manager.are_threads_alive():
            self.after(100, self.stop_loading_animation)
        else:
            self._stop_loading_animation()

    def _stop_loading_animation(self):
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
                    file=path.join(self.ASSETS_PATH, self.ui_data["icons"]["block_spin_gif"]),
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
        self.modal_theme = ThemeModal(self, self.base_dir, self.CACHE_PATH)
        self.wait_window(self.modal_theme)
        self.recheck_button.grid_remove()

        if getattr(self.modal_theme, "theme_selected", False):
            self.update_ui_for_selected_theme()
        else:
            self.clear_selection()

    def clear_selection(self):
        self.modal_theme = None
        self.theme_label.configure(text="Select Theme: None")
        self.detect_files_text.configure(
            text="Please Select a Theme",
            fg="#000000",
            image=self.theme_not_selected_icon,
        )
        self.install_button.configure(state="disabled")
        self.install_files_button.grid_remove()


    def update_ui_for_selected_theme(self):
        """Update UI when a theme is selected."""
        updated_ui_data = self.ui_data["update_ui_for_selected_theme"]

        self.install_button.configure(state="disabled")
        
        self.detect_files_text.configure(
        image=self.theme_selected_icon,
        text=updated_ui_data["detect_files_text"]["text"],
        fg=updated_ui_data["detect_files_text"]["fg"],
        )

        self.theme_label.configure(
            text=f"{updated_ui_data["theme_label"]["text"]} {self.modal_theme.theme_selected.title}"
        )
        self.install_files_button.configure(
            command=self.get_theme,
            text=updated_ui_data["install_files_button"]["text"],
            text_color=updated_ui_data["install_files_button"]["text_color"],
            image=None,
            state=updated_ui_data["install_files_button"]["state"],
        )
        self.clean_install.grid(
            row=updated_ui_data["clean_install"]["grid_data"]["row"],
            column=updated_ui_data["clean_install"]["grid_data"]["column"],
            padx=updated_ui_data["clean_install"]["grid_data"]["padx"],
            pady=updated_ui_data["clean_install"]["grid_data"]["pady"],
            sticky=updated_ui_data["clean_install"]["grid_data"]["sticky"], 
        )
        self.install_files_button.grid(pady=updated_ui_data["install_files_button"]["grid_data"]["pady"])

    def run_theme_process(self):
        """Run the theme processing logic."""
        self.theme_data = ThemeDownloader(
            self.modal_theme.theme_selected,
            self.THEME_PATH,
            self.check_var.get(),
            self.base_dir,
        ).process_theme()

        self.stop_loading_animation()
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
        self.detect_files_text.configure(
            text=handle_data_json_theme["detect_files_text"]["text"],
            fg=handle_data_json_theme["detect_files_text"]["fg"],
        )
        self.data_json_path = path.join(self.theme_data.get("path"), "data", "installer_files_data.json")
        self.thread_manager.start_thread(self.fetch_files)
        self.clean_install.grid_remove()

    def handle_userChrome_theme(self):
        """Handle themes that include a userChrome.css file."""
        handle_userChrome_theme = self.ui_data["handle_userChrome_theme"]
        self.detect_files_text.configure(
            text=handle_userChrome_theme["detect_files_text"]["text"],
            fg=handle_userChrome_theme["detect_files_text"]["fg"],
        )
        self.install_button.configure(
            state=handle_userChrome_theme["install_button"]["state"]
        )
        self.recheck_button.configure(
            state=handle_userChrome_theme["recheck_button"]["state"],
            command=self.get_theme)
        self.install_files_button.configure(
            image=self.check_icon,
            text=handle_userChrome_theme["install_files_button"]["text"],
            text_color=handle_userChrome_theme["install_files_button"]["text_color"],
            state=handle_userChrome_theme["install_files_button"]["state"],
            fg_color=handle_userChrome_theme["install_files_button"]["fg_color"],
            width=handle_userChrome_theme["install_files_button"]["width"],
        )       
        self.check_var = BooleanVar(value=False)
        self.recheck_button.grid(
            row=handle_userChrome_theme["recheck_button"]["grid_data"]["row"],
            column=handle_userChrome_theme["recheck_button"]["grid_data"]["column"],
            padx=handle_userChrome_theme["recheck_button"]["grid_data"]["padx"],
            pady=handle_userChrome_theme["recheck_button"]["grid_data"]["pady"],
            sticky=handle_userChrome_theme["recheck_button"]["grid_data"]["sticky"],
        )
        self.clean_install.grid_remove()

    def no_theme_data_found(self):
        """Handle cases where no valid theme data is found."""
        no_theme_data_found = self.ui_data["no_theme_data_found"]
        self.detect_files_text.configure(
            text=no_theme_data_found["detect_files_text"]["text"],
            fg=no_theme_data_found["detect_files_text"]["fg"],
        )
        self.install_files_button.configure(
            image=self.check_icon,
            text=no_theme_data_found["install_files_button"]["text"],
            text_color=no_theme_data_found["install_files_button"]["text_color"],
            state=no_theme_data_found["install_files_button"]["state"],
            fg_color=no_theme_data_found["install_files_button"]["fg_color"],
            width=no_theme_data_found["install_files_button"]["width"],
        )  
        self.install_button.configure(
            state=no_theme_data_found["install_button"]["state"]
        )

    # File handling and animations
    def locate_files(self):
        """Check if all necessary theme files are present."""
        file_check_result = FileManager(self.data_json_path).check_files_exist(
            root=self.theme_data.get("path")
        )
        self.stop_loading_animation()
        if file_check_result:
            self.handle_missing_files()
        else:
            self.handle_all_files_installed()

    def handle_all_files_installed(self):
        """Update UI when all theme files are installed."""
        handle_all_files_installed = self.ui_data["handle_all_files_installed"]
        self.install_files_button.configure(
            width=handle_all_files_installed["install_files_button"]["width"],
            text=handle_all_files_installed["install_files_button"]["text"],
            text_color=handle_all_files_installed["install_files_button"]["text_color"],
            state=handle_all_files_installed["install_files_button"]["state"],
            image=self.check_icon,
        )
        self.install_button.configure(state=handle_all_files_installed["install_button"]["state"])
        self.recheck_button.grid(
            row=handle_all_files_installed["recheck_button"]["grid_data"]["row"],
            column=handle_all_files_installed["recheck_button"]["grid_data"]["column"],
            padx=handle_all_files_installed["recheck_button"]["grid_data"]["padx"],
            pady=handle_all_files_installed["recheck_button"]["grid_data"]["pady"],
            sticky=handle_all_files_installed["recheck_button"]["grid_data"]["sticky"],
        )
        self.clean_install.grid_remove()

    def handle_missing_files(self):
        """Update UI when some theme files are missing."""
        handle_missing_files = self.ui_data["handle_missing_files"]
        self.install_files_button.configure(
            text=handle_missing_files["install_files_button"]["text"],
            text_color=handle_missing_files["install_files_button"]["text_color"],
            state=handle_missing_files["install_files_button"]["state"],
            width=handle_missing_files["install_files_button"]["width"],
            image=self.attention_icon, command=self.install_files
        )
        self.install_files_button.grid(
            row=handle_missing_files["install_files_button"]["grid_data"]["row"],
            column=handle_missing_files["install_files_button"]["grid_data"]["column"],
            padx=handle_missing_files["install_files_button"]["grid_data"]["padx"],
            pady=handle_missing_files["install_files_button"]["grid_data"]["pady"],
            sticky=handle_missing_files["install_files_button"]["grid_data"]["sticky"],
        )
        self.recheck_button.grid(
            row=handle_missing_files["recheck_button"]["grid_data"]["row"],
            column=handle_missing_files["recheck_button"]["grid_data"]["column"],
            padx=handle_missing_files["recheck_button"]["grid_data"]["padx"],
            pady=handle_missing_files["recheck_button"]["grid_data"]["pady"],
            sticky=handle_missing_files["recheck_button"]["grid_data"]["sticky"],
        )

    def install_files(self):
        """Open modal to install missing files and recheck afterward."""
        modal = FileInstallerModal(self, self.base_dir, self.data_json_path, self.theme_data.get("path"))
        self.wait_window(modal)
        self.recheck_files()

    def refetch_files(self):
        """Refetch necessary files and update UI."""
        refetch_files = self.ui_data["refetch_files"]
        self.install_files_button.configure(
            text=refetch_files["install_files_button"]["text"],
            text_color=refetch_files["install_files_button"]["text_color"],
            state=refetch_files["install_files_button"]["state"],
        )
        self.install_button.configure(state=refetch_files["install_button"]["state"])
        self.clean_install.grid_remove()
        self.thread_manager.start_thread(self.fetch_files)

    # Thread and file fetching management
    def get_theme(self):
        """Handle the theme installation process."""
        get_theme = self.ui_data["get_theme"]
        self.start_loading_animation()
        self.get_neccessary_files()
        self.install_files_button.configure(
            text=get_theme["install_files_button"]["text"],
            text_color=get_theme["install_files_button"]["text_color"],
            state=get_theme["install_files_button"]["state"],
        )
        self.detect_files_text.config(
            text=get_theme["detect_files_text"]["text"], fg=get_theme["detect_files_text"]["fg"]
        )
        self.thread_manager.start_thread(self.run_theme_process)

    def get_neccessary_files(self):
        """Fetch and check necessary files for the theme."""
        get_neccessary_files = self.ui_data["get_neccessary_files"]
        self.detect_files_text.config(
            text=get_neccessary_files["detect_files_text"]["text"],
            fg=get_neccessary_files["detect_files_text"]["fg"],
        )
        file_manager = FileManager(json_file_path=self.CUSTOM_SCRIPT_LOADER_PATH, json_file_url=self.ui_data["data_paths"]["CUSTOM_SCRIPT_LOADER_URL"])
        if file_manager.json_data:
            missing_files = file_manager.check_files_exist()
            if missing_files:
                self.thread_manager.start_thread(file_manager.download_missing_files, missing_files, self.CACHE_PATH)


    def fetch_files(self):
        """Fetch files based on data JSON path."""
        fetch_files = self.ui_data["fetch_files"]
        self.start_loading_animation()
        file_manager = FileManager(self.data_json_path)
        self.recheck_button.configure(
            state=fetch_files["recheck_button"]["state"],
            command=self.refetch_files)
        self.recheck_button.grid(
            row=fetch_files["recheck_button"]["grid_data"]["row"],
            column=fetch_files["recheck_button"]["grid_data"]["column"],
            padx=fetch_files["recheck_button"]["grid_data"]["padx"],
            pady=fetch_files["recheck_button"]["grid_data"]["pady"],
            sticky=fetch_files["recheck_button"]["grid_data"]["sticky"],
        )

        if file_manager.json_data:
            self.thread_manager.start_thread(self.locate_files)
        else:
            self.handle_fetch_files_failure()

    def recheck_files(self):
        """Recheck file status and update UI."""
        recheck_files = self.ui_data["recheck_files"]
        self.start_loading_animation()
        self.install_files_button.configure(
            text=recheck_files["install_files_button"]["text"],
            text_color=recheck_files["install_files_button"]["text_color"],
            state=recheck_files["install_files_button"]["state"],
        )
        self.install_button.configure(state="disabled")
        self.clean_install.grid_remove()
        self.thread_manager.start_thread(self.locate_files)

    def handle_fetch_files_failure(self):
        """Handle the failure to fetch files."""
        handle_fetch_files_failure = self.ui_data["handle_fetch_files_failure"]
        self.install_files_button.configure(
            image=self.attention_icon,
            text=handle_fetch_files_failure["install_files_button"]["text"],
            text_color=handle_fetch_files_failure["install_files_button"]["text_color"],
            state=handle_fetch_files_failure["install_files_button"]["state"],
        )
        self.clean_install.grid(
            row=handle_fetch_files_failure["clean_install"]["grid_data"]["row"],
            column=handle_fetch_files_failure["clean_install"]["grid_data"]["column"],
            padx=handle_fetch_files_failure["clean_install"]["grid_data"]["padx"],
            pady=handle_fetch_files_failure["clean_install"]["grid_data"]["pady"],
            sticky=handle_fetch_files_failure["clean_install"]["grid_data"]["sticky"],
        )

    def update_parameters(self, **kwargs):
        # Process and use the parameters as needed
        pass
