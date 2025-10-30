from os import path
import sys

from core.data_tools.language_manager import LanguageManager

# Language Data
LANGUAGES = {"en": "English", "tr": "Türkçe", "zh_CN": "简体中文"}

language_manager = LanguageManager(LANGUAGES)
APP_LANGUAGE = language_manager.get_language()

def change_language(selected_language):
    global APP_LANGUAGE # Use the global APP_LANGUAGE variable
    language_code = [
            lang
                for lang, name in LANGUAGES.items()
                if name == selected_language
            ][0]
    language_manager.save_language(language_code)
    APP_LANGUAGE = language_code

# Global Data
BASE_DIR = getattr(sys, "_MEIPASS", path.abspath(path.join(path.dirname(__file__), "..", ".."))) # This is the path to the root directory of the project

# Icons
ATTENTION_ICON = "attention.png"
CHECK_ICON = "check.png"
THEME_PREVIEW_ICON = "preview.png"
THEME_NOT_SELECTED_ICON = "theme_not_selected.png"
THEME_SELECTED_ICON = "theme_selected.png"
HEADER_TITLE_BACKGROUND = "header_title_background.png"
LINE_TOP = "line_top.png"
RELOAD_ICON = "reload.png"
BLOCK_SPINNER_ICON = "block_spinner.gif"
INSTALL_ICON = "install.png"
REMOVE_ICON = "remove.png"
BACK_ICON = "back.png"
EXIT_ICON = "exit.png"
FINISH_ICON = "finish.png"

ANIMATION_SPEED = 100

ASSETS_PATH = path.join(BASE_DIR, "assets")
THEME_PATH = "themes"
CUSTOM_SCRIPT_LOADER_URL = "https://raw.githubusercontent.com/Hakanbaban53/RealFire-Installer/main/src/data/online/fx-autoconfig.json"
CUSTOM_SCRIPT_LOADER_PATH = "data/fx-autoconfig.json"

# Themes Modal
DATA_URL = "https://raw.githubusercontent.com/FirefoxCSS-Store/FirefoxCSS-Store.github.io/main/docs/themes.json"
DATA_PATH = "data/themes.json"
ITEMS_PER_PAGE = 15


"""Core Data"""
# Theme Details Modal
BASE_URL = "https://raw.githubusercontent.com/FirefoxCSS-Store/FirefoxCSS-Store.github.io/main/docs/"

# Theme Downloader
REPO_PROVIDERS = {
    "github.com": "/archive/refs/heads/master.zip",
    "gitlab.com": "/-/archive/main/main.zip",
    "codeberg.org": "/archive/main.zip",
    "git.gay": "/-/archive/main/main.zip",  # Assume similar to GitLab
}
