from platform import system

from installer_core.data_tools.load_json_data import LoadJsonData

class OSProperties:
    def __init__(self, data_file_path):
        load_json_data = LoadJsonData()
        self.os_data = load_json_data.load_json_data(data_file_path)

    def get_os(self):
        """Detects the operating system and returns a string."""
        os_name = system()
        if os_name == "Windows":
            return "windows"
        elif os_name == "Darwin":  # macOS detection
            return "macos"
        else:
            return "linux"  # Assuming any other OS is Linux-like

    def get_values(self):
        os_name = self.get_os()
        if self.os_data:
            return self.os_data.get(os_name, {})
        else:
            return {}

    def get_locations(self):
        os_data = self.get_values()
        return os_data.get("default_locations", {})
