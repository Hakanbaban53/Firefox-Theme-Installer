from json import load
from platform import system

class OSProperties:
    OS_NAME = None  
    with open("../RealFire-Installer/data/installer_data.json", "r") as file:
        os_data = load(file)

    def get_os(self):
        """Detects the operating system and returns a string."""
        self.OS_NAME = system()
        if self.OS_NAME == 'Windows':
            return 'Windows'
        elif self.OS_NAME == 'Darwin':  # macOS detection
            return 'macOS'
        else:
            return 'Linux'  # Assuming any other OS is Linux-like
        
    def get_values(self):
        osName = self.get_os()
        return self.os_data.get(osName.lower())
    
    def get_locations(self):
        os_data = self.get_values()
        return os_data["default_locations"]


