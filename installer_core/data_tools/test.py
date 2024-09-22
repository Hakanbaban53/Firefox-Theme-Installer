import tkinter as tk
from tkinter import messagebox

from language_manager import LanguageManager


class AppUI:
    def __init__(self, root, language_manager):
        """
        Initializes the Tkinter app UI with the detected or saved language.

        :param root: Tkinter root window
        :param language_manager: An instance of the LanguageManager class
        """
        self.root = root
        self.language_manager = language_manager
        self.app_language = self.language_manager.get_language()

        # Configure the root window
        self.root.title("Language Manager Test")
        self.root.geometry("300x200")

        # Create UI Elements
        self.create_widgets()

    def create_widgets(self):
        """
        Create the necessary widgets for the UI.
        """
        # Label for the current language
        self.language_label = tk.Label(self.root, text=f"Current Language: {self.app_language}", font=("Arial", 14))
        self.language_label.pack(pady=20)

        # OptionMenu for language selection
        self.language_var = tk.StringVar(self.root)
        self.language_var.set(self.app_language)  # Set the saved language or default as the initial option

        self.language_menu = tk.OptionMenu(self.root, self.language_var, *self.language_manager.supported_languages, command=self.change_language)
        self.language_menu.pack(pady=10)

        # Button to show a messagebox with the current language
        self.show_lang_button = tk.Button(self.root, text="Show Language", command=self.show_language_message)
        self.show_lang_button.pack(pady=10)

    def change_language(self, selected_language):
        """
        Updates the language based on user selection and refreshes the UI.

        :param selected_language: The language selected from the OptionMenu
        """
        self.app_language = selected_language
        self.language_label.config(text=f"Current Language: {self.app_language}")
        self.language_manager.save_language(selected_language)  # Save the selected language to the JSON file

    def show_language_message(self):
        """
        Displays a message box showing the app language.
        """
        messagebox.showinfo("App Language", f"The app is running in: {self.app_language}")


# Test the LanguageManager with a simple Tkinter app
if __name__ == "__main__":
    supported_languages = ['en', 'fr', 'es']  # Example of supported languages
    language_manager = LanguageManager(supported_languages, fallback_language='en')

    # Create the Tkinter window
    root = tk.Tk()

    # Initialize the App UI with LanguageManager
    app = AppUI(root, language_manager)

    # Start the Tkinter main loop
    root.mainloop()