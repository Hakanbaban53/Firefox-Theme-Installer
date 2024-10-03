from os import getlogin, path, getenv
from re import search

class GetFolderLocations:
    def __init__(self, os_values):
        self.os_values = os_values

    def get_profile_folder(self):
        input_values = self.os_values.get("default_locations", {})

        FIREFOXFOLDER = input_values.get("firefox_folder", "")
        PROFILENAME = ""

        # Get the current user's username
        try:
            current_user = getlogin()
        except OSError:
            current_user = getenv('USERNAME') or getenv('USER')

        if "$USER" in FIREFOXFOLDER:
            # Construct the Firefox folder path with the current user's username
            FIREFOXFOLDER = FIREFOXFOLDER.replace("$USER", current_user)
        
        # Expand environment variables in the FIREFOXFOLDER path
        FIREFOXFOLDER = path.expandvars(FIREFOXFOLDER)
        
        # Check if profiles.ini exists
        PROFILES_FILE = path.join(FIREFOXFOLDER, "profiles.ini")
        if not path.isfile(PROFILES_FILE):
            return ""

        # Define default Profile folder path else use -p option
        if not PROFILENAME:
            with open(PROFILES_FILE, "r") as f:
                content = f.read()
                match = search(r'\[Install.*?\]\nDefault=(.*?)\n', content)
                if match:
                    default_profile = match.group(1)
                    PROFILEFOLDER = path.join(FIREFOXFOLDER, default_profile)
                    return PROFILEFOLDER
        else:
            PROFILEFOLDER = path.join(FIREFOXFOLDER, PROFILENAME)
            return PROFILEFOLDER
