import requests
import zipfile
import os
import json


class ThemeDownloader:
    def __init__(self, theme_data, extract_path):
        self.theme_data = theme_data
        self.extract_path = extract_path
        self.zip_path = os.path.join(extract_path, "theme.zip")
        self.download_url = self.theme_data.link + "/archive/refs/heads/main.zip"
        os.makedirs(extract_path, exist_ok=True)  # Ensure cache directory exists

    def download_theme(self):
        try:
            response = requests.get(self.download_url)
            response.raise_for_status()  # Check if the request was successful
            with open(self.zip_path, "wb") as file:
                file.write(response.content)
            print("Download completed successfully.")
        except requests.HTTPError as e:
            raise Exception(f"Failed to download theme: {e}")

    def extract_theme(self):
        try:
            with zipfile.ZipFile(self.zip_path, "r") as zip_ref:
                zip_ref.extractall(self.extract_path)
            print("Extraction completed successfully.")
        except zipfile.BadZipFile as e:
            raise Exception(f"Failed to extract theme: {e}")

    def check_theme_files(self):
        data_json_path = os.path.join(
            self.extract_path,
            self.theme_data.title + "-main",
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
                userchrome_css_path = os.path.join(root)
                print("Theme has userChrome.css file.")
                return {"type": "userChrome.css", "path": userchrome_css_path}

        # No relevant files found
        print("No theme data or chrome/userChrome.css found.")
        return None

    def process_theme(self):
        try:
            self.download_theme()
            self.extract_theme()
            theme_data = self.check_theme_files()
            if theme_data:
                return theme_data
            else:
                return False
        except Exception as e:
            print(e)
