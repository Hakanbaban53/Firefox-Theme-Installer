from os import path, name
from tkinter import Toplevel, Label, Frame
from tkinter import ttk
from threading import Thread
from PIL import Image, ImageTk
from customtkinter import CTkButton
from components.set_window_icon import SetWindowIcon
from functions.detect_and_download_files import FileManager
from modals.info_modals import InfoModals
from functions.load_json_data import LoadJsonData


class FileInstallerModal(Toplevel):
    def __init__(self, parent, base_dir, theme_dir):
        super().__init__(parent)
        # Load the UI data from the JSON file
        UI_DATA_PATH = path.join(
            base_dir, "data", "modals", "check_files_modal_data.json"
        )
        load_json_data = LoadJsonData()
        self.ui_data = load_json_data.load_json_data(UI_DATA_PATH)
        
        self.file_manager = FileManager(theme_dir)
        self.title(self.ui_data["FileInstallerModal"]["title"])

        self.base_dir = base_dir
        self.theme_dir = theme_dir

        self.configure_layout(parent)
        self.center_window()
        self.create_widgets()

    def configure_layout(self, parent):
        """Configure the layout of the modal."""
        self.transient(parent)
        self.configure(bg="#2B2631")
        self.resizable(False, False)
        self.wait_visibility()
        self.grab_set()
        icon_setter = SetWindowIcon(self.base_dir)
        icon_setter.set_window_icon(self)

    def create_widgets(self):
        """Create and arrange the widgets in the modal."""
        modal_config = self.ui_data["FileInstallerModal"]

        self.files_modal_frame = Frame(self, bg="#2B2631")
        self.files_modal_frame.pack(padx=20, pady=10)

        self.missing_files_label = Label(
            master=self.files_modal_frame,
            text=modal_config["missing_files_label"],
            fg="#FFFFFF",
            bg="#2B2631",
            font=("Arial", 16, "bold"),
        )
        self.missing_files_label.grid(row=0, column=0, padx=0, pady=(10, 20))

        # Create treeview
        self.treeview = ttk.Treeview(master=self.files_modal_frame)
        self.treeview.grid(row=1, column=0, padx=20, pady=0)

        # Define columns dynamically from JSON
        for i, col in enumerate(modal_config["tree_view_columns"]):
            self.treeview["columns"] = (f"#{i}",)
            self.treeview.column(f"#{i}", width=col["width"])
            # Define headings
            self.treeview.heading(f"#{i}", text=col["header"], anchor="w")

        # Add dictionary items to treeview
        for folder, files in self.check_all_files_installed().items():
            folder_id = self.treeview.insert("", "end", text=folder)
            for file in files:
                self.treeview.insert(folder_id, "end", text="", values=(file,))

        self.buttons_frame = Frame(master=self.files_modal_frame, bg="#2B2631")
        self.buttons_frame.grid(row=3, column=0, columnspan=2, padx=0, pady=(20, 10))

        self.check_button = CTkButton(
            master=self.buttons_frame,
            text=modal_config["buttons"]["check_button"],
            text_color="white",
            command=self.on_check_button_click,
            fg_color="#771D76",
        )
        self.check_button.grid(row=0, column=0, padx=20, pady=0)

        self.install_files_button = CTkButton(
            master=self.buttons_frame,
            text=modal_config["buttons"]["install_button"],
            text_color="white",
            command=self.on_install_button_click,
            fg_color="#F08D27",
        )
        self.install_files_button.grid(row=0, column=1, padx=20, pady=0)

    def check_all_files_installed(self):
        """Check if all files are installed and return the missing files."""
        self.file_check_result = self.file_manager.check_files_exist(root=self.base_dir)
        return self.file_check_result

    def on_install_button_click(self):
        """Handle the install button click event."""
        self.install_files_button.configure(text="Installing", state="disabled")
        thread = Thread(target=self.start_download_process)
        thread.start()
        self.after(100, self.check_thread, thread)

    def check_thread(self, thread):
        """Check if the thread is finished and update the UI accordingly."""
        if thread.is_alive():
            self.after(100, self.check_thread, thread)
        else:
            self.install_files_button.configure(text="Installed", fg_color="#D9D9D9")

    def start_download_process(self):
        """Download missing files."""
        try:
            missing_files = self.check_all_files_installed()
            self.file_manager.download_missing_files(missing_files)
        except Exception as e:
            print(f"Error during download process: {e}")

    def on_check_button_click(self):
        """Handle the check button click event."""
        all_files_installed = len(self.check_all_files_installed())
        if all_files_installed == 0:
            modal = InfoModals(self, self.base_dir, "check_files_installed")
            self.wait_window(modal)
            self.destroy()
        else:
            InfoModals(self, self.base_dir, "check_files_not_installed")

    def center_window(self):
        """Center the modal window on the screen."""
        self.update_idletasks()
        window_width = self.winfo_width()
        window_height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry("+{}+{}".format(x, y))
