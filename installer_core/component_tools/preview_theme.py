from os import path, makedirs, listdir
from subprocess import run, CalledProcessError
# from logging import basicConfig, info, error, warning, INFO

from installer_core.file_utils.file_actions import FileActions

# Configure logging
# basicConfig(level=INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PreviewTheme:
    def __init__(
        self,
        cache_dir,
        theme_dir,
        temp_profile_folder,
        os_name,
        CSL,
        profile_folder,
        application_folder,
    ):
        self.application_folder = application_folder
        self.profile_folder = profile_folder
        self.custom_script_loader = CSL
        self.cache_dir = cache_dir
        self.theme_dir = theme_dir
        self.temp_profile_folder = temp_profile_folder
        self.os_name = os_name
        self.chrome_folder = path.join(self.temp_profile_folder, "chrome")
        self.file_actions = FileActions(os_name)
        # info(f"PreviewTheme initialized with temp profile folder: {self.temp_profile_folder}")

    def copy_files(self):
        self.cleanup()  # Ensure no leftover profile folder or files
        makedirs(self.temp_profile_folder, exist_ok=True)  # Create the profile folder
        makedirs(self.chrome_folder, exist_ok=True)  # Ensure the chrome folder exists

        # Create a temporary Firefox profile
        try:
            run(
                ["firefox", "-CreateProfile", f"temp_theme_profile {self.temp_profile_folder}"],
                check=True
            )
            # info("Temporary Firefox profile created.")
        except CalledProcessError as e:
            # error(f"Failed to create Firefox profile: {e}")
            return

        user_js_src = path.join(self.cache_dir, "fx-autoconfig", "user.js")
        if path.exists(user_js_src):
            self.file_actions.copy_file(user_js_src, self.temp_profile_folder)
            # info("Copied user.js to the temporary profile folder.")

        if self.custom_script_loader:
            self._copy_custom_script_files()

        # Copy all other files and folders into the chrome folder (excluding user.js)
        for item in listdir(self.theme_dir):
            src_path = path.join(self.theme_dir, item)
            dest_path = path.join(self.chrome_folder, item)  # Copy into chrome folder
            if path.isdir(src_path):
                self.file_actions.copy_folder(src_path, dest_path)
                # info(f"Copied folder {src_path} to {dest_path}.")
            elif path.isfile(src_path) and item != "user.js":
                makedirs(path.dirname(dest_path), exist_ok=True)
                self.file_actions.copy_file(src_path, dest_path)
                # info(f"Copied file {src_path} to {dest_path}.")

        self.file_actions.execute_operations()
        # info("All files and folders copied into the chrome folder.")

    def _copy_custom_script_files(self):
        # Helper function to copy custom script files if CSL is enabled
        try:
            custom_files = {
                "config.js": self.application_folder,
                "mozilla.cfg": self.application_folder,
                "config-prefs.js": path.join(self.application_folder, "defaults", "pref"),
                "local-settings.js": path.join(self.application_folder, "defaults", "pref"),
            }

            for filename, dest_dir in custom_files.items():
                src = path.join(self.cache_dir, "fx-autoconfig", filename)
                if path.exists(src):
                    self.file_actions.copy_file(src, dest_dir)
                    # info(f"Copied {filename} to {dest_dir}.")
        except Exception as e:
            # error(f"An error occurred while copying custom script files: {e}")
            return

    def run_firefox(self):
        self.copy_files()
        # info(f"Starting Firefox with profile: {self.temp_profile_folder}")
        try:
            run(["firefox", "-no-remote", "-profile", self.temp_profile_folder], check=True)
        except CalledProcessError as e:
            return
            # error(f"Failed to run Firefox: {e}")
        finally:
            self.cleanup()
            # info("Cleaned up temporary profile folder after Firefox run.")

    def cleanup(self):
        # Ensure clean removal of the temporary profile folder
        if path.exists(self.temp_profile_folder):
            try:
                if path.isfile(self.temp_profile_folder):
                    self.file_actions.remove_file(self.temp_profile_folder)  # Handle case where a file exists with the same name
                    # warning(f"Removed stray file named {self.temp_profile_folder}.")
                else:
                    self.file_actions.remove_folder(self.temp_profile_folder)
                    # info(f"Deleted temporary profile folder: {self.temp_profile_folder}.")
            except Exception as e:
                return
                # error(f"Failed to delete temporary profile folder: {e}")

        # Clean up custom script loader files
        if self.custom_script_loader:
            files_to_remove = [
                path.join(self.application_folder, "config.js"),
                path.join(self.application_folder, "mozilla.cfg"),
                path.join(self.application_folder, "defaults", "pref", "config-prefs.js"),
                path.join(self.application_folder, "defaults", "pref", "local-settings.js")
            ]

            for file_path in files_to_remove:
                if path.isfile(file_path):
                    try:
                        self.file_actions.remove_file(file_path)
                        # info(f"Deleted file: {file_path}.")
                    except Exception as e:
                        return
                        # error(f"Failed to delete file {file_path}: {e}")
        self.file_actions.execute_operations()

# Example usage:
# preview_theme = PreviewTheme(
#     cache_dir="/path/to/cache",
#     theme_dir="/path/to/theme",
#     temp_profile_folder="/path/to/temp/profile",
#     os_name="Linux",
#     CSL=True,
#     profile_folder="/path/to/profile",
#     application_folder="/path/to/application"
# )
# preview_theme.run_firefox()
