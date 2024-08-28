from itertools import cycle
from json import load
from os import path
from pathlib import Path
from tkinter import BooleanVar, PhotoImage, Label, TclError
from threading import Thread
from PIL import Image

from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkCheckBox, CTkImage

from components.create_header import CreateHeader
from components.create_navigation_button import NavigationButton
from functions.get_the_theme_files import ThemeDownloader
from modals.check_files_modal import FileInstallerModal
from modals.info_modals import InfoModals
from functions.get_os_properties import OSProperties
from functions.detect_and_download_files import FileManager
from modals.theme_modal import ThemeModal


class HomePage(CTkFrame):
    ANIMATION_SPEED = 100

    def __init__(self, parent, controller, base_dir):
        super().__init__(parent)

        self.controller = controller
        self.base_dir = base_dir

        self.config_data = self.load_json_data(
            path.join(base_dir, "data", "pages", "home_page_data.json")
        ) 

        self.ASSETS_PATH = path.join(
            base_dir, self.config_data["data_paths"]["ASSETS_PATH"]
        )
        self.NAVIGATION_BUTTON_DATA_PATH = path.join(
            base_dir, self.config_data["data_paths"]["NAVIGATION_BUTTON_DATA_PATH"]
        )
        self.OS_PROPERTIES_PATH = path.join(
            base_dir, self.config_data["data_paths"]["OS_PROPERTIES_PATH"]
        )
        self.THEME_PATH = Path(
            path.expanduser(self.config_data["data_paths"]["THEME_PATH"])
        )
        self.CUSTOM_SCRIPT_LOADER_PATH = path.join(
            base_dir, self.config_data["data_paths"]["CUSTOM_SCRIPT_LOADER_PATH"]
        )

        # Load additional data
        self.navigation_button_data = self.load_json_data(
            self.NAVIGATION_BUTTON_DATA_PATH
        )
        self.button_data = self.navigation_button_data["navigation_buttons"]
        self.os_values = OSProperties(self.OS_PROPERTIES_PATH).get_values()
        self.navigation_button = NavigationButton(self.button_data)
        self.header = CreateHeader()

        # Initialize variables
        self.data_json_path = None
        self.modal_theme = None
        self.theme_data = None

        # Configure layout and create widgets
        self.configure_layout()
        self.create_widgets()

    def load_json_data(self, path):
        with open(path, "r") as file:
            return load(file)

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
        # Load icons and images based on JSON paths
        icons = self.config_data["icons"]
        self.attention_icon = CTkImage(
            light_image=Image.open(
                path.join(self.ASSETS_PATH, icons["attention_icon"])
            ),
            dark_image=Image.open(path.join(self.ASSETS_PATH, icons["attention_icon"])),
            size=(24, 24),
        )
        self.check_icon = CTkImage(
            light_image=Image.open(path.join(self.ASSETS_PATH, icons["check_icon"])),
            dark_image=Image.open(path.join(self.ASSETS_PATH, icons["check_icon"])),
            size=(24, 24),
        )
        self.install_files_icon = CTkImage(
            light_image=Image.open(
                path.join(self.ASSETS_PATH, icons["install_files_icon"])
            ),
            dark_image=Image.open(
                path.join(self.ASSETS_PATH, icons["install_files_icon"])
            ),
            size=(24, 24),
        )
        self.theme_not_selected_icon = PhotoImage(
            file=path.join(self.ASSETS_PATH, icons["theme_not_selected_icon"]),
            height=32,
            width=24,
        )
        self.theme_selected_icon = PhotoImage(
            file=path.join(self.ASSETS_PATH, icons["theme_selected_icon"]),
            height=32,
            width=24,
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
        self.select_action_img = CTkImage(
            light_image=Image.open(
                path.join(self.ASSETS_PATH, icons["header_title_bg"])
            ),
            dark_image=Image.open(
                path.join(self.ASSETS_PATH, icons["header_title_bg"])
            ),
            size=(270, 36),
        )
        self.reload_icon = CTkImage(
            light_image=Image.open(path.join(self.ASSETS_PATH, icons["reload_icon"])),
            dark_image=Image.open(path.join(self.ASSETS_PATH, icons["reload_icon"])),
            size=(24, 24),
        )

    def create_header(self):
        self.header.create_header(
            self.home_page_frame, self.header_title_bg, self.line_top_img
        )

    def create_os_info(self):
        os_info = self.config_data["create_os_info"]

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
        theme_select = self.config_data["theme_select"]

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

        navigation_buttons = self.config_data["create_navigation_buttons"]

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
            path.join(self.ASSETS_PATH, "icons/remove_icon.png"),
            lambda: self.controller.show_frame("remove_page"),
            padding_x=(10, 20),
            side="right",
        )
        self.install_button = self.navigation_button.create_navigation_button(
            navigation_frame,
            "Install",
            path.join(self.ASSETS_PATH, "icons/install_icon.png"),
            lambda: self.controller.show_frame(
                "install_page",
                theme_dir=(
                    self.theme_data.get("path")
                    if self.theme_data.get("type") == "userChrome.css"
                    else path.join(self.base_dir, "chrome")
                ),
            ),
            padding_x=(5, 5),
            side="right",
            state="disabled",
        )
        self.navigation_button.create_navigation_button(
            navigation_frame,
            "Exit",
            path.join(self.ASSETS_PATH, "icons/exit_icon.png"),
            lambda: InfoModals(self, self.base_dir, "Exit"),
            padding_x=(20, 10),
            side="left",
        )

    def create_file_detection(self):

        file_detection = self.config_data["create_file_detection"]

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
        create_section = self.config_data["create_recheck_skip_section"]

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
        self.frames = self.load_gif()  # Load the GIF frames
        self.update_gif(self.frames)  # Start the GIF animation

    def stop_loading_animation(self):
        if hasattr(self, "animation_id"):
            self.after_cancel(self.animation_id)  # Stop the GIF animation
            self.detect_files_text.config(
                image=""
            )  # Clear the image to stop displaying the GIF

    def load_gif(self):
        frames = []
        index = 0
        while True:
            try:
                frame = PhotoImage(
                    file=path.join(self.ASSETS_PATH, "icons/block_spin.gif"),
                    format=f"gif -index {index}",
                )
                frames.append(frame)
                index += 2
            except TclError:
                break
        return cycle(frames)

    def update_gif(self, frames):
        frame = next(frames)
        self.detect_files_text.config(image=frame)
        self.animation_id = self.after(self.ANIMATION_SPEED, self.update_gif, frames)

    def select_theme(self):
        self.modal_theme = ThemeModal(self, self.base_dir)
        self.wait_window(self.modal_theme)
        self.recheck_button.grid_remove()

        if (
            hasattr(self.modal_theme, "theme_selected")
            and self.modal_theme.theme_selected
        ):
            self.detect_files_text.configure(
                text="Theme Selected ", image=self.theme_selected_icon, fg="#000000"
            )
            self.theme_label.configure(
                text=f"Select Theme: {self.modal_theme.theme_selected.title}"
            )
            self.install_files_button.configure(
                text="Install Theme",
                state="normal",
                command=self.get_theme,
                text_color="#000000",
                image=None,
            )
            self.clean_install.grid(row=7, column=0, padx=10, pady=10, sticky="")
            self.install_files_button.grid(pady=10)
            self.install_button.configure(state="disabled")
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
            if theme_type == "data":
                self.handle_data_json_theme()
            elif theme_type == "userChrome.css":
                self.handle_userChrome_theme()
            else:
                self.no_theme_data_found()
        else:
            self.no_theme_data_found()

    def handle_data_json_theme(self):
        self.detect_files_text.configure(
            text="Theme has its own data JSON", fg="#00FF00"
        )
        self.data_json_path = self.theme_data.get("path")
        thread = Thread(target=self.fetch_files)
        thread.start()
        self.clean_install.grid_remove()

    def handle_userChrome_theme(self):
        self.detect_files_text.configure(
            text="Theme has userChrome.css file", fg="#00FF00"
        )
        self.install_button.configure(state="normal")
        self.recheck_button.configure(state="normal", command=self.get_theme)
        self.install_files_button.configure(
            text="Installed",
            fg_color="#D9D9D9",
            state="disabled",
            image=self.check_icon,
            text_color="#000000",
        )
        self.check_var = BooleanVar(value=False)
        self.recheck_button.grid(row=1, column=0, padx=10, pady=0, sticky="")
        self.clean_install.grid_remove()

    def no_theme_data_found(self):
        self.detect_files_text.configure(
            text="No theme data or chrome/userChrome.css found",
            fg="#FF0000",
        )
        self.install_files_button.configure(
            text="Installed",
            fg_color="#D9D9D9",
            state="disabled",
            image=self.check_icon,
            text_color="#000000",
        )
        self.install_button.configure(state="disabled")

    def handle_fetch_files_failure(self):
        self.install_files_button.configure(
            text="Failed to Fetch Files Data",
            text_color="#f04141",
            image=self.attention_icon,
        )
        self.clean_install.grid(row=7, column=0, padx=10, pady=10, sticky="")
        self.install_files_button.configure(state="disabled")

    def locate_files(self):
        file_check_result = FileManager(self.data_json_path).check_files_exist(
            root=self.base_dir
        )

        if file_check_result:
            self.handle_missing_files()
        else:
            self.handle_all_files_installed()

    def handle_all_files_installed(self):
        self.install_files_button.configure(
            text="All Files Installed",
            text_color="#10dc60",
            image=self.check_icon,
            state="disabled",
        )
        self.install_button.configure(state="normal")
        self.recheck_button.grid(row=7, column=1, padx=0, pady=10, sticky="")
        self.clean_install.grid_remove()

    def handle_missing_files(self):
        self.install_files_button.configure(
            text="Some Files Are Missing",
            text_color="#f04141",
            image=self.attention_icon,
            command=self.install_files,
            state="normal",
        )
        self.install_files_button.grid(row=2, column=0, padx=10, pady=10, sticky="")
        self.recheck_button.grid(row=7, column=1, padx=0, pady=10, sticky="")

    def install_files(self):
        modal = FileInstallerModal(self, self.base_dir)
        self.wait_window(modal)
        self.recheck_files()

    def refetch_files(self):
        self.install_files_button.configure(
            text="Fetching The Files", text_color="#000000", state="disabled"
        )
        self.install_button.configure(state="disabled")
        self.clean_install.grid_remove()
        thread = Thread(target=self.fetch_files)
        thread.start()

    def get_theme(self):
        """Handle the theme installation process."""
        self.start_loading_animation()  # Start the loading GIF
        self.get_neccessary_files()
        self.install_files_button.configure(
            text="Installing Files", text_color="#000000", state="disabled"
        )
        self.detect_files_text.config(text="Installing Theme Files", fg="#000000")
        thread = Thread(target=self.run_theme_process)
        thread.start()
        self.check_thread(thread)

    def get_neccessary_files(self):
        # Disable the button and change the text
        self.detect_files_text.config(text="Installing Necessary Files", fg="#000000")
        custom_script_loader = FileManager(
            self.CUSTOM_SCRIPT_LOADER_PATH
        ).load_json_data()

        if custom_script_loader:
            missing_files = FileManager(
                self.CUSTOM_SCRIPT_LOADER_PATH
            ).check_files_exist(custom_script_loader)
            if missing_files:
                thread = Thread(
                    target=FileManager(
                        self.CUSTOM_SCRIPT_LOADER_PATH
                    ).download_missing_files,
                    args=(missing_files,),
                )
                thread.start()
                self.check_thread(thread)
            else:
                # print("All necessary files are already present.")
                self.stop_loading_animation()
        else:
            # print("Failed to load custom script loader data.")
            self.stop_loading_animation()

    def check_thread(self, thread):
        """Check if the thread is finished and update the UI accordingly."""
        if thread.is_alive():
            self.after(100, self.check_thread, thread)
        else:
            self.stop_loading_animation()  # Stop the loading GIF

    def fetch_files(self):
        self.start_loading_animation()  # Start the loading GIF
        fetch_files_data = FileManager(self.data_json_path).load_json_data()
        self.recheck_button.configure(state="normal", command=self.refetch_files)
        self.recheck_button.grid(
            row=1, column=0, padx=0, pady=5, columnspan=2, sticky=""
        )

        if fetch_files_data:
            thread = Thread(target=self.locate_files)
            thread.start()
            self.check_thread(thread)
        else:
            self.handle_fetch_files_failure()
            self.stop_loading_animation()  # Stop the loading GIF

    def recheck_files(self):
        self.start_loading_animation()  # Start the loading GIF
        self.install_files_button.configure(
            text="Checking The Files", text_color="#000000", state="disabled"
        )
        self.install_button.configure(state="disabled")
        self.clean_install.grid_remove()
        thread = Thread(target=self.locate_files)
        thread.start()
        self.check_thread(thread)

    def update_parameters(self, **kwargs):
        # Process and use the parameters as needed
        pass
