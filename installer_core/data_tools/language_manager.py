from os import path, makedirs
from locale import getdefaultlocale
from json import dump, load

from installer_core.data_tools.get_os_properties import OSProperties


class LanguageManager:
    def __init__(self, base_dir, supported_languages, language_names, fallback_language='en', config_file="config.json"):
        """
        Initializes the LanguageManager with supported languages, language names, a fallback language,
        and handles saving/loading the language from a config file.

        :param supported_languages: A list of supported language codes (e.g., ['en', 'tr']).
        :param language_names: A dictionary mapping language codes to user-friendly names (e.g., {'en': 'English', 'tr': 'Türkçe'}).
        :param fallback_language: The default language code to fall back on if the system language is not supported.
        :param config_file: Path to the configuration file for saving/loading the selected language.
        """
        self.CACHE_PATH = OSProperties(base_dir).get_cache_location()
        self.supported_languages = supported_languages
        self.language_names = language_names  # Map codes to names (e.g. {'en': 'English', 'tr': 'Türkçe'})
        self.fallback_language = fallback_language
        self.config_file = path.join(self.CACHE_PATH, config_file)
        self.system_language = self.detect_system_language()
        self.current_language = self.load_language()  # Load saved language if available

    def detect_system_language(self):
        """
        Detects the system's default language using the locale module.

        :return: A string representing the system's language code (e.g., 'en', 'fr', etc.).
        """
        system_locale = getdefaultlocale()[0]  # Returns a tuple (language_code, encoding)
        if system_locale:
            language_code = system_locale.split('_')[0]  # Extract the language part ('en_US' -> 'en')
            return language_code
        else:
            return None

    def get_language(self):
        """
        Returns the current language code, either loaded from config or detected from the system.

        :return: A string representing the chosen language code for the app.
        """
        return self.current_language

    def get_language_name(self):
        """
        Returns the user-friendly name for the current language.

        :return: A string representing the user-friendly language name.
        """
        return self.language_names.get(self.current_language, self.language_names.get(self.fallback_language))

    def save_language(self, language_code):
        """
        Saves the selected language to a JSON config file. Creates the directory if it doesn't exist.

        :param language_code: The language code to save.
        """
        # Ensure the directory exists
        makedirs(path.dirname(self.config_file), exist_ok=True)

        # Save the language to the config file
        with open(self.config_file, 'w') as file:
            dump({"language": language_code}, file)
        
        self.current_language = language_code


    def load_language(self):
        """
        Loads the saved language from a JSON config file. If no file is found or the language is unsupported, 
        it defaults to the system language or fallback.

        :return: The loaded or default language code.
        """
        if path.exists(self.config_file):
            with open(self.config_file, 'r') as file:
                config = load(file)
                saved_language = config.get("language")
                if saved_language in self.supported_languages:
                    return saved_language
        # Fallback to system-detected language if no saved language exists
        if self.system_language in self.supported_languages:
            return self.system_language
        return self.fallback_language