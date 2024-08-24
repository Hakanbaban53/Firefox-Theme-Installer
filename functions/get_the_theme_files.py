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
        self.user_js_url = "https://github.com/Hakanbaban53/RealFire/raw/main/programs/user.js"
        os.makedirs(extract_path, exist_ok=True)
        self.user_js_target_dir = None

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
            shutil.rmtree(self.theme_folder_path)
            print("Existing theme directory removed for clean install.")

        try:
            with zipfile.ZipFile(self.zip_path, "r") as zip_ref:
                zip_ref.extractall(self.extract_path)
            print("Extraction completed successfully.")
            return True
        except zipfile.BadZipFile as e:
            raise Exception(f"Failed to extract theme: {e}")

    def download_user_js(self):
        try:
            if self.user_js_target_dir:
                user_js_path = os.path.join(self.user_js_target_dir, "user.js")
                response = requests.get(self.user_js_url, stream=True)
                response.raise_for_status()

                with open(user_js_path, "wb") as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)

                print(f"user.js downloaded and placed in {self.user_js_target_dir}.")
                return True
            else:
                print("user.js target directory not set.")
                return False
        except requests.HTTPError as e:
            raise Exception(f"Failed to download user.js: {e}")
        except requests.RequestException as e:
            raise Exception(f"Error during download of user.js: {e}")

    def check_theme_files(self):
        data_json_path = os.path.join(
            self.theme_folder_path,
            "data",
            "installer_files_data.json",
        )

        # Check if data installer_files_data.json exists
        if os.path.exists(data_json_path):
            print("Theme has its own data JSON.")
            return {"type": "data", "path": data_json_path}

        # Check if userChrome.css file exists in the specific theme folder
        for root, dirs, files in os.walk(self.theme_folder_path):
            if "userChrome.css" in files:
                print("Theme has userChrome.css file.")
                self.user_js_target_dir = root
                return {"type": "userChrome.css", "path": root}

        # No relevant files found
        print("No theme data or chrome/userChrome.css found.")
        return None

    def process_theme(self):
        try:
            if self.download_theme():
                if self.extract_theme():
                    theme_data = self.check_theme_files()
                    if theme_data and self.download_user_js():
                        return theme_data
            return False
        except Exception as e:
            print(e)
