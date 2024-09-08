from json import JSONDecodeError, load
from os import makedirs, path, remove
from requests import get, exceptions
from datetime import datetime, timedelta
from logging import info, error

class LoadJsonData:
    def __init__(self, json_file_url=None):
        self.json_file_url = json_file_url

    def load_json_data(self, json_file_path, check_file_age=False):
        if path.exists(json_file_path) and check_file_age:
            file_age = datetime.now() - datetime.fromtimestamp(
                path.getmtime(json_file_path)
            )
            if file_age > timedelta(days=3):
                info(f"File {json_file_path} is older than one week. Deleting and downloading a new one.")
                remove(json_file_path)

        try:
            with open(json_file_path, "r") as file:
                return load(file)
        except JSONDecodeError as e:
            error(f"Error decoding JSON: {e}")
            return {}
        except FileNotFoundError:
            info(f"JSON file not found: {json_file_path}. Attempting to download from {self.json_file_url}")
            return self.download_json_file(self.json_file_url, json_file_path)
        except Exception as e:
            error(f"An error occurred: {e}")
            return {}

    def download_json_file(self, download_link, destination, max_retries=6):
        retries = 0
        while retries < max_retries:
            try:
                response = get(download_link)
                if response.status_code == 200:
                    with open(destination, "wb") as file:
                        file.write(response.content)
                    info(f"Downloaded {destination}")
                    return self.load_json_data(destination)
                else:
                    error(f"Failed to download {download_link}. Status code: {response.status_code}")
                    retries += 1
            except exceptions.RequestException as e:
                error(f"An error occurred: {e}")
                retries += 1
            except FileNotFoundError:
                error(f"Failed to download {download_link}. File/Folder not found. Creating folder and retrying")
                makedirs(path.dirname(destination), exist_ok=True)
                retries += 1

        error(f"Failed to download after {max_retries} attempts. Showing error message.")
        return self.show_error_message()

    def show_error_message(self):
        error("Error fetching the file list after multiple attempts.")
        return {}
