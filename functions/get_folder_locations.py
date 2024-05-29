import os
from re import search
from functions.get_os_properties import OSProperties

def get_profile_folder():
    input_values = OSProperties().get_locations()
    
    FIREFOXFOLDER = input_values["firefox_folder"]
    PROFILENAME = ""
    # print(FIREFOXFOLDER)

    # Get the current user's username
    try:
        current_user = os.getlogin()
    except OSError:
        current_user = os.getenv('USERNAME') or os.getenv('USER')

    if "$USER" in FIREFOXFOLDER:
        # Construct the Firefox folder path with the current user's username
        FIREFOXFOLDER = FIREFOXFOLDER.replace("$USER", current_user)
    
    # Expand environment variables in the FIREFOXFOLDER path
    FIREFOXFOLDER = os.path.expandvars(FIREFOXFOLDER)
    
    # Check if profiles.ini exists
    PROFILES_FILE = os.path.join(FIREFOXFOLDER, "profiles.ini")
    # print(PROFILES_FILE)
    if not os.path.isfile(PROFILES_FILE):
        # print("The profiles.ini file does not exist in the specified Firefox folder.")
        return ""

    # Define default Profile folder path else use -p option
    if not PROFILENAME:
        with open(PROFILES_FILE, "r") as f:
            content = f.read()
            match = search(r'\[Install.*?\]\nDefault=(.*?)\n', content)
            if match:
                default_profile = match.group(1)
                PROFILEFOLDER = os.path.join(FIREFOXFOLDER, default_profile)
                return PROFILEFOLDER
    else:
        PROFILEFOLDER = os.path.join(FIREFOXFOLDER, PROFILENAME)
        return PROFILEFOLDER

# print(get_profile_folder())
