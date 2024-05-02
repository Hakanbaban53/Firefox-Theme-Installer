import os
import json
import requests

class FileManager:
    def __init__(self, folder_file_data):
        with open("../RealFire_Installer/data/installer_files_data.json", "r") as file:
            self.folder_file_data = json.load(file)

    def download_from_github(self, download_link, destination, max_retries=3):
        retries = 0
        while retries < max_retries:
            try:
                response = requests.get(download_link)
                if response.status_code == 200:
                    with open(destination, 'wb') as file:
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
                    print(f"Failed to download after {max_retries} attempts. Exiting.")
                    return

    def create_folder(self, folder_path):
        try:
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                print(f"Created folder: {folder_path}")
        except OSError as e:
            print(f"An error occurred while creating folder: {e}")

    def check_and_download(self):
        for folder, contents in self.folder_file_data.items():
            folder_path = os.path.join('.', folder)
            self.create_folder(folder_path)  # Create folder if it doesn't exist

            for file_name, download_link in contents.items():
                file_path = os.path.join(folder_path, file_name)
                if not os.path.isfile(file_path):
                    self.download_from_github(download_link, file_path)  # Download file

