from pathlib import Path
import platform

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/home/hakan/Documents/GitHub/pythonInstaller/assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class OSProperties:
    OS_NAME = None  
    TEXT_COLOR = "black"  # Default color

    def get_os(self):
        """Detects the operating system and returns a string."""
        self.OS_NAME = platform.system()
        if self.OS_NAME == 'Windows':
            return 'Windows'
        elif self.OS_NAME == 'Darwin':  # macOS detection
            return 'macOS'
        else:
            return 'Linux'  # Assuming any other OS is Linux-like
        
    def get_os_color(self):
        text_color = self.TEXT_COLOR  # Default text color
        
        if self.OS_NAME == "Windows":
            text_color = "#357EC7"
        elif self.OS_NAME == "Linux":
            text_color = "#F06F27"
        elif self.OS_NAME == "Darwin":
            text_color = "#000000"
        
        return text_color
    
    def os_icon(self):
        os_icon_path = relative_to_assets(
            f"icons/{self.get_os().lower()}.png"
        )
        return os_icon_path
