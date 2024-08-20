from json import load
from os import path
from pathlib import Path
from tkinter import PhotoImage, Label
from threading import Thread

from customtkinter import (
    CTkFrame,
    CTkImage,
    CTkLabel,
    CTkButton,
    StringVar,
    CTkCheckBox,
)
from PIL import Image

from functions.get_the_theme_files import ThemeDownloader
from functions.get_theme_data import ThemeManager
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

        # Define paths
        self.ICON_PATH = path.join(base_dir, "assets", "icons")
        self.BACKGROUND_PATH = path.join(base_dir, "assets", "backgrounds")
        self.THEMES_DATA_PATH = path.join(base_dir, "data", "themes.json")
        self.DATA_PATH = path.join(base_dir, "data", "installer_data.json")
        self.THEME_PATH = Path(path.expanduser("~")) / ".cache" / "RealFire" / "Themes"

        # Load data
        self.text_data = self.load_json_data(self.DATA_PATH)
        self.button_data = self.text_data.get("common_values")["navigation_buttons"]
        self.theme_manager = ThemeManager(self.THEMES_DATA_PATH)
        self.os_values = OSProperties(self.DATA_PATH).get_values()

        # Initialize variables
        self.data_json_path = None
        self.modal_theme = None

        # Load icons and images
        self.attention_icon = PhotoImage(
            file=path.join(self.ICON_PATH, "attention.png"), height=24, width=24
        )
        self.check_icon = PhotoImage(
            file=path.join(self.ICON_PATH, "check.png"), height=20, width=20
        )
        self.install_files_icon = self.load_image(
            path.join(self.ICON_PATH, "get_from_internet.png"), (24, 24)
        )
        # Configure layout and create widgets
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
        home_page_frame = CTkFrame(
            self,
            fg_color="#2B2631",
        )
        home_page_frame.grid(row=0, column=1, sticky="SW")
        home_page_frame.columnconfigure(0, weight=1)
        self.home_page_frame = home_page_frame

    def create_widgets(self):
        self.create_header()
        self.create_os_info()
        self.theme_select()
        self.create_navigation_buttons()
        self.create_file_detection()
        self.create_recheck_skip_section()

    def create_header(self):
        header_title_bg = self.load_image(
            path.join(self.BACKGROUND_PATH, "header_title_background.png"), (390, 64)
        )
        line_top_img = self.load_image(
            path.join(self.BACKGROUND_PATH, "line_top.png"), (650, 6)
        )

        header_label = CTkLabel(
            self.home_page_frame,
            text="Welcome to the RealFire Installer",
            image=header_title_bg,
            text_color="White",
            font=("Inter", 22, "bold"),
        )
        header_label.grid(
            row=0, column=0, columnspan=2, padx=203, pady=(35, 0), sticky="NSEW"
        )

        line_top_label = CTkLabel(self.home_page_frame, text="", image=line_top_img)
        line_top_label.grid(
            row=1, column=0, columnspan=2, padx=10, pady=10, sticky="NSEW"
        )

    def create_os_info(self):
        os_icon_image = self.load_image(
            path.join(self.ICON_PATH, f"{self.os_values['os_name'].lower()}.png"),
            (20, 24),
        )

        os_label = CTkLabel(
            self.home_page_frame,
            text="Detected Operating System: ",
            text_color="White",
            font=("Inter", 20, "bold"),
        )
        os_label.grid(row=2, column=0, padx=(175, 0), pady=20, sticky="ew")

        os_frame = CTkFrame(self.home_page_frame, corner_radius=12, fg_color="white")
        os_frame.grid(row=2, column=1, padx=(0, 185), sticky="ew")

        os_info_label = CTkLabel(
            os_frame,
            text=f"{self.os_values['os_name']} ",
            text_color=self.os_values["os_color"],
            font=("Arial", 20, "bold"),
            image=os_icon_image,
            compound="right",
        )
        os_info_label.pack(padx=10, pady=10, side="left")

    def theme_select(self):
        theme_frame = CTkFrame(
            self.home_page_frame,
            corner_radius=12,
            fg_color="white",
            border_color="#771D76",
            border_width=4,
        )
        theme_frame.grid(row=3, column=0, columnspan=2, pady=(10, 35), sticky="")

        self.theme_label = CTkLabel(
            theme_frame,
            text="Select Theme: None",
            text_color="Black",
            font=("Inter", 18),
        )
        self.theme_label.pack(padx=10, pady=10, side="left")

        theme_select = CTkButton(
            theme_frame,
            text="Change Theme",
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
        theme_select.pack(padx=10, pady=10, side="right")

    def create_navigation_buttons(self):
        select_action_img = self.load_image(
            path.join(self.BACKGROUND_PATH, "header_title_background.png"), (270, 36)
        )

        select_action_label = CTkLabel(
            self.home_page_frame,
            text="Please Select the Action",
            image=select_action_img,
            text_color="White",
            font=("Inter", 20, "bold"),
        )
        select_action_label.grid(row=4, column=0, columnspan=2, padx=60, pady=(0,15), sticky="ew")

        navigation_frame = CTkFrame(
            self.home_page_frame,
            width=460,
            height=54,
            corner_radius=12,
            border_width=4,
            fg_color="white",
            border_color="#F89F24",
        )
        navigation_frame.grid(row=5, column=0, columnspan=2, pady=(0,15), sticky="")

        self.create_navigation_button(
            navigation_frame,
            "Remove",
            path.join(self.ICON_PATH, "remove_icon.png"),
            lambda: self.controller.show_frame("remove_page"),
            padding_x=(10, 20),
            side="right",
        )
        self.install_button = self.create_navigation_button(
            navigation_frame,
            "Install",
            path.join(self.ICON_PATH, "install_icon.png"),
            lambda: self.controller.show_frame("install_page"),
            padding_x=(5, 5),
            side="right",
            state="disabled",
        )
        self.create_navigation_button(
            navigation_frame,
            "Exit",
            path.join(self.ICON_PATH, "exit_icon.png"),
            lambda: InfoModals(self, self.base_dir, "Exit"),
            padding_x=(20, 10),
            side="left",
        )

    def create_navigation_button(
        self,
        parent,
        text,
        image_path,
        command,
        padding_x,
        side,
        img_side="left",
        **kwargs,
    ):
        button_image = self.load_image(image_path, (20, 20))
        button = CTkButton(
            parent,
            width=float(self.button_data["width"]),
            height=float(self.button_data["height"]),
            corner_radius=float(self.button_data["corner_radius"]),
            bg_color=self.button_data["bg_color"],
            fg_color=self.button_data["fg_color"],
            hover_color=self.button_data["hover_color"],
            text_color=self.button_data["text_color"],
            font=(self.button_data["font_family"], int(self.button_data["font_size"])),
            image=button_image,
            text=text,
            compound=img_side,
            command=command,
            **kwargs,
        )
        button.pack(padx=padding_x, pady=10, side=side)
        return button

    def create_file_detection(self):
        self.detect_files_frame = CTkFrame(
            self.home_page_frame, corner_radius=12, fg_color="white"
        )
        self.detect_files_frame.grid(row=6, column=0, padx=0, columnspan=2, sticky="")

        self.detect_files_text = Label(
            self.detect_files_frame,
            text="Please Select theme ",
            fg="#000000",
            bg="#FFFFFF",
            font=("Arial", 16, "bold"),
            compound="right",
        )
        self.detect_files_text.grid(row=0, column=0, padx=10, pady=10, sticky="")

        self.install_files_button = CTkButton(
            master=self.detect_files_frame,
            text="Show Files",
            width=float(self.button_data["width"]),
            height=float(self.button_data["height"]),
            corner_radius=float(self.button_data["corner_radius"]),
            bg_color=self.button_data["bg_color"],
            fg_color=self.button_data["fg_color"],
            hover_color=self.button_data["hover_color"],
            text_color=self.button_data["text_color"],
            font=(self.button_data["font_family"], int(self.button_data["font_size"])),
            command=self.get_theme,
            image=self.install_files_icon,
            state="disabled",
        )

    def create_recheck_skip_section(self):
        self.recheck_skip_frame = CTkFrame(self.home_page_frame, fg_color="#2B2631")
        self.recheck_skip_frame.grid(
            row=7, column=0, padx=0, pady=0, columnspan=2, sticky=""
        )

        self.check_var = StringVar(value="off")
        self.user_know_what_do = CTkCheckBox(
            self.recheck_skip_frame,
            text="I know what I do",
            text_color="#FFFFFF",
            font=("Arial", 16, "bold"),
            variable=self.check_var,
            onvalue="on",
            offvalue="off",
        )

        reload_icon = self.load_image(
            path.join(self.ICON_PATH, "reload_icon.png"), (20, 20)
        )
        self.recheck_button = CTkButton(
            self.recheck_skip_frame,
            width=40,
            height=40,
            text="",
            fg_color="#FFFFFF",
            command=self.refetch_files,
            image=reload_icon,
        )

    def select_theme(self):
        self.modal_theme = ThemeModal(self, self.theme_manager, self.base_dir)
        self.wait_window(self.modal_theme)

        if hasattr(self.modal_theme, 'theme_selected') and self.modal_theme.theme_selected:
            self.theme_label.configure(text=f"Select Theme: {self.modal_theme.theme_selected.title}")
            self.install_files_button.configure(text="Install Files", state="normal")
            self.install_files_button.grid()
        else:
            self.modal_theme = None
            self.theme_label.configure(text="Select Theme: None")
            self.detect_files_text.configure(
                text="Please Select theme ", fg="#000000"
            )
            self.install_button.configure(state="disabled")
            self.install_files_button.grid_remove()

    def get_theme(self):
        self.detect_files_text.configure(
            text="Installing Files ", fg="#000000"
        )
        self.install_files_button.grid_remove()
        handler = ThemeDownloader(self.modal_theme.theme_selected, self.THEME_PATH)
        test = handler.process_theme()
        
        if isinstance(test, dict) and test.get('type') == "data":
            self.detect_files_text.configure(
                text="Theme has its own data JSON", fg="#00FF00", image=self.check_icon
            )
            self.data_json_path = test.get('path')
            thread = Thread(target=self.fetch_files())
            thread.start()


        elif isinstance(test, dict) and test.get('type') == 'userChrome.css':
            self.detect_files_text.configure(
                text="Theme has userChrome.css file", fg="#00FF00", image=self.check_icon
            )
            self.install_button.configure(state="normal")
        else:
            self.detect_files_text.configure(
                text="No theme data or chrome/userChrome.css found.", fg="#FF0000", image=self.attention_icon
            )
            self.install_button.configure(state="disabled")

    def fetch_files(self):
        fetch_files_data = FileManager(self.data_json_path).load_json_data()
        if fetch_files_data == {}:
            self.install_files_button.configure(
                text="Failed to Fetch Files Data  ", text_color="#f04141", image=self.attention_icon
            )
            self.install_files_button.configure(state="disabled")
            self.recheck_button.configure(state="normal")
            self.user_know_what_do.grid(row=1, column=0, padx=10, pady=0, sticky="")
            self.recheck_button.grid(row=1, column=0, padx=0, pady=5, columnspan=2, sticky="")
        else:
            Thread(target=self.locate_files ).start()


    def locate_files(self):
        file_check_result = FileManager(self.data_json_path).check_files_exist(root=self.base_dir)
        if not file_check_result:
            self.install_files_button.configure(
                text="All Files Installed  ", text_color="#10dc60", image=self.check_icon
            )
            self.install_files_button.configure(state="disabled")
            self.install_button.configure(state="normal")
            self.recheck_button.grid(row=6, column=0, padx=0, pady=0, sticky="")
            self.user_know_what_do.grid_remove()
        else:
            self.install_files_button.configure(
                text="Some Files Are Missing  ", text_color="#f04141", image=self.attention_icon, command=self.install_files
            )
            self.install_files_button.configure(state="normal")
            self.install_files_button.grid(row=2, column=0, padx=10, pady=10, sticky="")
            self.user_know_what_do.grid(row=7, column=0, padx=10, pady=0, sticky="")
            self.recheck_button.grid(row=7, column=1, padx=10, pady=0, sticky="")

    def install_files(self):
        modal = FileInstallerModal(self, self.base_dir)
        self.wait_window(modal)
        self.recheck_files()

    def refetch_files(self):
        self.install_files_button.configure(text="Fetching The Files  ", text_color="#000000", state="disabled")
        self.install_button.configure(state="disabled")
        self.user_know_what_do.grid_remove()
        thread = Thread(target=self.fetch_files)
        thread.start()

    def recheck_files(self):
        self.install_files_button.configure(text="Checking The Files  ", text_color="#000000", state="disabled")
        self.install_button.configure(state="disabled")
        self.user_know_what_do.grid_remove()
        thread = Thread(target=self.locate_files)
        thread.start()

    def update_parameters(self, **kwargs):
        # Process and use the parameters as needed
        pass