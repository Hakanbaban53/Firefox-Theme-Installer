import os
import subprocess
import shutil
from os import path

class PreviewTheme:
    def __init__(self, theme_dir, temp_profile_folder, os_name):
        self.theme_dir = theme_dir
        self.temp_profile_folder = temp_profile_folder
        self.os_name = os_name
        self.chrome_folder = path.join(self.temp_profile_folder, "chrome")

    def copy_files(self):
        self.cleanup()  # Ensure no leftover profile folder
        os.makedirs(self.temp_profile_folder, exist_ok=True)  # Create the profile folder
        os.makedirs(self.chrome_folder, exist_ok=True)  # Ensure the chrome folder exists

        subprocess.run(["firefox", "-CreateProfile", f"temp_theme_profile {self.temp_profile_folder}"])
        
        user_js_src = path.join(self.theme_dir, "user.js")
        if path.exists(user_js_src):
            shutil.copy(user_js_src, self.temp_profile_folder)
            print("user.js copied.")

        # Copy all other files and folders into the chrome folder (excluding user.js)
        for item in os.listdir(self.theme_dir):
            src_path = path.join(self.theme_dir, item)
            dest_path = path.join(self.chrome_folder, item)  # Copy into chrome folder
            if os.path.isdir(src_path):
                shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
            elif os.path.isfile(src_path) and item != "user.js":
                os.makedirs(path.dirname(dest_path), exist_ok=True)
                shutil.copy(src_path, dest_path)

        print("Files and folders copied into the chrome folder.")

    def run_firefox(self):
        self.copy_files()
        print(f"Starting Firefox with profile: {self.temp_profile_folder}")
        subprocess.run(["firefox", "-no-remote", "-profile", self.temp_profile_folder])
        self.cleanup()

    def cleanup(self):
        if path.exists(self.temp_profile_folder):
            print("Deleting temporary profile folder.")
            shutil.rmtree(self.temp_profile_folder)
