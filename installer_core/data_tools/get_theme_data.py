from installer_core.data_tools.load_json_data import LoadJsonData
from re import search

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
        if image_path != None and image_path.startswith(('https://', 'http://')):
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
    
    def get_filtered_themes(self, search_query, selected_tag):
        """
        Retrieves themes that match the search query and selected tag.

        :param search_query: The search query to filter themes by.
        :param selected_tag: The tag to filter themes by.
        :return: A list of Theme objects that match the search query and selected tag.
        """
        return [
            theme
            for theme in self.themes
            if search_query in theme.title.lower()
            and (not selected_tag or selected_tag in theme.tags)
        ]
    
    def short_themes(self, themes, column, sort_order):
        """
        Sorts themes based on the specified column and sort order.

        :param themes: A list of Theme objects to sort.
        :param column: The column to sort by.
        :param sort_order: The order to sort the themes in.
        :return: A list of sorted Theme objects.
        """
        return sorted(
            themes,
            key=lambda t: getattr(t, column, ""),
            reverse=sort_order == "desc",
        )
    
    def is_valid_custom_theme(self, url):
        """
        Validates a custom theme URL by checking if it is a valid URL.

        :param url: The URL to validate.
        :return: True if the URL is valid, False otherwise.
        """
        allowed_domains = ["github.com", "gitlab.com", "codeberg.org", "git.gay"]
        return any(domain in url for domain in allowed_domains)
    
    def extract_repo_name(self, url):
        """
        Extracts the repository name from a GitHub/GitLab URL.

        :param url: The URL of the theme's repository.
        :return: The repository name (e.g., RealFire from https://github.com/Hakanbaban53/RealFire/).
        """
        # Regular expression to extract the repo name (last part of the URL)
        match = search(r'/([^/]+)/?$', url)
        if match:
            return match.group(1)
        return "Custom"  # Default to "Custom" if no match is found
    