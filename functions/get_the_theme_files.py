import requests
import zipfile
import os
import shutil
from requests.adapters import HTTPAdapter
from urllib3 import Retry
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
        print(self.clean_install)

        os.makedirs(extract_path, exist_ok=True)
        # logging.basicConfig(level=logging.INFO)

    def theme_already_downloaded(self):
        return os.path.exists(self.theme_folder_path)
    
    def download_theme(self):
        # Define a session to manage retries
        session = requests.Session()
        retry = Retry(
            total=5,  # Total retries
            backoff_factor=0.3,  # Wait time between retries
            status_forcelist=[500, 502, 503, 504]  # Retry on these status codes
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        try:
            # Initiate the download
            with session.get(self.download_url, stream=True, timeout=10) as response:
                response.raise_for_status()
                with open(self.zip_path, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            file.write(chunk)
            return True
        except requests.exceptions.Timeout:
            print("Download timed out.")
        except requests.exceptions.TooManyRedirects:
            print("Too many redirects.")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")

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
                return theme_data
            return False
        except Exception as e:
            # logging.error(f"An error occurred: {e}")
            raise e
