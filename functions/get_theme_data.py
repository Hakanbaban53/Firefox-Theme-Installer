import datetime
import json
import os

import requests

class Theme:
    def __init__(self, title, link, description, image, tags):
        self.title = title
        self.link = link
        self.description = description
        self.image = self.convert_image_url(image)
        self.tags = tags

    def convert_image_url(self, image_path):
        base_url = 'https://raw.githubusercontent.com/FirefoxCSS-Store/FirefoxCSS-Store.github.io/main/docs/'
        return base_url + image_path

    def __repr__(self):
        return f"Theme(title={self.title}, link={self.link})"

class ThemeManager:
    def __init__(self, json_file_path, json_file_url, check_file_age=False):
        self.json_file_url = json_file_url
        self.json_file_path = json_file_path
        self.check_file_age = check_file_age

        self.themes = self.load_json_data(self.json_file_path, self.check_file_age)

    def load_json_data(self, json_file_path=None, check_file_age=False):
        if os.path.exists(json_file_path) and check_file_age:
            file_age = datetime.now() - datetime.fromtimestamp(os.path.getmtime(json_file_path))
            if file_age > datetime.timedelta(days=3):
                # print(f"File {json_file_path} is older than one week. Deleting and downloading a new one.")
                os.remove(json_file_path)

        try:
            with open(json_file_path, 'r') as file:
                json_data = json.load(file)
                themes = [Theme(**theme_data) for theme_data in json_data]
            return themes
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
        except FileNotFoundError:
            # print(f"JSON file not found: {json_file_path}. Attempting to download from {self.json_file_url}")
            return self.download_json_file(self.json_file_url, json_file_path)
        except Exception as e:
            print(f"An error occurred: {e}")
        return {}
    
    def download_json_file(self, download_link, destination, max_retries=6):
        retries = 0
        while retries < max_retries:
            try:
                response = requests.get(download_link)
                if response.status_code == 200:
                    with open(destination, "wb") as file:
                        file.write(response.content)
                    # print(f"Downloaded {destination}")
                    return self.load_json_data(destination)
                else:
                    # print(f"Failed to download {download_link}. Status code: {response.status_code}")
                    retries += 1
            except requests.exceptions.RequestException as e:
                # print(f"An error occurred: {e}")
                retries += 1

        # print(f"Failed to download after {max_retries} attempts. Showing error message.")
        return self.show_error_message()

    def show_error_message(self):
        # print("Error fetching the file list after multiple attempts.")
        return {}

    def get_all_themes(self):
        return self.themes

    def get_theme_by_title(self, title):
        for theme in self.themes:
            if theme.title == title:
                return theme
        return None

    def get_themes_by_tag(self, tag):
        return [theme for theme in self.themes if tag in theme.tags]
