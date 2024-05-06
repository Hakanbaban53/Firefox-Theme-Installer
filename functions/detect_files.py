import os
import json
import requests
from concurrent.futures import ThreadPoolExecutor


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
                    print(
                        f"Failed to download {download_link}. Status code: {response.status_code}"
                    )
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

    def check_and_download(self, folder_file_data=None, root="."):
        if folder_file_data is None:
            folder_file_data = self.folder_file_data

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for folder, contents in folder_file_data.items():
                if isinstance(
                    contents, dict
                ):  # If contents is a dict, it's a subfolder
                    subfolder_path = os.path.join(root, folder)
                    self.create_folder(
                        subfolder_path
                    )  # Create subfolder if it doesn't exist
                    # Recursively check the subfolder
                    futures.append(
                        executor.submit(
                            self.check_and_download, contents, subfolder_path
                        )
                    )
                else:  # If contents is not a dict, it's assumed to be a file link
                    file_path = os.path.join(root, folder)
                    if not os.path.isfile(file_path):
                        # Submit download task to the thread pool
                        futures.append(
                            executor.submit(
                                self.download_from_github, contents, file_path
                            )
                        )

            # Wait for all futures to complete
            for future in futures:
                future.result()

    def check_files_exist(self, folder_file_data=None, root="."):
        if folder_file_data is None:
            folder_file_data = self.folder_file_data
            self.missing_files = {}  # Her kontrolde sözlüğü sıfırla

        for folder, contents in folder_file_data.items():
            folder_path = os.path.join(root, folder)
            if isinstance(
                contents, dict
            ):  # Eğer içerik bir sözlükse, bu bir alt klasördür
                self.check_files_exist(contents, folder_path)
            else:  # Eğer içerik bir sözlük değilse, bu bir dosya bağlantısı olarak kabul edilir
                if not os.path.isfile(folder_path):
                    # Eksik dosyanın bulunduğu klasör adını al
                    missing_folder_name = (
                        os.path.basename(root) if root != "." else folder
                    )
                    # Eksik dosyayı klasör adı altında grupla
                    if missing_folder_name not in self.missing_files:
                        self.missing_files[missing_folder_name] = []
                    self.missing_files[missing_folder_name].append(folder)

        return self.missing_files

