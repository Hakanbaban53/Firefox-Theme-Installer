from installer_core.data_tools.load_json_data import LoadJsonData

class Theme:
    def __init__(self, title, link, description, image, tags):
        self.title = title
        self.link = link
        self.description = description
        self.image = self.convert_image_url(image)
        self.tags = tags

    def convert_image_url(self, image_path):
        base_url = 'https://raw.githubusercontent.com/FirefoxCSS-Store/FirefoxCSS-Store.github.io/main/docs/'
        if image_path.startswith('https://') or image_path.startswith('http://'):
            return image_path
        else:
            return base_url + image_path
    
    def to_dict(self):
        return {
            "title": self.title,
            "link": self.link,
            "description": self.description,
            "image": self.image,
            "tags": self.tags,
        }

class ThemeManager:
    def __init__(self, json_file_path, json_file_url):
        load_json_data = LoadJsonData(json_file_url)
        json_data = load_json_data.load_json_data(json_file_path)
        self.themes = [Theme(**theme_data) for theme_data in json_data]

    def get_all_themes(self):
        return self.themes

    def get_theme_by_title(self, title):
        for theme in self.themes:
            if theme.title == title:
                return theme
        return None

    def get_themes_by_tag(self, tag):
        return [theme for theme in self.themes if tag in theme.tags]
