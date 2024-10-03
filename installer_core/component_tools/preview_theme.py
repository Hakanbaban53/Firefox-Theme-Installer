from os import path, makedirs, listdir
from subprocess import Popen, run, CalledProcessError
# from logging import basicConfig, info, error, warning, INFO

from installer_core.data_tools.get_os_properties import OSProperties
from installer_core.file_utils.file_actions import FileActions

# Configure logging
# basicConfig(level=INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PreviewTheme:
    def __init__(
        self,
        base_dir,
        theme_dir,
        CSL,
        profile_folder,
        application_folder,
    ):
        self.application_folder = application_folder
        self.profile_folder = profile_folder
        self.custom_script_loader = CSL
        self.theme_dir = theme_dir

        self.os_properties = OSProperties(base_dir)
        self.current_os = self.os_properties.detect_os()  # Get current OS info

        self.CACHE_PATH = self.os_properties.get_cache_location()
        self.THEME_TEMP_PATH = self.os_properties.get_theme_preview_location()

        self.chrome_folder = path.join(self.THEME_TEMP_PATH, "chrome")
        self.file_actions = FileActions(self.current_os)
        # info(f"PreviewTheme initialized with temp profile folder: {self.THEME_TEMP_PATH}")

    def copy_files(self):
        self.cleanup()  # Ensure no leftover profile folder or files
        makedirs(self.THEME_TEMP_PATH, exist_ok=True)  # Create the profile folder
        makedirs(self.chrome_folder, exist_ok=True)  # Ensure the chrome folder exists

        # Create a temporary Firefox profile based on the current OS
        try:
            if self.current_os == "linux":
                run(["firefox", "-CreateProfile", f"temp_theme_profile {self.THEME_TEMP_PATH}"], check=True)
            elif self.current_os == "windows":
                firefox_path = path.join(self.application_folder, "firefox.exe")
                run([firefox_path, "-CreateProfile", f"temp_theme_profile {self.THEME_TEMP_PATH}", "-wait-for-browser"], check=True)
            elif self.current_os == "macos":
                firefox_path = path.join(self.application_folder, "Firefox.app")
                run(["open", "-n", firefox_path, "--args", "-CreateProfile", f"temp_theme_profile {self.THEME_TEMP_PATH}"], check=True)
            else:
                raise OSError(f"Unsupported OS: {self.current_os}")
            # info("Temporary Firefox profile created.")
        except CalledProcessError as e:
            # error(f"Failed to create Firefox profile: {e}")
            return

        user_js_src = path.join(self.CACHE_PATH, "fx-autoconfig", "user.js")
        if path.exists(user_js_src):
            self.file_actions.copy_file(user_js_src, self.THEME_TEMP_PATH)
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
                src = path.join(self.CACHE_PATH, "fx-autoconfig", filename)
                if path.exists(src):
                    self.file_actions.copy_file(src, dest_dir)
                    # info(f"Copied {filename} to {dest_dir}.")
        except Exception as e:
            # error(f"An error occurred while copying custom script files: {e}")
            return

    def run_firefox(self):
        self.copy_files()
        # info(f"Starting Firefox with profile: {self.THEME_TEMP_PATH}")
        try:
            if self.current_os == "linux":
                process = Popen(["firefox", "-no-remote", "-profile", self.THEME_TEMP_PATH])
            elif self.current_os == "windows":
                firefox_path = path.join(self.application_folder, "firefox.exe")
                process = Popen([firefox_path, "-no-remote", "-profile", self.THEME_TEMP_PATH, "-wait-for-browser"])
            elif self.current_os == "macos":
                firefox_path = path.join(self.application_folder, "Firefox.app")
                process = Popen(["open", "-n", firefox_path, "--args", "-no-remote", "-profile", self.THEME_TEMP_PATH])
            else:
                raise OSError(f"Unsupported OS: {self.current_os}")
            
            # Wait for Firefox to close
            process.wait()
        except CalledProcessError as e:
            # error(f"Failed to run Firefox: {e}")
            return
        finally:
            # Cleanup after Firefox closes
            self.cleanup()
            # info("Cleaned up temporary profile folder after Firefox run.")
        
    def cleanup(self):
        # Ensure clean removal of the temporary profile folder
        if path.exists(self.THEME_TEMP_PATH):
            try:
                if path.isfile(self.THEME_TEMP_PATH):
                    self.file_actions.remove_file(self.THEME_TEMP_PATH)  # Handle case where a file exists with the same name
                    # warning(f"Removed stray file named {self.THEME_TEMP_PATH}.")
                else:
                    self.file_actions.remove_folder(self.THEME_TEMP_PATH)
                    # info(f"Deleted temporary profile folder: {self.THEME_TEMP_PATH}.")
            except Exception as e:
                # error(f"Failed to delete temporary profile folder: {e}")
                return

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
                        # error(f"Failed to delete file {file_path}: {e}")
                        return
        self.file_actions.execute_operations()

# Example usage:
# preview_theme = PreviewTheme(
#     base_dir="/path/to/base",
#     theme_dir="/path/to/theme",
#     CSL=True,
#     profile_folder="/path/to/profile",
#     application_folder="/path/to/application"
# )
# preview_theme.run_firefox()
