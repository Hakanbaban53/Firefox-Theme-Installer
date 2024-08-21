import requests
import zipfile
import os
import shutil

class ThemeDownloader:
    def __init__(self, theme_data, extract_path, clean_install):
        self.theme_data = theme_data
        self.extract_path = extract_path
        self.zip_path = os.path.join(extract_path, f"{self.theme_data.title}.zip")
        self.theme_folder_path = os.path.join(extract_path, f"{self.theme_data.title}-main")
        self.download_url = self.theme_data.link + "/archive/refs/heads/main.zip"
        self.clean_install = clean_install
        os.makedirs(extract_path, exist_ok=True)  # Ensure extract directory exists

    def theme_already_downloaded(self):
        return os.path.exists(self.theme_folder_path)

    def download_theme(self):
        if self.theme_already_downloaded() and not self.clean_install:
            print("Theme already downloaded and extracted.")
            return True

        try:
            response = requests.get(self.download_url, stream=True)
            response.raise_for_status()  # Check if the request was successful
            with open(self.zip_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print("Download completed successfully.")
            return True
        except requests.HTTPError as e:
            raise Exception(f"Failed to download theme: {e}")
        except requests.RequestException as e:
            raise Exception(f"Error during download: {e}")

    def extract_theme(self):
        if self.theme_already_downloaded() and not self.clean_install:
            print("Theme already extracted.")
            return True

        if self.clean_install and os.path.exists(self.theme_folder_path):
            shutil.rmtree(self.theme_folder_path)  # Remove existing directory for a clean install
            print("Existing theme directory removed for clean install.")

        try:
            with zipfile.ZipFile(self.zip_path, "r") as zip_ref:
                zip_ref.extractall(self.extract_path)
            print("Extraction completed successfully.")
            return True
        except zipfile.BadZipFile as e:
            raise Exception(f"Failed to extract theme: {e}")

    def check_theme_files(self):
        data_json_path = os.path.join(
            self.theme_folder_path,
            "data",
            "installer_files_data.json",
        )
        userchrome_css_path = None

        # Check if data installer_files_data.json exists
        if os.path.exists(data_json_path):
            print("Theme has its own data JSON.")
            return {"type": "data", "path": data_json_path}

        # Check if userChrome.css file exists
        for root, dirs, files in os.walk(self.extract_path):
            if "userChrome.css" in files:
                userchrome_css_path = os.path.join(root, "userChrome.css")
                print("Theme has userChrome.css file.")
                return {"type": "userChrome.css", "path": userchrome_css_path}

        # No relevant files found
        print("No theme data or chrome/userChrome.css found.")
        return None

    def process_theme(self):
        try:
            if self.download_theme():
                if self.extract_theme():
                    theme_data = self.check_theme_files()
                    if theme_data:
                        return theme_data
            return False
        except Exception as e:
            print(e)
