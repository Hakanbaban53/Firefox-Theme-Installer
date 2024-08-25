import requests
import zipfile
import os
import shutil
# import logging

class ThemeDownloader:
    def __init__(self, theme_data, extract_path, clean_install, base_dir=None):
        self.theme_data = theme_data
        self.extract_path = extract_path
        self.zip_path = os.path.join(extract_path, f"{self.theme_data.title}.zip")
        self.theme_folder_path = os.path.join(extract_path, f"{self.theme_data.title}-main")
        self.download_url = self.theme_data.link + "/archive/refs/heads/main.zip"
        self.clean_install = clean_install
        self.user_js_url = "https://github.com/Hakanbaban53/RealFire/raw/main/programs/user.js"
        self.user_js_target_dir = None
        self.base_dir = base_dir

        os.makedirs(extract_path, exist_ok=True)
        # logging.basicConfig(level=logging.INFO)

    def theme_already_downloaded(self):
        return os.path.exists(self.theme_folder_path)

    def download_theme(self):
        if self.theme_already_downloaded() and not self.clean_install:
            # logging.info("Theme already downloaded and extracted.")
            return True

        try:
            # logging.info("Starting theme download...")
            with requests.get(self.download_url, stream=True) as response:
                response.raise_for_status()
                with open(self.zip_path, "wb") as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
            # logging.info("Download completed successfully.")
            return True
        except requests.HTTPError as e:
            # logging.error(f"Failed to download theme: {e}")
            return False
        except requests.RequestException as e:
            # logging.error(f"Error during download: {e}")
            return False

    def extract_theme(self):
        if self.theme_already_downloaded() and not self.clean_install:
            # logging.info("Theme already extracted.")
            return True

        if self.clean_install and os.path.exists(self.theme_folder_path):
            shutil.rmtree(self.theme_folder_path)
            # logging.info("Existing theme directory removed for clean install.")

        try:
            # logging.info("Starting extraction...")
            with zipfile.ZipFile(self.zip_path, "r") as zip_ref:
                zip_ref.extractall(self.extract_path)
            # logging.info("Extraction completed successfully.")
            return True
        except zipfile.BadZipFile as e:
            # logging.error(f"Failed to extract theme: {e}")
            raise e

    def download_user_js(self):
        if not self.user_js_target_dir:
            # logging.warning("user.js target directory not set.")
            return False

        try:
            # logging.info("Starting user.js download...")
            os.makedirs(self.user_js_target_dir, exist_ok=True)
            user_js_path = os.path.join(self.user_js_target_dir, "user.js")

            with requests.get(self.user_js_url, stream=True) as response:
                response.raise_for_status()
                with open(user_js_path, "wb") as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)

            # logging.info(f"user.js downloaded and placed in {self.user_js_target_dir}.")
            return True
        except requests.HTTPError as e:
            # logging.error(f"Failed to download user.js: {e}")
            raise
        except requests.RequestException as e:
            # logging.error(f"Error during download of user.js: {e}")
            raise

    def check_theme_files(self):
        data_json_path = os.path.join(self.theme_folder_path, "data", "installer_files_data.json")

        if os.path.exists(data_json_path):
            # logging.info("Theme has its own data JSON.")
            self.user_js_target_dir = os.path.join(self.base_dir, "chrome")
            return {"type": "data", "path": data_json_path}

        for root, dirs, files in os.walk(self.theme_folder_path):
            if "userChrome.css" in files:
                # logging.info("Theme has userChrome.css file.")
                self.user_js_target_dir = root
                return {"type": "userChrome.css", "path": root}

        # logging.warning("No theme data or chrome/userChrome.css found.")
        return None

    def process_theme(self):
        try:
            if self.download_theme() and self.extract_theme():
                theme_data = self.check_theme_files()
                if theme_data and self.download_user_js():
                    return theme_data
            return False
        except Exception as e:
            # logging.error(f"An error occurred: {e}")
            raise e
