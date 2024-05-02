from os import getlogin, path
from re import search
from functions.get_os_properties import OSProperties

def get_profile_folder():
    input_values = OSProperties().get_locations()

    FIREFOXFOLDER = input_values["firefox_folder"]
    PROFILENAME = ""

    # Get the current user's username
    current_user = getlogin()

    if "$USER" in FIREFOXFOLDER:
        # Construct the Firefox folder path with the current user's username
        FIREFOXFOLDER = FIREFOXFOLDER.replace("$USER", current_user)

    # Check if profiles.ini exists
    PROFILES_FILE = path.join(FIREFOXFOLDER, "profiles.ini")
    if not path.isfile(PROFILES_FILE):
        PROFILEFOLDER = ""
        return PROFILEFOLDER

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