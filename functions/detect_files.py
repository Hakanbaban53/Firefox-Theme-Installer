import os
import json
import requests
from concurrent.futures import ThreadPoolExecutor
import logging

class FileManager:
    def __init__(self, json_file_path):
        self.folder_file_data = self.load_json_data(json_file_path)
        self.missing_files = {}

    def load_json_data(self, json_file_path):
        try:
            with open(json_file_path, "r") as file:
                return json.load(file)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
        except FileNotFoundError:
            print(f"JSON file not found: {json_file_path}")
        except Exception as e:
            print(f"An error occurred: {e}")
        return {}

    def download_from_github(self, download_link, destination, max_retries=3):
        retries = 0
        while retries < max_retries:
            try:
                response = requests.get(download_link)
                if response.status_code == 200:
                    with open(destination, "wb") as file:
                        file.write(response.content)
                    print(f"Downloaded {destination}")
                    return
                else:
                    print(f"Failed to download {download_link}. Status code: {response.status_code}")
                    retries += 1
            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")
                retries += 1
            finally:
                if retries == max_retries:
                    print(f"Failed to download after {max_retries} attempts. Skipping.")

    def create_folder(self, folder_path):
        try:
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                print(f"Created folder: {folder_path}")
        except OSError as e:
            print(f"An error occurred while creating folder: {e}")



    def download_missing_files(self, missing_files):
        logging.basicConfig(level=logging.INFO)
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for folder_path, files in missing_files.items():
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                    print(f"Folder generated: {folder_path}")
                for file_info in files:
                    file_path = os.path.join(folder_path, file_info['file'])
                    download_link = file_info['url']
                    logging.info(f"Downloading {file_path} from {download_link}")
                    futures.append(executor.submit(self.download_from_github, download_link, file_path))

            for future in futures:
                try:
                    future.result()
                except Exception as e:
                    logging.error(f"An error occurred: {e}")


    def check_files_exist(self, folder_file_data=None, root="."):
        if folder_file_data is None:
            folder_file_data = self.folder_file_data
            self.missing_files = {}  # Reset the dictionary for each check

        for folder, contents in folder_file_data.items():
            folder_path = os.path.join(root, folder)
            if isinstance(contents, dict):  # If the content is a dictionary, it's a subfolder
                self.check_files_exist(contents, folder_path)
            else:  # If the content is not a dictionary, it's considered a file link
                if not os.path.isfile(folder_path):
                    if root not in self.missing_files:
                        self.missing_files[root] = []
                    self.missing_files[root].append({
                        'file': folder,
                        'url': contents
                    })

        return self.missing_files

# filemanager = FileManager("../RealFire_Installer/data/installer_files_data.json")
# missing_files = filemanager.check_files_exist()
# filemanager.download_missing_files(missing_files)
# print(missing_files)