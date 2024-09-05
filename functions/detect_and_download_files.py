from os import path,  makedirs
from requests import get, exceptions
from concurrent.futures import ThreadPoolExecutor

from functions.load_json_data import LoadJsonData
# from logging import basicConfig, INFO, info, error

class FileManager:
    def __init__(self, json_file_path, json_file_url=None):
        self.json_file_path = json_file_path
        self.json_file_url = json_file_url
        self.missing_files = {}

        load_json_data = LoadJsonData()
        self.json_data = load_json_data.load_json_data(self.json_file_path)


    def download_from_github(self, download_link, destination, max_retries=3):
        retries = 0
        while retries < max_retries:
            try:
                response = get(download_link)
                if response.status_code == 200:
                    makedirs(path.dirname(destination), exist_ok=True)
                    with open(destination, "wb") as file:
                        file.write(response.content)
                    # info(f"Downloaded {destination}")
                    return
                else:
                    # error(f"Failed to download {download_link}. Status code: {response.status_code}")
                    retries += 1
            except exceptions.RequestException as e:
                # error(f"An error occurred: {e}")
                retries += 1
        # error(f"Failed to download after {max_retries} attempts. Skipping.")

    def create_folder(self, folder_path):
        try:
            makedirs(folder_path, exist_ok=True)
            # info(f"Created folder: {folder_path}")
        except OSError as e:
            raise e
            # error(f"An error occurred while creating folder: {e}")

    def download_missing_files(self, missing_files, base_dir="."):
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for folder_path, files in missing_files.items():
                target_folder_path = path.normpath(path.join(base_dir, folder_path))
                if not path.exists(target_folder_path):
                    makedirs(target_folder_path)
                    # info(f"Folder generated: {target_folder_path}")
                for file_info in files:
                    file_path = path.normpath(path.join(target_folder_path, file_info['file']))
                    download_link = file_info['url']
                    # info(f"Downloading {file_path} from {download_link}")
                    futures.append(executor.submit(self.download_from_github, download_link, file_path))

            for future in futures:
                try:
                    future.result()
                except Exception as e:
                    # error(f"An error occurred: {e}")
                    raise e

    def check_files_exist(self, folder_file_data=None, root="."):
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
                    self.missing_files[root].append({
                        'file': folder,
                        'url': contents
                    })

        # info(f"Missing files: {self.missing_files}")
        return self.missing_files

# Example usage
# filemanager = FileManager(
#     "../RealFire_Installer/data/installer_files_data.,
#     "https://raw.githubusercontent.com/Hakanbaban53/RealFire-Installer/main/data/installer_files_data.
# )
# missing_files = filemanager.check_files_exist()

# base_download_dir = "./downloads"
# filemanager.download_missing_files(missing_files, base_dir=base_download_dir)

# print(missing_files)