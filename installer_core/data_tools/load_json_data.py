from json import JSONDecodeError, load
from os import makedirs, path, remove
from requests import get, exceptions
from datetime import datetime, timedelta
from logging import info, error
import time

class LoadJsonData:
    def __init__(self, json_file_url=None):
        self.json_file_url = json_file_url

    def load_json_data(self, json_file_path, check_file_age=False):
        """
        Load JSON data from a file. Optionally check if the file is outdated and needs to be refreshed.
        """
        # Check file age if required
        if check_file_age and self._is_file_outdated(json_file_path, days=3):
            info(f"File {json_file_path} is older than 3 days. Deleting and downloading a new one.")
            self._delete_file(json_file_path)

        try:
            with open(json_file_path, "r", encoding="utf-8") as file:
                return load(file)
        except JSONDecodeError as e:
            error(f"Error decoding JSON from {json_file_path}: {e}")
        except FileNotFoundError:
            info(f"JSON file not found: {json_file_path}. Attempting to download from {self.json_file_url}")
            return self._download_json_file(self.json_file_url, json_file_path)
        except Exception as e:
            error(f"Unexpected error when loading JSON from {json_file_path}: {e}")

        return {}

    def _is_file_outdated(self, file_path, days):
        """
        Check if a file is older than a given number of days.
        """
        if path.exists(file_path):
            file_age = datetime.now() - datetime.fromtimestamp(path.getmtime(file_path))
            return file_age > timedelta(days=days)
        return False

    def _delete_file(self, file_path):
        """
        Delete a file if it exists.
        """
        try:
            if path.exists(file_path):
                remove(file_path)
                info(f"Deleted outdated file: {file_path}")
        except Exception as e:
            error(f"Failed to delete {file_path}: {e}")

    def _download_json_file(self, download_link, destination, max_retries=6):
        """
        Download a JSON file from a URL with retries and save it to the specified destination.
        """
        retries = 0
        while retries < max_retries:
            try:
                response = get(download_link)
                response.raise_for_status()  # Raise an exception for HTTP errors
                self._save_to_file(destination, response.content)
                info(f"Downloaded JSON file to {destination}")
                return self.load_json_data(destination)
            except exceptions.RequestException as e:
                error(f"Request error during download attempt {retries + 1}/{max_retries}: {e}")
            except OSError as e:
                error(f"OS error while handling file {destination}: {e}")
                self._ensure_directory_exists(destination)
            retries += 1
            time.sleep(2 ** retries)  # Exponential backoff

        error(f"Failed to download {download_link} after {max_retries} attempts.")
        return self._show_error_message()

    def _save_to_file(self, file_path, content):
        """
        Save content to a file.
        """
        try:
            with open(file_path, "wb") as file:
                file.write(content)
        except OSError as e:
            error(f"Error saving file {file_path}: {e}")
            raise

    def _ensure_directory_exists(self, file_path):
        """
        Ensure the directory for the given file path exists.
        """
        try:
            makedirs(path.dirname(file_path), exist_ok=True)
            info(f"Created directories for {file_path}")
        except OSError as e:
            error(f"Failed to create directories for {file_path}: {e}")

    def _show_error_message(self):
        """
        Log an error message when all download attempts fail.
        """
        error("Error fetching the JSON data after multiple attempts.")
        return {}
