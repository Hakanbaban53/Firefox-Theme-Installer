import requests
import zipfile
import os
import shutil
from requests.adapters import HTTPAdapter
from urllib3 import Retry

class ThemeDownloader:
    def __init__(self, theme_data, extract_path, clean_install, base_dir=None):
        self.theme_data = theme_data
        self.extract_path = extract_path
        self.zip_path = os.path.join(extract_path, f"{self.theme_data.title}.zip")
        self.theme_folder_path = os.path.join(extract_path, f"{self.theme_data.title}-main")
        self.download_url = self.theme_data.link + "/archive/refs/heads/main.zip"
        self.clean_install = clean_install
        self.base_dir = base_dir

        os.makedirs(extract_path, exist_ok=True)

    def theme_already_downloaded(self):
        # Check if the theme folder already exists
        return os.path.exists(self.theme_folder_path)

    def zip_file_exists_and_valid(self):
        # Check if the zip file exists and is not corrupted
        if not os.path.exists(self.zip_path):
            return False
        try:
            with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
                bad_file = zip_ref.testzip()
                if bad_file is not None:
                    print(f"Corrupt file detected: {bad_file}")
                    return False
            return True
        except zipfile.BadZipFile:
            print("Bad zip file detected.")
            return False

    def download_theme(self):
        if self.zip_file_exists_and_valid():
            print("Zip file already downloaded and valid.")
            return True
        
        # Define a session to manage retries
        session = requests.Session()
        retry = Retry(
            total=5,  
            backoff_factor=0.3,  
            status_forcelist=[500, 502, 503, 504]  
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
            print("Theme already extracted.")
            return True

        # Clean install: remove existing folder if it exists
        if self.clean_install and os.path.exists(self.theme_folder_path):
            shutil.rmtree(self.theme_folder_path)
            print("Existing theme directory removed for clean install.")

        try:
            print("Starting extraction...")
            with zipfile.ZipFile(self.zip_path, "r") as zip_ref:
                zip_ref.extractall(self.extract_path)
            print("Extraction completed successfully.")
            return True
        except zipfile.BadZipFile as e:
            print(f"Failed to extract theme: {e}")
            raise e

    def check_theme_files(self):
        data_json_path = os.path.join(self.theme_folder_path, "data", "installer_files_data.json")

        if os.path.exists(data_json_path):
            print("Theme has its own data JSON.")
            self.user_js_target_dir = os.path.join(self.base_dir, "chrome")
            return {"type": "data", "path": data_json_path}

        for root, dirs, files in os.walk(self.theme_folder_path):
            if "userChrome.css" in files:
                print("Theme has userChrome.css file.")
                self.user_js_target_dir = root
                return {"type": "userChrome.css", "path": root}

        print("No theme data or chrome/userChrome.css found.")
        return None

    def process_theme(self):
        try:
            if self.download_theme() and self.extract_theme():
                theme_data = self.check_theme_files()
                return theme_data
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            raise e
