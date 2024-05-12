from threading import Thread
import customtkinter
from tkinter import messagebox, ttk
from functions.detect_files import FileManager
from modals.combined_modal import CombinedModal


class FileInstallerModal(customtkinter.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color="#2B2631")
        self.resizable(False, False)
        self.wait_visibility()
        self.grab_set()
        self.title("Install Missing Files")

        self.file_manager = FileManager(
            "../RealFire_Installer/data/installer_files_data.json"
        )
        self.file_check_result = self.file_manager.check_files_exist()  # Missing files
        self.create_widgets()

    def create_widgets(self):

        self.files_modal_frame = customtkinter.CTkFrame(self, fg_color="#2B2631")
        self.files_modal_frame.pack(padx=20, pady=10)

        self.missing_files_label = customtkinter.CTkLabel(
            master=self.files_modal_frame,
            text="Some Files Are Missing. Do you want to Install?",
            text_color="#FFFFFF",
            font=("Arial", 16, "bold"),
        )
        self.missing_files_label.grid(row=0, column=0, padx=0, pady=(10, 20))

        treeview = ttk.Treeview(
            master=self.files_modal_frame,
        )
        treeview.grid(row=1, column=0, padx=20, pady=0)

        # Sütunları tanımla
        treeview["columns"] = ("File(s) Name",)
        treeview.column("#0")
        treeview.column("File(s) Name", anchor="w")

        # Başlıkları tanımla
        treeview.heading("#0", text="Folder(s) Name", anchor="w")
        treeview.heading("File(s) Name", text="File(s) Name", anchor="w")

        # Sözlük elemanlarını treeview'a ekle
        for kategori, dosyalar in self.file_check_result.items():
            kategori_id = treeview.insert("", "end", text=kategori)
            for dosya in dosyalar:
                treeview.insert(kategori_id, "end", text="", values=(dosya,))

        self.user_know_what_do = customtkinter.CTkCheckBox(
            master=self.files_modal_frame,
            text="I know what I do",
            text_color="#FFFFFF",
            font=("Arial", 16, "bold"),
        )
        self.user_know_what_do.grid(row=2, column=0, padx=0, pady=(20, 10))

        self.buttons_frame = customtkinter.CTkFrame(
            master=self.files_modal_frame, fg_color="#2B2631"
        )
        self.buttons_frame.grid(row=3, column=0, padx=0, pady=(20, 10))

        self.check_button = customtkinter.CTkButton(
            master=self.buttons_frame,
            text="Check",
            text_color="white",
            command=self.on_next_button_click,
            bg_color="#2B2631",
            fg_color="#f04141",
        )
        self.check_button.grid(row=0, column=0, padx=20, pady=0)

        self.install_files_button = customtkinter.CTkButton(
            master=self.buttons_frame,
            text="Install",
            text_color="white",
            command=self.on_install_button_click,
            bg_color="#2B2631",
            fg_color="#10dc60",
        )
        self.install_files_button.grid(row=0, column=1, padx=20, pady=0)

    def check_all_files_installed(self):
        return len(self.file_check_result) == 0

    def on_install_button_click(self):
        self.install_files_button.configure(text="Installing", state="disabled")
        self.file_manager.check_and_download()
        self.install_files_button.configure(text="Installed", fg_color="#D9D9D9")

    def on_next_button_click(self):
        all_files_installed = self.check_all_files_installed()
        if all_files_installed:
            CombinedModal(self, "Exit")
            # Here you would add your code to go to the next page of the installer
        else:
            self.destroy()
