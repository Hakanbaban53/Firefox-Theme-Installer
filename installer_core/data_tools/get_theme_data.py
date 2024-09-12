from installer_core.data_tools.load_json_data import LoadJsonData


class Theme:
    def __init__(self, title, link, description, image, tags):
        """
        Initialize a Theme instance with title, link, description, image URL, and tags.

        :param title: The title of the theme.
        :param link: The URL link to the theme's repository or page.
        :param description: A brief description of the theme.
        :param image: The path or URL of the theme's preview image.
        :param tags: A list of tags associated with the theme.
        """
        self.title = title
        self.link = link
        self.description = description
        self.image = self.convert_image_url(image)
        self.tags = tags

    def convert_image_url(self, image_path):
        """
        Converts a relative image path to a full URL if not already in URL format.

        :param image_path: The image path, either a URL or a relative path.
        :return: A complete URL to the image.
        """
        base_url = 'https://raw.githubusercontent.com/FirefoxCSS-Store/FirefoxCSS-Store.github.io/main/docs/'
        if image_path.startswith(('https://', 'http://')):
            return image_path
        return f"{base_url}{image_path}"

    def to_dict(self):
        """
        Converts the Theme instance to a dictionary.

        :return: A dictionary representation of the theme.
        """
        return {
            "title": self.title,
            "link": self.link,
            "description": self.description,
            "image": self.image,
            "tags": self.tags,
        }


class ThemeManager:
    def __init__(self, json_file_path, json_file_url):
        """
        Initialize the ThemeManager with a list of themes loaded from a JSON file.

        :param json_file_path: The path to the JSON file containing theme data.
        :param json_file_url: The URL for loading JSON data (if used by LoadJsonData).
        """
        self.themes = self.load_themes(json_file_path, json_file_url)
        self.theme_by_title = {theme.title: theme for theme in self.themes}  # For quick lookup by title

    def load_themes(self, json_file_path, json_file_url):
        """
        Loads themes from a JSON file and converts them to Theme objects.

        :param json_file_path: The path to the JSON file containing theme data.
        :param json_file_url: The URL for loading JSON data (if used by LoadJsonData).
        :return: A list of Theme objects.
        """
        load_json_data = LoadJsonData(json_file_url)
        json_data = load_json_data.load_json_data(json_file_path)
        return [Theme(**theme_data) for theme_data in json_data if self.validate_theme_data(theme_data)]


    @staticmethod
    def validate_theme_data(theme_data):
        """
        Validates the JSON data for a theme.

        :param theme_data: A dictionary representing a theme's data.
        :return: True if the data is valid, False otherwise.
        """
        required_keys = {"title", "link", "description", "image", "tags"}
        return required_keys.issubset(theme_data) and isinstance(theme_data["tags"], list)

    def get_all_themes(self):
        """
        Retrieves all themes managed by the ThemeManager.

        :return: A list of all Theme objects.
        """
        return self.themes

    def get_theme_by_title(self, title):
        """
        Retrieves a theme by its title.

        :param title: The title of the theme.
        :return: The Theme object if found, else None.
        """
        return self.theme_by_title.get(title)

    def get_themes_by_tag(self, tag):
        """
        Retrieves themes that match a specific tag.

        :param tag: The tag to filter themes by.
        :return: A list of Theme objects that contain the specified tag.
        """
        return [theme for theme in self.themes if tag in theme.tags]
