import os
import subprocess
from os import path

from functions.install_files import FileActions


class PreviewTheme:
    def __init__(
        self,
        base_dir,
        theme_dir,
        temp_profile_folder,
        os_name,
        CSL,
        profile_folder,
        application_folder,
        progress_bar=None,
        output_entry=None,
    ):
        self.application_folder = application_folder
        self.profile_folder = profile_folder
        self.custom_script_loader = CSL
        self.base_dir = base_dir
        self.theme_dir = theme_dir
        self.temp_profile_folder = temp_profile_folder
        self.os_name = os_name
        self.chrome_folder = path.join(self.temp_profile_folder, "chrome")
        self.file_actions = FileActions(os_name)
        self.progress_bar = progress_bar
        self.output_entry = output_entry
        print(self.application_folder)

    def copy_files(self):
        self.cleanup()  # Ensure no leftover profile folder
        os.makedirs(
            self.temp_profile_folder, exist_ok=True
        )  # Create the profile folder
        os.makedirs(
            self.chrome_folder, exist_ok=True
        )  # Ensure the chrome folder exists

        subprocess.run(
            [
                "firefox",
                "-CreateProfile",
                f"temp_theme_profile {self.temp_profile_folder}",
            ]
        )

        print(self.custom_script_loader )
        user_js_src = path.join(self.base_dir, "fx-autoconfig", "user.js")
        if path.exists(user_js_src):
            self.file_actions.copy_file(user_js_src, self.temp_profile_folder)
            print("user.js copied.")
        if self.custom_script_loader:
            self.file_actions.copy_file(
                path.join(self.base_dir, "fx-autoconfig", "config.js"),
                self.application_folder,
            )
            self.file_actions.copy_file(
                path.join(self.base_dir, "fx-autoconfig", "mozilla.cfg"),
                self.application_folder,
            )
            self.file_actions.copy_file(
                path.join(self.base_dir, "fx-autoconfig", "config-prefs.js"),
                path.join(self.application_folder, "defaults", "pref"),
            )
            self.file_actions.copy_file(
                path.join(self.base_dir, "fx-autoconfig", "local-settings.js"),
                path.join(self.application_folder, "defaults", "pref"),
            )

        # Copy all other files and folders into the chrome folder (excluding user.js)
        for item in os.listdir(self.theme_dir):
            src_path = path.join(self.theme_dir, item)
            dest_path = path.join(self.chrome_folder, item)  # Copy into chrome folder
            if os.path.isdir(src_path):
                self.file_actions.copy_folder(src_path, dest_path)
            elif os.path.isfile(src_path) and item != "user.js":
                os.makedirs(path.dirname(dest_path), exist_ok=True)
                self.file_actions.copy_file(src_path, dest_path)

        self.file_actions.execute_operations(self.progress_bar, self.output_entry)
        print("Files and folders copied into the chrome folder.")

    def run_firefox(self):
        self.copy_files()
        print(f"Starting Firefox with profile: {self.temp_profile_folder}")
        subprocess.run(["firefox", "-no-remote", "-profile", self.temp_profile_folder])
        self.cleanup()
        self.file_actions.execute_operations(self.progress_bar, self.output_entry)
        print("Deleted temporary profile folder.")

    def cleanup(self):
        # Check if the temporary profile folder exists before attempting to remove it
        if os.path.exists(self.temp_profile_folder):
            self.file_actions.remove_folder(self.temp_profile_folder)
        
        # List of files to check and remove if they exist
        if self.custom_script_loader:
            files_to_remove = [
                os.path.join(self.application_folder, "config.js"),
                os.path.join(self.application_folder, "mozilla.cfg"),
                os.path.join(self.application_folder, "defaults", "pref", "config-prefs.js"),
                os.path.join(self.application_folder, "defaults", "pref", "local-settings.js")
            ]

            # Check and remove each file if it exists
            for file_path in files_to_remove:
                if os.path.isfile(file_path):
                    self.file_actions.remove_file(file_path)
                    print(f"Deleted file: {file_path}")
                else:
                    print(f"File not found, skipping: {file_path}")


