from json import load
from platform import system

class OSProperties:
    def __init__(self, data_file_path):
        self.os_data = None
        self.load_data(data_file_path)

    def load_data(self, data_file_path):
        try:
            with open(data_file_path, "r") as file:
                self.os_data = load(file)
        except FileNotFoundError:
            print(f"Error: Could not find data file at '{data_file_path}'")
        except Exception as e:
            print(f"Error loading data from '{data_file_path}': {e}")
            self.os_data = {}

    def get_os(self):
        """Detects the operating system and returns a string."""
        os_name = system()
        if os_name == 'Windows':
            return 'windows'
        elif os_name == 'Darwin':  # macOS detection
            return 'macos'
        else:
            return 'linux'  # Assuming any other OS is Linux-like

    def get_values(self):
        os_name = self.get_os()
        if self.os_data:
            return self.os_data.get(os_name, {})
        else:
            return {}

    def get_locations(self):
        os_data = self.get_values()
        return os_data.get("default_locations", {})