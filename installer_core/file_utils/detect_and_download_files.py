from os import path, makedirs
from requests import get, exceptions
from concurrent.futures import ThreadPoolExecutor

from installer_core.data_tools.load_json_data import LoadJsonData

# Uncomment and configure logging if needed
# from logging import basicConfig, INFO, info, error
# basicConfig(level=INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FileManager:
    def __init__(self, json_file_path, json_file_url=None):
        self.missing_files = {}
        load_json_data = LoadJsonData(json_file_url)
        self.json_data = load_json_data.load_json_data(json_file_path)

    def download_from_github(self, download_link, destination, max_retries=3):
        """
        Downloads a file from GitHub with retries on failure.
        """
        retries = 0
        while retries < max_retries:
            try:
                response = get(download_link, timeout=10)
                response.raise_for_status()
                makedirs(path.dirname(destination), exist_ok=True)
                with open(destination, "wb") as file:
                    file.write(response.content)
                # info(f"Downloaded {destination}")
                return True
            except exceptions.RequestException as e:
                retries += 1
                # error(f"Error downloading {download_link}: {e} (Attempt {retries}/{max_retries})")
        # error(f"Failed to download {download_link} after {max_retries} attempts.")
        return False

    def create_folder(self, folder_path):
        """
        Creates a folder if it doesn't exist.
        """
        try:
            makedirs(folder_path, exist_ok=True)
            # info(f"Created folder: {folder_path}")
        except OSError as e:
            # error(f"Error creating folder {folder_path}: {e}")
            raise e

    def download_missing_files(self, missing_files, base_dir="."):
        """
        Downloads all missing files in parallel.
        """
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [
                executor.submit(self.download_from_github, file_info['url'], path.normpath(path.join(base_dir, folder_path, file_info['file'])))
                for folder_path, files in missing_files.items()
                for file_info in files
            ]

            for future in futures:
                try:
                    if not future.result():
                        # Handle download failure
                        # error(f"Download failed for a file.")
                        pass
                except Exception as e:
                    # error(f"An error occurred during file download: {e}")
                    raise e

    def check_files_exist(self, folder_file_data=None, root="."):
        """
        Checks if all required files exist based on the JSON data structure.
        """
        if folder_file_data is None:
            folder_file_data = self.json_data
            self.missing_files = {}

        for folder, contents in folder_file_data.items():
            folder_path = path.normpath(path.join(root, folder))
            if isinstance(contents, dict):
                self.check_files_exist(contents, folder_path)
            else:
                if not path.isfile(folder_path):
                    if root not in self.missing_files:
                        self.missing_files[root] = []
                    self.missing_files[root].append({'file': folder, 'url': contents})

        # info(f"Missing files: {self.missing_files}")
        return self.missing_files

# Example usage
# filemanager = FileManager(
#     "../RealFire_Installer/data/installer_files_data.json",
#     "https://raw.githubusercontent.com/Hakanbaban53/RealFire-Installer/main/data/installer_files_data.json"
# )
# missing_files = filemanager.check_files_exist()
# base_download_dir = "./downloads"
# filemanager.download_missing_files(missing_files, base_dir=base_download_dir)
# print(missing_files)
