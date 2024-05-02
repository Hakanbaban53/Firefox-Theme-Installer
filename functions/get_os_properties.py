import json
import platform

class OSProperties:
    OS_NAME = None  
    with open("../RealFire_Installer/data/installer_data.json", "r") as file:
        os_data = json.load(file)

    def get_os(self):
        """Detects the operating system and returns a string."""
        self.OS_NAME = platform.system()
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


