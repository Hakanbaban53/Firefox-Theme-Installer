from os import path
from customtkinter import CTkFrame, CTkLabel, CTkButton

from installer_core.component_tools.thread_manager import ThreadManager
from installer_core.data_tools.get_theme_data import Theme
from installer_core.data_tools.load_json_data import LoadJsonData
from modals.theme_detail_modal import ThemeDetailModal


class DetectInstalledTheme:
    def __init__(self, parent, chrome_folder, theme_detected_icon, base_dir, app_language):
        self.json_loader = LoadJsonData(json_file_url=None)
        UI_DATA_PATH = path.join(
            base_dir, "data", "components", "detect_installed_theme", "language", "tr.json"
        )
        self.ui_data = self.json_loader.load_json_data(UI_DATA_PATH)

        self.app_language = app_language
        self.thread_manager = ThreadManager()
        self.parent = parent
        self.chrome_folder = chrome_folder
        self.theme_data_path = path.join(self.chrome_folder, "selected_theme_data.json")
        self.theme_detected_icon = theme_detected_icon
        self.base_dir = base_dir
        self.theme_data = None
        self.installed_themes_label = None

    def create_installed_themes(self, preview_and_check_installed_theme_frame):
        installed_themes_data = self.ui_data

        installed_themes_frame = CTkFrame(
            preview_and_check_installed_theme_frame,
            width=440,
            height=60,
            corner_radius=12,
            fg_color="#FFFFFF",
        )
        installed_themes_frame.grid(
            row=0,
            column=0,
            padx=10,
            pady=0,
            sticky="",
        )

        self.installed_themes_label = CTkLabel(
            installed_themes_frame,
            text=installed_themes_data["installed_themes_label"]["text"],
            text_color="#000000",
            font=("Arial", 18, "bold"),
            compound="right",
        )
        self.installed_themes_label.pack(
            padx=(10, 4),
            pady=10,
            side="top",
        )

        self.theme_details_button = CTkButton(
            installed_themes_frame,
            text=installed_themes_data["theme_details_button"]["text"],
            height=42,
            fg_color="#D9D9D9",
            hover_color="#EEEEEE",
            corner_radius=10,
            text_color="#000000",
            compound="right",
            font=("Arial", 16, "bold"),
            image=self.theme_detected_icon,
            command=lambda: ThemeDetailModal(
                self.parent,
                theme=self.theme_data,
                base_dir=self.base_dir,
                app_language=self.app_language
            ),
        )

    def detect_installed_theme(self):
        # Start the detection in a separate thread
        self.thread_manager.start_thread(
            target=self._detect_installed_theme, on_finish=self.update_ui
        )

    def _detect_installed_theme(self):
        # Check if the chrome folder exists
        if path.exists(self.chrome_folder):
            # Check for the theme data file
            if path.isfile(self.theme_data_path):
                try:
                    theme_data = self.json_loader.load_json_data(self.theme_data_path)
                    if theme_data:
                        self.theme_data = Theme(**theme_data)
                        if self.theme_data.title:
                            return self.theme_data.title
                        else:
                            return False
                except Exception:
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

    def update_ui(self):
        # Use the Tkinter `after` method to safely update the UI from the main thread
        result = self._detect_installed_theme()  # Get the result

        def update_label():
            update_label_data = self.ui_data["update_ui"]
            if result is True:
                self.installed_themes_label.configure(
                    text=update_label_data["installed_themes_label_unkown"]
                )
            elif result is False:
                self.installed_themes_label.configure(
                    text=update_label_data["installed_themes_label_no_theme"]
                )
            else:
                self.installed_themes_label.configure(
                    text=update_label_data["installed_themes_label_theme"]
                    + f"{result} "
                )
                self.theme_details_button.pack(padx=10, pady=10, side="bottom")

        # Call the update function after a delay to ensure it's on the main thread
        self.installed_themes_label.after(0, update_label)
        return result
