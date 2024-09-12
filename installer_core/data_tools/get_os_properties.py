from pathlib import Path
from platform import system

from installer_core.data_tools.load_json_data import LoadJsonData

class OSProperties:
    def __init__(self, base_dir):
        """
        Initializes the OSProperties class, loads OS-specific data,
        and determines the current operating system.
        
        :param base_dir: Base directory path for locating the JSON data file.
        """
        self.os_properties_path = Path(base_dir) / "data" / "OS data" / "os_properties.json"
        self.os_name = self.detect_os()
        self.os_data = self.load_os_data()

    def detect_os(self):
        """
        Detects the current operating system.
        
        :return: A string representing the OS: 'windows', 'macos', or 'linux'.
        """
        os_name = system()
        if os_name == "Windows":
            return "windows"
        elif os_name == "Darwin":
            return "macos"
        else:
            return "linux"

    def load_os_data(self):
        """
        Loads operating system-specific data from the JSON file.

        :return: A dictionary of OS-specific data or an empty dictionary if loading fails.
        """
        load_json_data = LoadJsonData()
        os_data = load_json_data.load_json_data(self.os_properties_path)
        return os_data if os_data else {}

    def get_values(self):
        """
        Retrieves properties specific to the current OS from the loaded data.

        :return: A dictionary of values for the current OS.
        """
        return self.os_data.get(self.os_name, {})

    def get_locations(self):
        """
        Returns default locations for the current OS from the properties data.

        :return: A dictionary of default locations.
        """
        return self.get_values().get("default_locations", {})

    def expand_path(self, path_str):
        """
        Expands environment variables and user home in paths based on the OS type.

        :param path_str: A string representing the path with potential variables.
        :return: A Path object with expanded paths.
        """
        if self.os_name == "windows":
            return Path(path_str).expandvars()
        else:
            return Path(path_str).expanduser()

    def get_theme_preview_location(self):
        """
        Returns the theme preview location for the current OS.

        :return: A Path object for the theme preview location.
        """
        preview_location = self.get_values().get("preview_location", "")
        return self.expand_path(preview_location)

    def get_cache_location(self):
        """
        Returns the cache location for the current OS.

        :return: A Path object for the cache location.
        """
        cache_location = self.get_values().get("cache_location", "")
        return self.expand_path(cache_location)

    def get_os_color(self):
        """
        Returns the OS-specific color defined in the properties data.

        :return: A string representing the OS color in hex format.
        """
        return self.get_values().get("os_color", "#FFFFFF")  # Default to white if not specified
