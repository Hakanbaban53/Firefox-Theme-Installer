import json

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
    def __init__(self, json_file_path):
        self.themes = self.load_themes_from_file(json_file_path)

    def load_themes_from_file(self, file_path):
        with open(file_path, 'r') as file:
            json_data = json.load(file)
            themes = [Theme(**theme_data) for theme_data in json_data]
        return themes

    def get_all_themes(self):
        return self.themes

    def get_theme_by_title(self, title):
        for theme in self.themes:
            if theme.title == title:
                return theme
        return None

    def get_themes_by_tag(self, tag):
        return [theme for theme in self.themes if tag in theme.tags]
